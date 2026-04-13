#!/usr/bin/env python3
"""
Validation script for the Spanish Cadastre Ontology.

Checks ontology, SKOS vocabularies, and examples for consistency,
completeness, and conformance to EDINT patterns.

Usage:
    python tests/validate.py
"""

import sys
import os
from pathlib import Path
from typing import List, Dict, Set, Tuple, Optional
from rdflib import Graph, URIRef, Literal, Namespace
from rdflib.namespace import RDF, RDFS, OWL, SKOS, XSD
from rdflib.plugins.parsers.notation3 import BadSyntax
import pyshacl


# Namespaces
CAT = Namespace("https://edint.github.io/edint-ontologia-inmuebles/ontology/catastro#")
EDINTKOS = Namespace("http://vocab.linkeddata.es/datosabiertos/kos/edint/")
EDINTKOS_USE = Namespace("http://vocab.linkeddata.es/datosabiertos/kos/edint/uso/")
EDINTKOS_ESTADO = Namespace("http://vocab.linkeddata.es/datosabiertos/kos/edint/estado/")
EDINTKOS_CLASE = Namespace("http://vocab.linkeddata.es/datosabiertos/kos/edint/clase/")
DCTERMS = Namespace("http://purl.org/dc/terms/")
CC = Namespace("http://creativecommons.org/ns#")
VANN = Namespace("http://purl.org/vocab/vann/")
SHACL = Namespace("http://www.w3.org/ns/shacl#")


class ValidationResult:
    def __init__(self, phase: str):
        self.phase = phase
        self.passed = True
        self.messages: List[str] = []
        self.warnings: List[str] = []
        self.errors: List[str] = []

    def add_error(self, message: str):
        self.errors.append(message)
        self.passed = False

    def add_warning(self, message: str):
        self.warnings.append(message)

    def add_info(self, message: str):
        self.messages.append(message)

    def has_errors(self) -> bool:
        return len(self.errors) > 0

    def has_warnings(self) -> bool:
        return len(self.warnings) > 0


class ProjectPaths:
    def __init__(self, project_root: Path):
        self.root = project_root
        self.ontology_dir = project_root / "ontology"
        self.kos_dir = project_root / "kos"
        self.examples_dir = project_root / "examples"
        self.shapes_dir = project_root / "shapes"
        self.tests_dir = project_root / "tests"

    def get_ontology_file(self) -> Path:
        return self.ontology_dir / "catastro.ttl"

    def get_kos_files(self) -> List[Path]:
        return sorted(self.kos_dir.glob("*.ttl"))

    def get_example_files(self) -> List[Path]:
        return sorted(self.examples_dir.glob("*.ttl"))

    def get_shape_files(self) -> List[Path]:
        return sorted(self.shapes_dir.glob("*.ttl"))


def load_graph(file_path: Path, base_uri: Optional[str] = None) -> Optional[Graph]:
    """Load an RDF file into a graph. Returns None on error."""
    g = Graph()
    try:
        g.parse(str(file_path), format="turtle")
        return g
    except BadSyntax as e:
        return None
    except Exception as e:
        return None


def phase_1_parse(paths: ProjectPaths) -> ValidationResult:
    """Phase 1: Parse all TTL files for syntax errors."""
    result = ValidationResult("Parsing")

    files_to_check = [
        paths.get_ontology_file(),
        *paths.get_kos_files(),
        *paths.get_example_files(),
    ]

    loaded_files = []
    failed_files = []

    for file_path in files_to_check:
        if not file_path.exists():
            continue

        g = load_graph(file_path)
        if g is None:
            failed_files.append(str(file_path.relative_to(paths.root)))
        else:
            loaded_files.append(str(file_path.relative_to(paths.root)))

    if failed_files:
        result.add_error(f"Failed to parse {len(failed_files)} file(s):")
        for f in failed_files:
            result.add_error(f"  - {f}")

    result.add_info(f"Loaded {len(loaded_files)} files successfully")

    return result


def phase_2_ontology_self_check(paths: ProjectPaths) -> ValidationResult:
    """Phase 2: Check ontology completeness and conventions."""
    result = ValidationResult("Ontology self-check")

    onto_file = paths.get_ontology_file()
    if not onto_file.exists():
        result.add_error("Ontology file not found: " + str(onto_file))
        return result

    g = load_graph(onto_file)
    if g is None:
        result.add_error("Failed to load ontology file")
        return result

    # Get the ontology IRI
    onto_iri = None
    for s in g.subjects(RDF.type, OWL.Ontology):
        onto_iri = s
        break

    if onto_iri is None:
        result.add_warning("No ontology IRI found (no rdf:type owl:Ontology)")
    else:
        result.add_info(f"Ontology IRI: {onto_iri}")

        # Check versionIRI and versionInfo consistency
        version_info = g.value(onto_iri, OWL.versionInfo)
        version_iri = g.value(onto_iri, OWL.versionIRI)

        if version_info is None:
            result.add_warning("No owl:versionInfo found")
        if version_iri is None:
            result.add_warning("No owl:versionIRI found")

        if version_info and version_iri:
            version_str = str(version_info).strip('"')
            if version_str not in str(version_iri):
                result.add_warning(
                    f"owl:versionIRI ({version_iri}) does not contain version info ({version_str})"
                )

    # Get all catastro: classes and properties
    classes = set()
    object_properties = set()
    datatype_properties = set()

    for s in g.subjects(RDF.type, OWL.Class):
        if s.startswith(CAT):
            classes.add(s)

    for s in g.subjects(RDF.type, OWL.ObjectProperty):
        if s.startswith(CAT):
            object_properties.add(s)

    for s in g.subjects(RDF.type, OWL.DatatypeProperty):
        if s.startswith(CAT):
            datatype_properties.add(s)

    result.add_info(f"Found {len(classes)} classes, {len(object_properties)} object properties, {len(datatype_properties)} data properties")

    # Check labels and comments (bilingual)
    missing_label_en = []
    missing_label_es = []
    missing_comment_en = []
    missing_comment_es = []

    all_terms = classes | object_properties | datatype_properties

    for term in sorted(all_terms):
        term_name = term.split("#")[-1]

        labels_en = list(g.objects(term, RDFS.label))
        labels_es = [l for l in labels_en if l.language == "es"]
        labels_en = [l for l in labels_en if l.language == "en"]

        comments_en = list(g.objects(term, RDFS.comment))
        comments_es = [c for c in comments_en if c.language == "es"]
        comments_en = [c for c in comments_en if c.language == "en"]

        if not labels_en:
            missing_label_en.append(term_name)
        if not labels_es:
            missing_label_es.append(term_name)
        if not comments_en:
            missing_comment_en.append(term_name)
        if not comments_es:
            missing_comment_es.append(term_name)

    if missing_label_en:
        result.add_error(f"{len(missing_label_en)} terms missing @en labels: {', '.join(missing_label_en[:5])}{'...' if len(missing_label_en) > 5 else ''}")
    if missing_label_es:
        result.add_error(f"{len(missing_label_es)} terms missing @es labels: {', '.join(missing_label_es[:5])}{'...' if len(missing_label_es) > 5 else ''}")
    if missing_comment_en:
        result.add_error(f"{len(missing_comment_en)} terms missing @en comments: {', '.join(missing_comment_en[:5])}{'...' if len(missing_comment_en) > 5 else ''}")
    if missing_comment_es:
        result.add_error(f"{len(missing_comment_es)} terms missing @es comments: {', '.join(missing_comment_es[:5])}{'...' if len(missing_comment_es) > 5 else ''}")

    # Check for annotation property declarations
    declared_annot_props = set()
    for s in g.subjects(RDF.type, OWL.AnnotationProperty):
        declared_annot_props.add(s)

    used_metadata_props = set()
    for term in all_terms:
        for p in g.predicates(term):
            if p in [DCTERMS.title, DCTERMS.description, DCTERMS.creator, DCTERMS.license,
                     VANN.preferredNamespacePrefix, VANN.preferredNamespaceUri]:
                used_metadata_props.add(p)

    undeclared = used_metadata_props - declared_annot_props
    if undeclared:
        result.add_warning(f"Metadata properties not declared as owl:AnnotationProperty: {[p.split('#')[-1] for p in undeclared]}")

    return result


def phase_3_skos_validation(paths: ProjectPaths) -> Tuple[ValidationResult, Dict[URIRef, Graph], Dict[URIRef, URIRef]]:
    """Phase 3: Validate SKOS structure and completeness."""
    result = ValidationResult("SKOS structural validation")

    kos_files = paths.get_kos_files()
    if not kos_files:
        result.add_error("No SKOS files found")
        return result, {}, {}

    all_schemes: Dict[URIRef, Graph] = {}
    all_concepts: Dict[URIRef, URIRef] = {}  # concept -> scheme

    for kos_file in kos_files:
        g = load_graph(kos_file)
        if g is None:
            result.add_error(f"Failed to load KOS file: {kos_file.name}")
            continue

        # Find concept schemes
        schemes = set(g.subjects(RDF.type, SKOS.ConceptScheme))
        result.add_info(f"{kos_file.name}: {len(schemes)} concept scheme(s)")

        # Find all concepts and their schemes
        concepts = set(g.subjects(RDF.type, SKOS.Concept))

        # Check each concept
        missing_pref_label_en = []
        missing_pref_label_es = []
        missing_definition_en = []
        missing_definition_es = []
        missing_in_scheme = []
        no_scheme = []

        for concept in concepts:
            scheme = g.value(concept, SKOS.inScheme)
            if scheme is None:
                no_scheme.append(concept.split("/")[-1])
            else:
                all_concepts[concept] = scheme

            # Check prefLabel (bilingual)
            pref_labels = list(g.objects(concept, SKOS.prefLabel))
            pref_labels_en = [l for l in pref_labels if l.language == "en"]
            pref_labels_es = [l for l in pref_labels if l.language == "es"]

            if not pref_labels_en:
                missing_pref_label_en.append(concept.split("/")[-1])
            if not pref_labels_es:
                missing_pref_label_es.append(concept.split("/")[-1])

            # Check definition (bilingual) - recommended by medioambiente pattern
            definitions = list(g.objects(concept, SKOS.definition))
            definitions_en = [d for d in definitions if d.language == "en"]
            definitions_es = [d for d in definitions if d.language == "es"]

            if not definitions_en:
                missing_definition_en.append(concept.split("/")[-1])
            if not definitions_es:
                missing_definition_es.append(concept.split("/")[-1])

        # Report issues
        if no_scheme:
            result.add_error(f"{len(no_scheme)} concepts without skos:inScheme")

        if missing_pref_label_en:
            result.add_error(f"{len(missing_pref_label_en)} concepts missing @en prefLabel")
        if missing_pref_label_es:
            result.add_error(f"{len(missing_pref_label_es)} concepts missing @es prefLabel")
        if missing_definition_en:
            result.add_warning(f"{len(missing_definition_en)} concepts missing @en definition")
        if missing_definition_es:
            result.add_warning(f"{len(missing_definition_es)} concepts missing @es definition")

        # Check top concept consistency
        for scheme in schemes:
            has_top = set(g.objects(scheme, SKOS.hasTopConcept))
            top_concepts = set(g.subjects(SKOS.topConceptOf, scheme))

            if has_top != top_concepts:
                result.add_error(
                    f"Scheme {scheme.split('/')[-1]}: skos:hasTopConcept ({len(has_top)}) "
                    f"!= skos:topConceptOf ({len(top_concepts)})"
                )

            all_schemes[scheme] = g
            result.add_info(f"{len(concepts)} concepts")

        result.messages[-1] = result.messages[-1].rstrip(", ")

        # Check broader/narrower consistency
        for concept in concepts:
            broader = set(g.objects(concept, SKOS.broader))
            narrower = set(g.objects(concept, SKOS.narrower))

            # For each broader, check that it has this concept as narrower
            for b in broader:
                b_narrower = set(g.objects(b, SKOS.narrower))
                if concept not in b_narrower:
                    result.add_warning(
                        f"skos:broader asymmetric: {concept.split('/')[-1]} -> {b.split('/')[-1]} "
                        f"but reverse skos:narrower missing"
                    )

            # For each narrower, check that it has this concept as broader
            for n in narrower:
                n_broader = set(g.objects(n, SKOS.broader))
                if concept not in n_broader:
                    result.add_warning(
                        f"skos:narrower asymmetric: {concept.split('/')[-1]} -> {n.split('/')[-1]} "
                        f"but reverse skos:broader missing"
                    )

        # Check for duplicate concepts (same URI defined multiple times)
        concept_counts = {}
        for triple in g.triples((None, RDF.type, SKOS.Concept)):
            concept_counts[triple[0]] = concept_counts.get(triple[0], 0) + 1

        duplicates = {c: count for c, count in concept_counts.items() if count > 1}
        if duplicates:
            result.add_error(f"{len(duplicates)} duplicate concept definitions: {[c.split('/')[-1] for c in list(duplicates.keys())[:3]]}")

    result.add_info(f"Total: {len(all_schemes)} schemes, {len(all_concepts)} concepts")

    return result, all_schemes, all_concepts


def phase_4_skos_ontology_linkage(paths: ProjectPaths, all_schemes: Dict[URIRef, Graph]) -> ValidationResult:
    """Phase 4: Check that SKOS schemes referenced in ontology exist."""
    result = ValidationResult("SKOS-ontology linkage")

    onto_file = paths.get_ontology_file()
    if not onto_file.exists():
        result.add_error("Ontology file not found")
        return result

    g = load_graph(onto_file)
    if g is None:
        result.add_error("Failed to load ontology file")
        return result

    # Find all owl:imports
    imports = set(g.objects(None, OWL.imports))
    result.add_info(f"Ontology imports {len(imports)} external ontologies")

    # Check that imported SKOS files exist
    missing_imports = []
    for imp in imports:
        # Convert to file path if it's an HTTP URI pointing to the local KOS
        if "vocab.linkeddata.es" in str(imp):
            # This is an expected external import, skip file check
            continue

    # Find all references to concept schemes in the ontology
    # (e.g., in owl:hasValue restrictions on skos:inScheme)
    referenced_schemes = set()

    for obj in g.objects(None, OWL.hasValue):
        if obj.startswith(EDINTKOS) and not obj.startswith(EDINTKOS_USE) and not obj.startswith(EDINTKOS_ESTADO) and not obj.startswith(EDINTKOS_CLASE):
            # This looks like a concept scheme reference
            referenced_schemes.add(obj)

    # Also check for skos:inScheme = SomeScheme in restrictions
    for s, p, o in g.triples((None, OWL.onProperty, SKOS.inScheme)):
        # Get the parent restriction
        parent_restriction = None
        for parent in g.subjects(None, s):
            if (parent, None, None) in g:
                parent_restriction = parent
                break

        if parent_restriction:
            has_value = g.value(parent_restriction, OWL.hasValue)
            if has_value and has_value.startswith(EDINTKOS):
                referenced_schemes.add(has_value)

    if referenced_schemes:
        result.add_info(f"Referenced {len(referenced_schemes)} concept schemes")

        missing_schemes = []
        for scheme in referenced_schemes:
            if scheme not in all_schemes:
                missing_schemes.append(scheme.split("/")[-1])

        if missing_schemes:
            result.add_error(f"Referenced schemes not found in KOS files: {missing_schemes}")

    return result


def phase_5_example_conformance(paths: ProjectPaths, all_schemes: Dict[URIRef, Graph], all_concepts: Dict[URIRef, URIRef]) -> ValidationResult:
    """Phase 5: Check that examples only use defined ontology terms and SKOS concepts."""
    result = ValidationResult("Example conformance")

    example_files = paths.get_example_files()
    if not example_files:
        result.add_warning("No example files found")
        return result

    onto_file = paths.get_ontology_file()
    if not onto_file.exists():
        result.add_error("Ontology file not found")
        return result

    onto_graph = load_graph(onto_file)
    if onto_graph is None:
        result.add_error("Failed to load ontology file")
        return result

    # Collect all defined ontology terms
    defined_classes = set(onto_graph.subjects(RDF.type, OWL.Class))
    defined_obj_props = set(onto_graph.subjects(RDF.type, OWL.ObjectProperty))
    defined_data_props = set(onto_graph.subjects(RDF.type, OWL.DatatypeProperty))
    defined_ontology_terms = defined_classes | defined_obj_props | defined_data_props

    for example_file in example_files:
        g = load_graph(example_file)
        if g is None:
            result.add_error(f"Failed to load example: {example_file.name}")
            continue

        result.add_info(f"Checking {example_file.name}...")

        # Check ontology terms used
        unknown_terms = set()
        for term in set(g.subjects(None, None)) | set(g.predicates(None, None)) | set(g.objects(None, None)):
            if isinstance(term, URIRef) and term.startswith(CAT):
                if term not in defined_ontology_terms:
                    unknown_terms.add(term)

        if unknown_terms:
            result.add_error(f"{example_file.name}: Undefined ontology terms: {[t.split('#')[-1] for t in list(unknown_terms)[:5]]}")

        # Check SKOS concepts used
        unknown_skos = set()
        for term in set(g.subjects(None, None)) | set(g.objects(None, None)):
            if isinstance(term, URIRef) and (term.startswith(EDINTKOS_USE) or term.startswith(EDINTKOS_ESTADO) or term.startswith(EDINTKOS_CLASE)):
                if term not in all_concepts:
                    unknown_skos.add(term)

        if unknown_skos:
            result.add_error(f"{example_file.name}: Undefined SKOS concepts: {[c.split('/')[-1] for c in list(unknown_skos)[:5]]}")

    return result


def phase_6_shacl_validation(paths: ProjectPaths) -> ValidationResult:
    """Phase 6: Run SHACL validation if shapes exist."""
    result = ValidationResult("SHACL validation")

    shape_files = paths.get_shape_files()
    if not shape_files:
        result.add_info("No SHACL shapes found, skipping SHACL validation")
        return result

    example_files = paths.get_example_files()
    if not example_files:
        result.add_warning("No example files to validate against SHACL shapes")
        return result

    # Load all shapes
    shapes_graph = Graph()
    for shape_file in shape_files:
        g = load_graph(shape_file)
        if g is None:
            result.add_error(f"Failed to load SHACL shape: {shape_file.name}")
            continue
        shapes_graph += g

    if len(shapes_graph) == 0:
        result.add_warning("No valid SHACL shapes loaded")
        return result

    result.add_info(f"Loaded {len(shape_files)} SHACL shape file(s)")

    # Validate each example
    for example_file in example_files:
        data_graph = load_graph(example_file)
        if data_graph is None:
            result.add_error(f"Failed to load example for SHACL validation: {example_file.name}")
            continue

        try:
            conforms, results_graph, results_text = pyshacl.validate(
                data_graph,
                shacl_graph=shapes_graph,
                ont_graph=None,
                inference="rdfs",
                abort_on_first=False,
                allow_infos=False,
                allow_warnings=False,
                meta_shacl=False,
                debug=False
            )

            if not conforms:
                result.add_error(f"{example_file.name}: SHACL validation failed")
                # Count violations
                violations = list(results_graph.subjects(None, SHACL.Violation))
                result.add_error(f"  {len(violations)} SHACL violation(s)")
                for v in violations[:3]:  # Show first 3
                    msg = results_graph.value(v, SHACL.resultMessage)
                    path = results_graph.value(v, SHACL.resultPath)
                    result.add_error(f"    - {msg} (on {path})")
                if len(violations) > 3:
                    result.add_error(f"    ... and {len(violations) - 3} more")
            else:
                result.add_info(f"{example_file.name}: SHACL validation PASSED")

        except Exception as e:
            result.add_error(f"{example_file.name}: SHACL validation error: {str(e)[:100]}")

    return result


def print_phase_result(result: ValidationResult, indent: int = 0):
    """Print a validation phase result."""
    prefix = "  " * indent
    status = "PASS" if result.passed else "FAIL"
    print(f"{prefix}[{result.phase}]{'.' * (50 - len(result.phase) - 6)} {status}")

    for msg in result.messages:
        print(f"{prefix}  {msg}")
    for warn in result.warnings:
        print(f"{prefix}  WARNING: {warn}")
    for err in result.errors:
        print(f"{prefix}  ERROR: {err}")


def main():
    # Find project root (go up from tests/ directory)
    project_root = Path(__file__).parent.parent.absolute()
    paths = ProjectPaths(project_root)

    print("=" * 70)
    print("Spanish Cadastre Ontology Validation")
    print(f"Project root: {project_root}")
    print("=" * 70)
    print()

    results = []

    # Phase 1: Parsing
    result1 = phase_1_parse(paths)
    results.append(result1)
    print_phase_result(result1)
    print()

    if result1.has_errors():
        # Don't continue if files don't parse
        print("\nSTOPPING: Parsing errors prevent further validation.")
        return 1

    # Phase 2: Ontology self-check
    result2 = phase_2_ontology_self_check(paths)
    results.append(result2)
    print_phase_result(result2)
    print()

    # Phase 3: SKOS validation (returns schemes and concepts for later phases)
    result3, all_schemes, all_concepts = phase_3_skos_validation(paths)
    results.append(result3)
    print_phase_result(result3)
    print()

    # Phase 4: SKOS-ontology linkage
    result4 = phase_4_skos_ontology_linkage(paths, all_schemes)
    results.append(result4)
    print_phase_result(result4)
    print()

    # Phase 5: Example conformance
    result5 = phase_5_example_conformance(paths, all_schemes, all_concepts)
    results.append(result5)
    print_phase_result(result5)
    print()

    # Phase 6: SHACL validation
    result6 = phase_6_shacl_validation(paths)
    results.append(result6)
    print_phase_result(result6)
    print()

    # Summary
    print("=" * 70)
    print("SUMMARY")
    print("=" * 70)

    passed = sum(1 for r in results if r.passed)
    failed = len(results) - passed
    with_warnings = sum(1 for r in results if r.has_warnings())

    print(f"Phases passed: {passed}/{len(results)}")
    print(f"Phases with warnings: {with_warnings}")

    if failed > 0:
        print(f"\nFAILED: {failed} phase(s) failed. Fix issues above.")
        return 1
    else:
        print("\nSUCCESS: All validation phases passed!")
        if with_warnings > 0:
            print(f"Note: {with_warnings} phase(s) had warnings.")
        return 0


if __name__ == "__main__":
    sys.exit(main())

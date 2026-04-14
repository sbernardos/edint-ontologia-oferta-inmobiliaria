# Examples - Ejemplos

This directory contains example instances of the Real Estate Ontology (Ontología Inmobiliaria) to demonstrate how to create and structure real estate listings in RDF/Turtle format.

## Purpose / Propósito

The examples provided here demonstrate:
- Basic structure of real estate listings
- Integration with the Spanish Cadastre ontology
- Use of controlled vocabularies for property and transaction types
- Geographic location specification using GeoSPARQL
- Bilingual implementation (Spanish/English)

Los ejemplos proporcionados aquí demuestran:
- Estructura básica de anuncios inmobiliarios
- Integración con la ontología del Catastro Español
- Uso de vocabularios controlados para tipos de inmuebles y transacciones
- Especificación de ubicación geográfica usando GeoSPARQL
- Implementación bilingüe (español/inglés)

## Available Examples / Ejemplos Disponibles

### 1. Sale Listing Example (Ejemplo de Venta)
**File:** `listing-sale-example.ttl`

This example shows a residential property for sale, including:
- Dwelling property type (vivienda)
- Sale transaction type (venta)
- Reference to cadastral property entity
- Active listing status
- Geographic coordinates

Este ejemplo muestra una vivienda en venta, incluyendo:
- Tipo de inmueble vivienda
- Tipo de transacción venta
- Referencia a entidad catastral de inmueble
- Estado de anuncio activo
- Coordenadas geográficas

### 2. Rent Listing Example (Ejemplo de Alquiler)
**File:** `listing-rent-example.ttl`

This example shows a commercial property for rent, including:
- Commercial local property type (local comercial)
- Rent transaction type (alquiler)
- Reference to cadastral property entity
- Active listing status
- Geographic coordinates

Este ejemplo muestra un local comercial en alquiler, incluyendo:
- Tipo de inmueble local comercial
- Tipo de transacción alquiler
- Referencia a entidad catastral de inmueble
- Estado de anuncio activo
- Coordenadas geográficas

### 3. Complete Listing Example (Ejemplo Completo)
**File:** `listing-complete-example.ttl`

This comprehensive example demonstrates:
- Multiple property types (dwelling, office, commercial)
- Different transaction types (sale, rent)
- Complete cadastral information
- Detailed geographic location
- Active and inactive listings
- Full metadata documentation

Este ejemplo comprensivo demuestra:
- Múltiples tipos de inmuebles (vivienda, oficina, comercial)
- Diferentes tipos de transacciones (venta, alquiler)
- Información catastral completa
- Ubicación geográfica detallada
- Anuncios activos e inactivos
- Documentación completa de metadatos

## Format / Formato

All examples are provided in **Turtle (.ttl)** format, which is a human-readable RDF serialization format.

Todos los ejemplos se proporcionan en formato **Turtle (.ttl)**, que es un formato de serialización RDF legible para humanos.

## Usage / Uso

### Validating Examples / Validando Ejemplos

To validate an example instance, use the provided validation script:

Para validar una instancia de ejemplo, use el script de validación proporcionado:

```bash
python tests/validate.py examples/listing-sale-example.ttl
python tests/validate.py examples/listing-rent-example.ttl
python tests/validate.py examples/listing-complete-example.ttl
```

### Querying Examples / Consultando Ejemplos

To query the examples using SPARQL:

Para consultar los ejemplos usando SPARQL:

```bash
# Load an example into your SPARQL endpoint
# Cargue un ejemplo en su punto final SPARQL

# Then execute one of the queries from the requirements/ directory
# Luego ejecute una de las consultas del directorio requirements/
sparql --query requirements/CQ01.sparql --data examples/listing-sale-example.ttl
```

### Creating New Examples / Creando Nuevos Ejemplos

1. Copy one of the existing example files as a template
2. Modify the identifiers and property values
3. Ensure all required properties are present
4. Validate using the validation script
5. Add appropriate documentation

1. Copie uno de los archivos de ejemplo existentes como plantilla
2. Modifique los identificadores y valores de propiedades
3. Asegúrese de que todas las propiedades requeridas estén presentes
4. Valide usando el script de validación
5. Agregue documentación apropiada

## Structure / Estructura

Each example follows this basic structure:

Cada ejemplo sigue esta estructura básica:

```turtle
@prefix edintinm: <https://edint.github.io/edint-ontologia-inmuebles/ontology/inmobiliaria#> .
@prefix dcterms: <http://purl.org/dc/terms/> .
@prefix skos: <http://www.w3.org/2004/02/skos/core#> .

# Create a listing
# Crear un anuncio
ex:Listing001 a edintinm:RealEstateListing ;
    dcterms:identifier "LIST-001" ;
    edintinm:propertyType <property-type-uri> ;
    edintinm:transactionType <transaction-type-uri> ;
    edintinm:isActive true ;
    edintinm:refersToCadastralEntity <cadastral-entity-uri> .
```

## Required Properties / Propiedades Requeridas

Each real estate listing MUST include:

Cada anuncio inmobiliario DEBE incluir:

- `rdf:type` = `edintinm:RealEstateListing`
- `dcterms:identifier` = Unique identifier
- `edintinm:propertyType` = Type of property (SKOS concept)
- `edintinm:transactionType` = Type of transaction (SKOS concept)
- `edintinm:refersToCadastralEntity` = Reference to cadastral entity

Optional properties:

Propiedades opcionales:

- `edintinm:isActive` = Boolean status (default: true)

## Related Files / Archivos Relacionados

- `requirements/requirements.csv` - Competency questions and SPARQL mappings
- `requirements/CQ*.sparql` - SPARQL query examples
- `ontology/inmobiliaria.ttl` - Main ontology definition
- `tests/validate.py` - Validation script

## Integration Notes / Notas de Integración

These examples integrate with:

Estos ejemplos se integran con:

- **EDINT Catastro Ontology**: For cadastral property references
- **GeoSPARQL**: For geographic location specification
- **SKOS Vocabularies**: For property and transaction types
- **Dublin Core Terms (dcterms)**: For identifiers and metadata

## Contact / Contacto

For questions or issues with these examples, please refer to the main repository documentation or file an issue on GitHub.

Para preguntas o problemas con estos ejemplos, por favor refiérase a la documentación principal del repositorio o abra un issue en GitHub.

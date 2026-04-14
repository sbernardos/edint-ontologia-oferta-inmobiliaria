# Implementación de vocabularios

Esta carpeta contiene los archivos de **implementación del vocabulario controlado o KOS (Sistemas de Organización del Conocimiento/ Knowledge Organization Systems)**, que representan la definición formal y legible por máquina de los vocabularios necesarios.


# Propósito

El objetivo de esta carpeta es almacenar los archivos de los **vocabularios controlados o KOS**, que describen los conceptos y las relaciones entre ellos.


# Formatos aceptados

Incluya recursos en los siguientes formatos:

- `.owl` — Ficheros Ontology Web Language files
- `.rdf` — Ficheros  Resource Description Framework files
- `.ttl` — Serialización en Turtle
- `.jsonld` — JSON para datos enlazados

# Vocabularios SKOS implementados

| Archivo | ConceptScheme | Prefijo | Descripción |
|---------|--------------|---------|-------------|
| **Catastro ontology** | | | |
| `catastro-use.ttl` | `edintkos:Uso` | `edintkos-use:` | Vocabulario controlado de usos para el Catastro Español (15 conceptos: Residencial, Industrial, Oficinas, Comercial, Deportivo, Espectáculos, Ocio-Hostelería, Sanitario, Cultural, Religioso, Educativo, Singular, Aparcamiento-Almacenamiento, Espacios Libres, Agrícola) |
| `catastro-estado.ttl` | `edintkos:Estado` | `edintkos-estado:` | Vocabulario controlado de estados de conservación (4 conceptos: Normal, Regular, Deficiente, Ruinoso) |
| `catastro-clase.ttl` | `edintkos:Clase` | `edintkos-clase:` | Vocabulario controlado de clasificación catastral (Urbana, Rural, BICES A-D) |
| **Inmobiliaria ontology** | | | |
| `inmobiliaria-transaction-type.ttl` | `edintkos:TransactionType` | `edintkos-trans:` | Vocabulario controlado de tipos de transacción inmobiliaria (3 conceptos: Venta, Alquiler, Traspaso) |

# Buenas prácticas

- Mantenga las versiones del vocabulario o KOS claramente etiquetadas y documentadas.
- Valide la sintaxis y semántica antes de realizar cambios.
- Mantenga la coherencia con los diagramas conceptuales y la documentación almacenados en la carpeta de conceptualización, si corresponde.
- Utilice una estrategia estandarizada de espacios de nombres y prefijos.


# Notas

- Esta carpeta debe contener únicamente **archivos de implementación** — no diagramas, notas ni documentación.
- Considere mantener un registro de cambios o un archivo de historial de versiones si se mantienen múltiples versiones de los vocabularios.

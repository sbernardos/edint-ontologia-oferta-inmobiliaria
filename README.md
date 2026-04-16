# Ontología EDINT Inmobiliaria (EDINT Real Estate Ontology)

La ontología Inmobiliaria representa el dominio de ofertas inmobiliarias en el contexto español.

# Propósito y alcance de la ontología (Purpose and scope of the ontology)

El propósito de la ontología Inmobiliaria es modelar ofertas inmobiliarias (venta, alquiler, traspaso) en el contexto español. 
El alcance de la ontología está limitado a la representación de anuncios inmobiliarios y su relación con entidades catastrales.

# Prefijo y espacio de nombres (Prefix and namespace)

El prefijo de la ontología es: `edintinm` y se encuentra publicada en el espacio de nombres: [http://vocab.linkeddata.es/datosabiertos/def/oferta-inmobiliaria/](http://vocab.linkeddata.es/datosabiertos/def/oferta-inmobiliaria/)

# Modelo conceptual (Ontology conceptualization)

![Diagrama del modelo conceptual](diagrams/diagrama-inmobiliaria.drawio.png)

# Cómo usar esta ontología (How to use this ontology)

## Basic Usage / Uso Básico

To create a real estate listing, follow this structure:

Para crear un anuncio inmobiliario, siga esta estructura:

```turtle
@prefix edintinm: <http://vocab.linkeddata.es/datosabiertos/def/oferta-inmobiliaria/> .
@prefix dcterms: <http://purl.org/dc/terms/> .
@prefix skos: <http://www.w3.org/2004/02/skos/core#> .

ex:MyListing a edintinm:RealEstateListing ;
    dcterms:identifier "LIST-001" ;
    edintinm:propertyType <http://vocab.linkeddata.es/datosabiertos/kos/edint/uso/V1A> ;
    edintinm:transactionType <http://vocab.linkeddata.es/datosabiertos/kos/edint/transaction-type/venta> ;
    edintinm:isActive true ;
    edintinm:refersToCadastralEntity <cadastral-entity-uri> .
```

## Property Types / Tipos de Inmuebles

The ontology uses the Spanish Cadastre use vocabulary:

La ontología utiliza el vocabulario de usos del Catastro Español:

- `V1A` - Vivienda / Dwelling
- `V2A` - Local Comercial / Commercial Local
- `V2B` - Oficina / Office
- `V2C` - Nave Industrial / Industrial Warehouse
- `V4` - Solar / Plot

## Transaction Types / Tipos de Transacción

Available transaction types:

Tipos de transacción disponibles:

- `venta` - Sale / Venta
- `alquiler` - Rent / Alquiler
- `traspaso` - Transfer / Traspaso

## SPARQL Queries / Consultas SPARQL

Example query to get all active listings:

Consulta de ejemplo para obtener todos los anuncios activos:

```sparql
PREFIX edintinm: <http://vocab.linkeddata.es/datosabiertos/def/oferta-inmobiliaria/>
PREFIX dcterms: <http://purl.org/dc/terms/>

SELECT ?listing ?listingId
WHERE {
  ?listing a edintinm:RealEstateListing ;
           dcterms:identifier ?listingId ;
           edintinm:isActive true .
}
```

See `requirements/` directory for more competency questions and SPARQL queries.

Vea el directorio `requirements/` para más preguntas de competencia y consultas SPARQL.

## Examples / Ejemplos

Example instances are available in the `examples/` directory:

Las instancias de ejemplo están disponibles en el directorio `examples/`:

- `listing-sale-example.ttl` - Sale listing / Anuncio de venta
- `listing-rent-example.ttl` - Rent listing / Anuncio de alquiler
- `listing-complete-example.ttl` - Complete example / Ejemplo completo

See `examples/README.md` for detailed documentation.

Vea `examples/README.md` para documentación detallada.

## Validation / Validación

Validate instances using the provided script:

Valide instancias usando el script proporcionado:

```bash
python tests/validate.py examples/listing-sale-example.ttl
```

# Estructura del repositorio (Repository structure)

El repositorio debe contener (al menos) las siguientes carpetas

| Carpeta | Descripción |
|--------|--------------|
| **diagrams/** | Contiene diagramas y otros recursos que representan el modelo conceptual de la ontología (por ejemplo, jerarquías de clases, relaciones). |
| **documentation/** | Contiene la documentación de la ontología y artefactos relacionados en formato HTML o dirigida a usuarios. |
| **tests/** | Contiene las pruebas para la evaluación de la ontología. |
| **kos/** | Contiene la implementación de vocabularios controlados o KOS relacionados con la ontología Inmobiliaria (transaction-type). Los vocabularios del catastro (uso, estado, clase) están en el repositorio [edint-ontologia-catastro](https://github.com/edint/edint-ontologia-catastro).|
| **ontology/** | Contiene los archivos de implementación de la ontología Inmobiliaria en formatos como .owl, .rdf, .ttl o .jsonld |
| **requirements/** | Contiene todos los documentos utilizados para definir los requisitos de la ontología: ejemplos de datos, preguntas de competencia, requisitos funcionales, casos de uso, etc. |
| **shapes/** | Contiene las restricciones SHACL utilizad para validar datos respecto a la ontología.  |

# Mantenimiento y evolución (Maintenance and evolution)

Para manejar las incidencias o mejoras sugeridas con respecto a la ontología, recomendamos seguir las guías proporcionadas en ([Issues Management](./ISSUES.md)) para generar una incidencia.

# Financiación (Funding)

Esta ontología ha sido desarrollada en el contexto del Espacio de Datos para las Infraestructuras Urbanas Inteligentes ([EDINT](https://edint.es)).

# Relación con otras ontologías (Relationship with other ontologies)

Esta ontología importa y se integra con:

- **EDINT Catastro** ([edint-ontologia-catastro](https://github.com/edint/edint-ontologia-catastro)) — Para acceder a información catastral como parcelas, propiedades y construcciones.
- **GeoSPARQL** — Para especificar la ubicación geográfica de los inmuebles usando geometrías y coordenadas WKT.
- **SKOS Vocabularies** — Para usar vocabularios controlados:
  - Uso de Catastro: `http://vocab.linkeddata.es/datosabiertos/kos/edint/uso`
  - Tipo de Transacción: `http://vocab.linkeddata.es/datosabiertos/kos/edint/transaction-type`

### Integration Details / Detalles de Integración

**Catastral References / Referencias Catastrales:**

La propiedad `edintinm:refersToCadastralEntity` vincula anuncios inmobiliarios con:

- `catastro:CadastralProperty` — Para edificios o unidades (viviendas, locales, oficinas)
- `catastro:CadastralParcel` — Para terrenos o solares

Esto permite acceder a información catastral completa:
- Referencia catastral (14 dígitos)
- Dirección (calle, número, código postal, ciudad, provincia)
- Geometría (coordenadas)

**Geographic Location / Ubicación Geográfica:**

A través de la integración con GeoSPARQL:
- `geo:hasGeometry` — Referencia a la geometría de la entidad catastral
- `geo:asWKT` — Coordenadas en formato Well-Known Text (WKT)
- Tipos de geometría soportados: Point, Polygon, etc.

![Logos](./resources/EDINT_UE_V-Color.png)

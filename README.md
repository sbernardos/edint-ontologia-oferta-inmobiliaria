# Ontología EDINT Inmobiliaria (EDINT Real Estate Ontology)

La ontología Inmobiliaria representa el dominio de ofertas inmobiliarias en el contexto español.

# Propósito y alcance de la ontología (Purpose and scope of the ontology)

El propósito de la ontología Inmobiliaria es modelar ofertas inmobiliarias (venta, alquiler, traspaso) en el contexto español. 
El alcance de la ontología está limitado a la representación de anuncios inmobiliarios y su relación con entidades catastrales.

# Prefijo y espacio de nombres (Prefix and namespace)

El prefijo de la ontología es: `edintinm` y se encuentra publicada en el espacio de nombres: [https://edint.github.io/edint-ontologia-inmuebles/ontology/inmobiliaria](https://edint.github.io/edint-ontologia-inmuebles/ontology/inmobiliaria)

# Modelo conceptual (Ontology conceptualization)

Cada repositorio de desarrollo de ontologías debe incluir, en este README principal, una representación visual de la conceptualización de la ontología.
Esta imagen ayuda a los usuarios y colaboradores a comprender rápidamente la estructura de la ontología, sus conceptos clave y las relaciones entre ellos.

- La imagen debe estar ubicada en la carpeta de conceptualización.
- Formatos aceptados: .svg, .png o .drawio.
- Debe referenciarse en este README usando la sintaxis de Markdown, por ejemplo:

![Diagrama del modelo conceptual](diagrams/diagrama-inmobiliaria.drawio.png)

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

![Logos](./resources/EDINT_UE_V-Color.png)

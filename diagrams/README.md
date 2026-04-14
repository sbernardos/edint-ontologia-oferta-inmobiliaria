# Recursos de conceptualización de ontologías

Esta carpeta contiene todos los  **recursos relacionados con las fases de conceptualización y diseño** de la ontología.

#  Propósito

El objetivo de este directorio es almacenar **materiales gráficos** que apoyen la comprensión y definición de los conceptos, relaciones y la estructura de la ontología, así como de su implementación (por ejemplo, en OWL o RDF)

# Contenidos

## Diagramas

### Diagrama del modelo conceptual (`diagrama-inmobiliaria.drawio`)

- **Formato**: draw.io (editable) y PNG (visualización)
- **Descripción**: Diagrama que muestra la clase principal de la ontología Inmobiliaria y sus relaciones.
- **Clases mostradas**: RealEstateListing
- **Relaciones**: propertyType, transactionType, refersToCadastralEntity, isActive, identifier

Incluya cualquier archivo que represente o respalde el modelo conceptual de la ontología, como por ejemplo:

- **Diagramas** ilustraciones de clases, relaciones y jerarquías.

**Nota**: Los diagramas del catastro han sido movidos al repositorio separado [edint-ontologia-catastro](https://github.com/edint/edint-ontologia-catastro). 

# Formatos aceptados

Incluya recursos en los siguientes formatos:
- `.svg` — Graficos en formato vectorial  
- `.png` — Diagramas o capturas de pantalla  
- `.drawio` — Diagramas editables creados con[diagrams.net (draw.io)](https://app.diagrams.net/)  
Podrían inlcuire otros formatos si son relevantes para la descripción de la conceptualización (por ejemplo, `.pdf`, `.jpg`, `.pptx`).

# Notas

- Mantener versiones de los diagramas cuando se produzcan cambios conceptuales importantes. 
- Esta carpeta **no** contiene código de la ontología ni archivos OWL/RDF; estos deben ubicarse en la carpeta de implementación (ontologia o vocabularios).  
- Comprobar que todos los diagramas sean coherentes con las especificaciones más recientes de la ontología.
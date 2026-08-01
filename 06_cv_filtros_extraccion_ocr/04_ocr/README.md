# 04 - Extracción OCR con pdfminer

Este módulo cubre la extracción de texto de documentos PDF utilizando la librería pdfminer.six, desde extracción básica hasta análisis avanzado.

## 📋 Contenido

### 01 - Extracción Básica
**Archivo**: `01_pdfminer.py`

Extracción simple de texto de archivos PDF:
- Carga de documentos PDF
- Extracción de texto completo
- Verificación de existencia de archivos
- Guardado de texto en archivo

**Conceptos**:
- Función extract_text()
- Manejo de rutas de archivos
- Codificación UTF-8
- Escritura de archivos

### 02 - Análisis Avanzado
**Archivo**: `02_pdfminer_avanzado.py`

Análisis completo y detallado de documentos PDF:
- Extracción de metadatos (autor, título, fecha, etc.)
- Conteo de páginas
- Análisis por página (palabras, caracteres)
- Estadísticas de contenido
- Búsqueda de patrones (emails, URLs, números)
- Palabras más frecuentes
- Generación de reportes

**Conceptos**:
- PDFParser y PDFDocument
- Extracción de metadatos
- Análisis de contenido
- Expresiones regulares
- Estadística de frecuencias

## 🔧 Requisitos

```bash
pip install pdfminer.six
```

## 🚀 Uso

Ejecuta cada script desde esta carpeta:

```bash
# Extracción básica
python .\01_pdfminer.py

# Análisis avanzado
python .\02_pdfminer_avanzado.py
```

## 📚 Conceptos Clave

### OCR (Optical Character Recognition)
Tecnología para convertir imágenes de texto en texto editable.

**Nota**: pdfminer.six extrae texto de PDFs que ya contienen texto digital, no realiza OCR en imágenes.

### Metadatos
Información sobre el documento (autor, título, fecha de creación, etc.).

### Expresiones Regulares
Patrones para buscar y extraer información específica del texto.

### Análisis de Frecuencia
Identificación de palabras más comunes en un documento.

## 📝 Estructura de Salida

### Extracción Básica
Genera:
- `texto_extraido.txt`: Texto completo del PDF

### Análisis Avanzado
Genera:
- `texto_completo.txt`: Texto completo del PDF
- `analisis_pdf.txt`: Reporte con estadísticas y análisis

## 💡 Consejos

1. Verifica que la ruta del PDF sea correcta antes de ejecutar
2. Asegúrate de que el PDF contiene texto digital (no solo imágenes)
3. Para PDFs con imágenes de texto, considera usar OCR (Tesseract, EasyOCR)
4. Experimenta con diferentes patrones regex para extraer información específica
5. Guarda los resultados para análisis posterior

## 🔍 Patrones Regex Útiles

```python
# Emails
r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

# URLs
r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'

# Números
r'\b\d+\b'

# Fechas (DD/MM/YYYY)
r'\d{2}/\d{2}/\d{4}'

# Teléfonos
r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b'
```

## 📖 Referencias

- [pdfminer.six Documentation](https://pdfminersix.readthedocs.io/)
- [pdfminer.six GitHub](https://github.com/pdfminer/pdfminer.six)
- [Python Regular Expressions](https://docs.python.org/3/library/re.html)
- [Collections.Counter](https://docs.python.org/3/library/collections.html#collections.Counter)

## 📝 Notas Importantes

- **pdfminer.six** extrae texto de PDFs digitales, no realiza OCR
- Para PDFs con imágenes de texto, usa librerías como:
  - Tesseract (con pytesseract)
  - EasyOCR
  - PaddleOCR
- Los metadatos pueden no estar disponibles en todos los PDFs
- La extracción depende de cómo esté estructurado el PDF

## 🎯 Aplicaciones Prácticas

- **Extracción de datos**: Obtener información de documentos
- **Análisis de contenido**: Estadísticas y palabras clave
- **Búsqueda**: Indexación de documentos
- **Automatización**: Procesamiento batch de múltiples PDFs
- **Análisis de texto**: NLP y análisis de sentimientos

## ⚠️ Limitaciones

- No realiza OCR en imágenes dentro de PDFs
- Puede tener dificultades con PDFs protegidos
- La calidad de extracción depende de la estructura del PDF
- No extrae imágenes o gráficos

## 🔧 Extensiones Posibles

1. Procesar múltiples PDFs en una carpeta
2. Integrar con bases de datos
3. Combinar con NLP para análisis de sentimientos
4. Crear índices de búsqueda
5. Generar reportes automáticos

---

**Última actualización**: Octubre 2025

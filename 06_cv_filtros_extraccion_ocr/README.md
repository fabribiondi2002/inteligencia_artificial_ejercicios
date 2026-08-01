# 06 - Filtros, Detección de Bordes, Pirámides y Extracción OCR

Este módulo cubre técnicas avanzadas de procesamiento de imágenes incluyendo filtros digitales, detección de bordes, pirámides de imágenes y extracción de texto de documentos PDF.

## 📋 Contenido

### 01 - Filtros de Imagen
Aplicación de diversos filtros para procesamiento y mejora de imágenes:
- **Filtro Gaussiano**: Suavizado de imágenes usando distribución gaussiana
- **Filtro de Mediana**: Eliminación de ruido preservando bordes
- **Filtro DoG (Difference of Gaussians)**: Detección de características
- **Unsharp Masking**: Mejora de nitidez y contraste
- **Transformada de Fourier**: Análisis en dominio de frecuencias

### 02 - Detección de Bordes
Técnicas para identificar y resaltar bordes en imágenes:
- **Operadores de Bordes**: Sobel, Prewitt y otros operadores básicos
- **Algoritmo de Canny**: Implementación manual del detector de bordes Canny
- **Canny con OpenCV**: Uso de la función optimizada de OpenCV
- **Coincidencia de Plantillas**: Búsqueda de patrones en imágenes
- **Coincidencia Múltiple**: Detección de múltiples instancias de un patrón

### 03 - Pirámides de Imágenes
Técnicas de multiresolución para análisis jerárquico de imágenes:
- **Pirámides Gaussianas**: Reducción progresiva de resolución
- **Pirámides Laplacianas**: Extracción de detalles en diferentes escalas
- **Fusión de Imágenes**: Combinación de múltiples imágenes usando pirámides

### 04 - Extracción OCR
Extracción de texto de documentos PDF usando pdfminer:
- **Extracción Básica**: Obtención simple de texto de PDFs
- **Análisis Avanzado**: Extracción de metadatos, análisis estadístico y búsqueda de patrones

## 🔧 Requisitos

```bash
pip install opencv-python numpy matplotlib scikit-image pdfminer.six
```

## 📁 Estructura del Proyecto

```
06_cv_filtros_extraccion_ocr/
├── README.md
├── 01_filtros/
│   ├── README.md
│   ├── 01_filtro_gaussiano.py
│   ├── 02_filtro_mediana.py
│   ├── 03_filtro_dog.py
│   ├── 04_filtro_unsharp_masking.py
│   └── 05_fourier.py
├── 02_bordes/
│   ├── README.md
│   ├── 01_bordes.py
│   ├── 02_canny_a_mano.py
│   ├── 03_canny_opencv.py
│   ├── 04_template1.py
│   └── 05_template_multiple.py
├── 03_piramides/
│   ├── README.md
│   ├── 01_piramides.py
│   ├── 02_paramide_laplaciana.py
│   └── 03_fusion_img.py
├── 04_ocr/
│   ├── README.md
│   ├── 01_pdfminer.py
│   └── 02_pdfminer_avanzado.py
├── img/                          # Imágenes de ejemplo
└── documentos/                   # Documentos PDF para OCR
```

## 🚀 Uso

Cada subcarpeta contiene ejemplos específicos con su propia documentación. Navega a cada carpeta y consulta su README para instrucciones detalladas.

Para ejecutar un script específico:

```bash
# Desde la carpeta del módulo
python .\nombre_script.py
```

## 📚 Conceptos Clave

- **Filtros**: Transformaciones que modifican los píxeles basándose en sus vecinos
- **Detección de Bordes**: Identificación de cambios abruptos de intensidad
- **Pirámides**: Representación multiresolución de imágenes
- **OCR**: Reconocimiento Óptico de Caracteres y extracción de texto
- **Kernels**: Matrices pequeñas usadas en operaciones de convolución

## 📖 Referencias

- [OpenCV Tutorials - Image Filtering](https://docs.opencv.org/4.x/d4/d13/tutorial_py_filtering.html)
- [OpenCV Tutorials - Edge Detection](https://docs.opencv.org/4.x/da/d22/tutorial_py_canny.html)
- [OpenCV Tutorials - Image Pyramids](https://docs.opencv.org/4.x/dc/d52/tutorial_py_image_pyramids.html)
- [pdfminer.six Documentation](https://pdfminersix.readthedocs.io/)
- [scikit-image Documentation](https://scikit-image.org/)

## 💡 Consejos

1. Comienza con los filtros básicos antes de pasar a técnicas más complejas
2. Experimenta con diferentes parámetros para entender su efecto
3. Usa `matplotlib` para visualizar los resultados intermedios
4. Revisa los comentarios en el código para entender cada paso
5. Prueba con tus propias imágenes después de completar los ejemplos

---

**Última actualización**: Octubre 2025

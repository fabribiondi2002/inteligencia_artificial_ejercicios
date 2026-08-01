# 05 - Imágenes Binarias y Morfología

Este módulo cubre los fundamentos del procesamiento de imágenes binarias y operaciones morfológicas utilizando OpenCV y Python.

## 📋 Contenido

### 01 - Escala de Grises
Conversión de imágenes a color a escala de grises utilizando diferentes métodos.

### 02 - Umbralización
Técnicas de umbralización para convertir imágenes en escala de grises a imágenes binarias:
- **Umbralización simple**: Diferentes tipos de thresholding básicos
- **Umbralización adaptativa**: Thresholding adaptativo para imágenes con iluminación variable
- **Método de Otsu**: Cálculo automático del umbral óptimo

### 03 - Operaciones Morfológicas
Transformaciones geométricas y operaciones morfológicas:
- **Traslación**: Desplazamiento de imágenes
- **Rotación**: Rotación de imágenes alrededor de un punto
- **Escalado**: Redimensionamiento con diferentes métodos de interpolación
- **Transformación de perspectiva**: Corrección de perspectiva mediante selección de puntos
- **Operaciones morfológicas**: Erosión, dilatación, apertura, cierre y gradiente

## 🔧 Requisitos

```bash
pip install opencv-python numpy matplotlib
```

## 📁 Estructura del Proyecto

```
05_imagenes_binarias_morfologia/
├── README.md
└── ejemplos/
    ├── img/                          # Imágenes de ejemplo
    ├── 01_gray_scale/
    │   ├── README.md
    │   └── gray_scale.py
    ├── 02_umbralización/
    │   ├── README.md
    │   ├── 01_umbralizacion_simple.py
    │   ├── 02_umbralizacion_adaptativa.py
    │   └── 03_umbralizacion_otsu.py
    └── 03_operaciones_morfologicas/
        ├── README.md
        ├── 01_traslacion.py
        ├── 02_rotacion.py
        ├── 03_escalado.py
        ├── 04_perspectiva.py
        └── 05_morfologicas.py
```

## 🚀 Uso

Cada subcarpeta contiene ejemplos específicos con su propia documentación. Navega a cada carpeta y consulta su README para instrucciones detalladas.

## 📚 Conceptos Clave

- **Imágenes en escala de grises**: Representación de imágenes con un solo canal de intensidad
- **Umbralización**: Proceso de convertir imágenes en escala de grises a binarias
- **Operaciones morfológicas**: Transformaciones basadas en la forma de los objetos en la imagen
- **Kernels**: Elementos estructurantes utilizados en operaciones morfológicas

## 📖 Referencias

- [Documentación de OpenCV - Thresholding](https://docs.opencv.org/4.x/d7/d4d/tutorial_py_thresholding.html)
- [Documentación de OpenCV - Morphological Transformations](https://docs.opencv.org/4.x/d9/d61/tutorial_py_morphological_ops.html)
- [Documentación de OpenCV - Geometric Transformations](https://docs.opencv.org/4.x/da/d6e/tutorial_py_geometric_transformations.html)

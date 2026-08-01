# 07 - Segmentación y Detección de Color

Este módulo cubre técnicas avanzadas de segmentación de imágenes, detección de colores en el espacio HSV, tracking de objetos y conteo de elementos mediante análisis de contornos.

## 📋 Contenido

### Algoritmo Watershed

- **01_Algoritmo_Watershed.py**: Implementación completa del algoritmo Watershed para segmentación de objetos superpuestos o adyacentes.

### Detección de Color HSV

- **02_color_HSV_imagen.py**: Detección de color rojo en imágenes estáticas usando el espacio de color HSV
- **03_color_HSV_amarillo.py**: Detección de color amarillo en imágenes usando rangos HSV
- **04_color_HSV_cam.py**: Detección de color rojo en tiempo real desde cámara web
- **05_color_track.py**: Tracking multi-color (azul, amarillo y rojo) con detección de centroides y contornos

### Segmentación Avanzada

- **06_segmentacion_color_img.py**: Segmentación por color con fondo en escala de grises en imágenes estáticas
- **07_segmentacion_color_cam.py**: Segmentación por color en video con fondo en escala de grises

### Conteo de Objetos

- **08_conteo.py**: Conteo básico de objetos mediante umbralización y detección de contornos
- **09_conteo_canny.py**: Conteo de objetos usando el detector de bordes Canny
- **10_conteo_colores.py**: Conteo y clasificación de objetos por color (amarillo, violeta, verde y rojo)

## 🔧 Requisitos

```bash
pip install opencv-python numpy matplotlib imutils
```

## 📁 Estructura del Proyecto

```text
07_cv_segmentacion/
├── README.md
├── src/
│   ├── 01_Algoritmo_Watershed.py
│   ├── 02_color_HSV_imagen.py
│   ├── 03_color_HSV_amarillo.py
│   ├── 04_color_HSV_cam.py
│   ├── 05_color_track.py
│   ├── 06_segmentacion_color_img.py
│   ├── 07_segmentacion_color_cam.py
│   ├── 08_conteo.py
│   ├── 09_conteo_canny.py
│   └── 10_conteo_colores.py
└── img/                          # Imágenes y videos de ejemplo
    ├── angry.mp4
    ├── cartas.png
    ├── colores.png
    ├── lunares.png
    ├── monedas.jpg
    ├── rosas.jpeg
    └── water_coins.jpg
```

## 🚀 Uso

### Ejemplos con Imágenes Estáticas

```bash
# Desde la carpeta src
python 01_Algoritmo_Watershed.py
python 02_color_HSV_imagen.py
python 08_conteo.py
```

### Ejemplos con Cámara Web

```bash
# Desde la carpeta src
python 04_color_HSV_cam.py
python 05_color_track.py
```

**Nota**: Para cerrar las ventanas de video en vivo, presiona la tecla `s` o `ESC` según el script.

### Configuración de Cámara en Linux

Los scripts que usan cámara web están configurados por defecto para Windows. En Linux, es posible que necesites ajustar el índice de la cámara:

```python
# Si la cámara por defecto (0) no funciona, prueba con:
cap = cv2.VideoCapture(1)  # o 2, 3, etc.

# Para sistemas Linux con v4l2, puedes usar:
cap = cv2.VideoCapture(0, cv2.CAP_V4L2)
```

Verifica las cámaras disponibles en Linux con:

```bash
ls /dev/video*
```

## 📚 Conceptos Clave

- **Espacio de Color HSV**: Hue (Matiz), Saturation (Saturación), Value (Valor) - más intuitivo para detección de colores que RGB
- **Watershed**: Algoritmo de segmentación que trata la imagen como un relieve topográfico
- **Máscaras**: Imágenes binarias que definen regiones de interés
- **Contornos**: Curvas que unen puntos continuos con el mismo color o intensidad
- **Momentos**: Características estadísticas de los contornos usadas para calcular centroides y áreas
- **Tracking**: Seguimiento de objetos en secuencias de video

## 🎨 Rangos de Color HSV

### Colores Básicos en HSV (OpenCV)

- **Rojo**: [0-10, 100-255, 20-255] y [170-180, 100-255, 20-255]
- **Amarillo**: [20-32, 100-255, 100-255]
- **Verde**: [36-70, 100-255, 20-255]
- **Azul**: [100-125, 100-255, 20-255]
- **Violeta**: [130-145, 100-255, 20-255]

**Nota**: Los rangos pueden variar según la iluminación. Usa trackbars para ajustar en tiempo real.

## 📖 Referencias

- [OpenCV Tutorials - Color Spaces](https://docs.opencv.org/4.x/df/d9d/tutorial_py_colorspaces.html)
- [OpenCV Tutorials - Contours](https://docs.opencv.org/4.x/d4/d73/tutorial_py_contours_begin.html)
- [OpenCV Tutorials - Watershed Algorithm](https://docs.opencv.org/4.x/d3/db4/tutorial_py_watershed.html)
- [Color Detection in HSV](https://docs.opencv.org/4.x/df/d9d/tutorial_py_colorspaces.html)

## 💡 Consejos

1. Usar el espacio HSV para detección de colores, es más robusto que RGB ante cambios de iluminación
2. Para el color rojo, recordar usar dos rangos (cerca de 0° y 180° en el círculo de matiz)
3. Aplicar operaciones morfológicas para limpiar máscaras con ruido
4. Ajustar los umbrales según el entorno de iluminación
5. Usar `cv2.medianBlur()` para suavizar máscaras sin perder bordes
6. Implementar área mínima al detectar contornos para filtrar ruido

## 🎯 Aplicaciones Prácticas

- Tracking de objetos por color en robótica
- Conteo automático de elementos en líneas de producción
- Segmentación de frutas por madurez (color)
- Detección de señales de tráfico
- Interfaces gestuales basadas en color
- Control industrial mediante detección de colores

---

**Última actualización**: Octubre 2025

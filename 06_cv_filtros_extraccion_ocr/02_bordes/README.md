# 02 - Detección de Bordes

Este módulo cubre técnicas para identificar y resaltar bordes en imágenes, incluyendo operadores clásicos y algoritmos avanzados.

## 📋 Contenido

### 01 - Operadores de Bordes
**Archivo**: `01_bordes.py`

Implementación de operadores clásicos de detección de bordes:
- Operador Sobel
- Operador Prewitt
- Operador Roberts
- Comparación de resultados

**Conceptos**:
- Gradientes de imagen
- Derivadas discretas
- Kernels de detección

### 02 - Algoritmo de Canny (Implementación Manual)
**Archivo**: `02_canny_a_mano.py`

Implementación paso a paso del detector de bordes Canny:
- Suavizado con filtro gaussiano
- Cálculo de gradientes
- Supresión de no-máximos
- Histéresis (umbralización con dos umbrales)

**Conceptos**:
- Algoritmo Canny completo
- Supresión de no-máximos
- Histéresis
- Análisis de rendimiento

### 03 - Canny con OpenCV
**Archivo**: `03_canny_opencv.py`

Uso de la función optimizada de Canny de OpenCV:
- Aplicación directa del algoritmo
- Ajuste de parámetros
- Comparación con implementación manual

**Conceptos**:
- Función cv.Canny()
- Parámetros threshold1 y threshold2
- Optimización en C++

### 04 - Coincidencia de Plantillas (Single)
**Archivo**: `04_template1.py`

Búsqueda de un patrón específico en una imagen:
- Carga de imagen y plantilla
- Aplicación de diferentes métodos de coincidencia
- Visualización de resultados
- Métodos: TM_CCOEFF, TM_CCORR, TM_SQDIFF y sus variantes normalizadas

**Conceptos**:
- Template matching
- Métodos de correlación
- Normalización de resultados

### 05 - Coincidencia Múltiple
**Archivo**: `05_template_multiple.py`

Detección de múltiples instancias de un patrón:
- Búsqueda de todas las coincidencias
- Uso de umbral de confianza
- Dibujo de rectángulos alrededor de coincidencias

**Conceptos**:
- Detección múltiple
- Umbralización de resultados
- Filtrado de coincidencias

## 🔧 Requisitos

```bash
pip install opencv-python numpy matplotlib
```

## 🚀 Uso

Ejecuta cada script desde esta carpeta:

```bash
# Operadores de bordes
python .\01_bordes.py

# Canny manual
python .\02_canny_a_mano.py

# Canny OpenCV
python .\03_canny_opencv.py

# Template matching simple
python .\04_template1.py

# Template matching múltiple
python .\05_template_multiple.py
```

## 📚 Conceptos Clave

### Gradiente
Vector que indica la dirección y magnitud del cambio más rápido en intensidad.

### Supresión de No-Máximos
Técnica para adelgazar los bordes detectados, manteniendo solo los máximos locales.

### Histéresis
Uso de dos umbrales para conectar segmentos de bordes débiles con fuertes.

### Template Matching
Búsqueda de un patrón (plantilla) dentro de una imagen más grande.

### Métodos de Coincidencia
- **TM_CCOEFF**: Coeficiente de correlación
- **TM_CCORR**: Correlación cruzada
- **TM_SQDIFF**: Diferencia de cuadrados
- **_NORMED**: Versiones normalizadas de los anteriores

## 💡 Consejos

1. Comienza con los operadores simples (Sobel) antes de Canny
2. Experimenta con los parámetros de Canny para entender su efecto
3. Para template matching, usa plantillas claras y bien definidas
4. Ajusta el umbral en template matching múltiple según tu aplicación
5. Visualiza los resultados intermedios para entender cada paso

## 📖 Referencias

- [OpenCV - Edge Detection](https://docs.opencv.org/4.x/da/d22/tutorial_py_canny.html)
- [OpenCV - Template Matching](https://docs.opencv.org/4.x/d4/dc6/tutorial_py_template_matching.html)
- [Canny Edge Detection Algorithm](https://en.wikipedia.org/wiki/Canny_edge_detector)
- [Sobel Operator](https://en.wikipedia.org/wiki/Sobel_operator)

## 📝 Notas Importantes

- El algoritmo Canny es uno de los detectores de bordes más populares
- La implementación manual ayuda a entender cada paso del proceso
- Template matching es sensible a rotaciones y cambios de escala
- Para aplicaciones robustas, considera usar características (SIFT, SURF, ORB)

---

**Última actualización**: Octubre 2025

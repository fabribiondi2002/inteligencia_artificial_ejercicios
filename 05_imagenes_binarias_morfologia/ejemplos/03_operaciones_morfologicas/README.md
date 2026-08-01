# Operaciones Morfológicas y Transformaciones Geométricas

Ejemplos de transformaciones geométricas y operaciones morfológicas sobre imágenes.

## 📝 Descripción

Este módulo cubre dos tipos principales de operaciones:

1. **Transformaciones Geométricas**: Modifican la geometría espacial de la imagen
2. **Operaciones Morfológicas**: Procesan imágenes basándose en formas y estructuras

## 🎯 Objetivo

Demostrar cómo aplicar transformaciones para manipular la posición, orientación y forma de las imágenes, así como operaciones morfológicas para procesamiento de imágenes binarias.

## 📋 Archivos

### Transformaciones Geométricas

#### 1. `01_traslacion.py`

Traslación (desplazamiento) de imágenes en el espacio 2D.

**Conceptos:**
- Matriz de transformación afín 2x3
- Desplazamiento en ejes X e Y
- Función `cv2.warpAffine()`

**Uso:**
```bash
python 01_traslacion.py
```

**Matriz de traslación:**
```
M = [[1, 0, tx],
     [0, 1, ty]]
```
Donde `tx` = desplazamiento en X, `ty` = desplazamiento en Y

---

#### 2. `02_rotacion.py`

Rotación de imágenes alrededor de un punto (generalmente el centro).

**Conceptos:**
- Centro de rotación
- Ángulo de rotación (sentido antihorario)
- Factor de escala opcional
- Función `cv2.getRotationMatrix2D()`

**Uso:**
```bash
python 02_rotacion.py
```

**Parámetros:**
- `center`: Punto sobre el cual rotar
- `angle`: Ángulo en grados (+ = antihorario)
- `scale`: Factor de escala (1.0 = sin cambio)

---

#### 3. `03_escalado.py`

Redimensionamiento de imágenes con diferentes métodos de interpolación.

**Métodos de interpolación:**

| Método | Uso Recomendado | Velocidad | Calidad |
|--------|-----------------|-----------|---------|
| **INTER_NEAREST** | Velocidad máxima | ⚡⚡⚡ | ⭐ |
| **INTER_LINEAR** | Uso general | ⚡⚡ | ⭐⭐ |
| **INTER_CUBIC** | Ampliación | ⚡ | ⭐⭐⭐ |
| **INTER_AREA** | Reducción | ⚡⚡ | ⭐⭐⭐ |
| **INTER_LANCZOS4** | Máxima calidad | ⚡ | ⭐⭐⭐⭐ |

**Uso:**
```bash
python 03_escalado.py
```

---

#### 4. `04_perspectiva.py`

Transformación de perspectiva mediante selección interactiva de 4 puntos.

**Conceptos:**
- Mapeo de 4 puntos origen a 4 puntos destino
- Matriz de perspectiva 3x3
- Corrección de perspectiva
- Función `cv2.getPerspectiveTransform()`

**Uso:**
```bash
python 04_perspectiva.py
```

**Instrucciones:**
1. Se abre una ventana con la imagen
2. Haz clic en 4 puntos (orden: sup-izq, sup-der, inf-der, inf-izq)
3. Los puntos se mapean a un rectángulo
4. Se muestra el resultado corregido

**Aplicaciones:**
- Escaneo de documentos
- Corrección de ángulos de cámara
- Extracción de señales de tráfico
- OCR en imágenes con perspectiva

---

### Operaciones Morfológicas

#### 5. `05_morfologicas.py`

Operaciones morfológicas básicas sobre imágenes binarias.

**Operaciones incluidas:**

1. **Erosión** (`cv2.erode()`)
   - Reduce el tamaño de objetos blancos
   - Elimina ruido pequeño
   - Separa objetos conectados débilmente

2. **Dilatación** (`cv2.dilate()`)
   - Aumenta el tamaño de objetos blancos
   - Rellena pequeños huecos
   - Conecta objetos cercanos

3. **Apertura** (`cv2.MORPH_OPEN`)
   - Erosión seguida de dilatación
   - Elimina ruido sin cambiar mucho el tamaño
   - Suaviza contornos

4. **Cierre** (`cv2.MORPH_CLOSE`)
   - Dilatación seguida de erosión
   - Rellena pequeños huecos en objetos
   - Conecta componentes cercanos

5. **Gradiente Morfológico** (`cv2.MORPH_GRADIENT`)
   - Diferencia entre dilatación y erosión
   - Detecta los contornos de objetos
   - Resalta bordes

**Uso:**
```bash
python 05_morfologicas.py
```

**Elemento Estructurante (Kernel):**
- Define la forma de la operación
- Kernel cuadrado: `np.ones((5,5), np.uint8)`
- Tamaños comunes: 3x3, 5x5, 7x7

---

## 🔧 Requisitos

```bash
pip install opencv-python numpy matplotlib
```

## 💡 Conceptos Clave

### Transformaciones Afines vs Perspectiva

| Característica | Transformación Afín | Transformación Perspectiva |
|----------------|---------------------|---------------------------|
| **Matriz** | 2x3 | 3x3 |
| **Líneas paralelas** | Se mantienen | Pueden converger |
| **Puntos necesarios** | 3 | 4 |
| **Ejemplos** | Traslación, rotación, escalado | Corrección de perspectiva |

### Morfología Matemática

**Principio:** Operaciones basadas en la teoría de conjuntos aplicadas a formas en imágenes.

**Elemento Estructurante:** Define el área de influencia y la forma de la operación.

**Propiedades:**
- Operan sobre imágenes binarias
- Pueden extenderse a escala de grises
- Útiles para preprocesamiento
- Base para operaciones más complejas

### Cuándo usar cada operación morfológica

**Erosión:**
- Eliminar ruido blanco pequeño
- Separar objetos unidos
- Adelgazar bordes

**Dilatación:**
- Rellenar huecos pequeños
- Conectar componentes cercanos
- Engrosar bordes

**Apertura:**
- Limpiar ruido blanco manteniendo forma
- Suavizar contornos externos
- Eliminar protrusiones pequeñas

**Cierre:**
- Rellenar huecos negros en objetos
- Conectar componentes cercanos
- Suavizar contornos internos

**Gradiente:**
- Detección de bordes
- Resaltar contornos
- Segmentación básica

## 📊 Aplicaciones Prácticas

### Transformaciones Geométricas
- **Traslación**: Centrado de objetos, data augmentation
- **Rotación**: Corrección de orientación, augmentación
- **Escalado**: Normalización de tamaños, thumbnails
- **Perspectiva**: Escaneo de documentos, placas, señales

### Operaciones Morfológicas
- Preprocesamiento para OCR
- Limpieza de imágenes escaneadas
- Extracción de características
- Segmentación de imágenes
- Detección de bordes
- Análisis de formas

## 🔗 Referencias

- [OpenCV: Geometric Transformations](https://docs.opencv.org/4.x/da/d6e/tutorial_py_geometric_transformations.html)
- [OpenCV: Morphological Transformations](https://docs.opencv.org/4.x/d9/d61/tutorial_py_morphological_ops.html)
- [Mathematical Morphology](https://en.wikipedia.org/wiki/Mathematical_morphology)
- [Image Interpolation](https://en.wikipedia.org/wiki/Image_scaling)

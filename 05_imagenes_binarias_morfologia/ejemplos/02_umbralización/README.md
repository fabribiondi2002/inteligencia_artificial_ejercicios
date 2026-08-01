# Umbralización (Thresholding)

Ejemplos de técnicas de umbralización para convertir imágenes en escala de grises a imágenes binarias.

## 📝 Descripción

La umbralización es el proceso de convertir una imagen en escala de grises a una imagen binaria (blanco y negro). Es uno de los métodos más simples de segmentación de imágenes.

## 🎯 Objetivo

Demostrar diferentes técnicas de umbralización:

- **Global/Simple**: Usa un umbral fijo para toda la imagen
- **Adaptativa**: Calcula umbrales locales para diferentes regiones
- **Otsu**: Calcula automáticamente el umbral óptimo

## 📋 Archivos

### 1. `01_umbralizacion_simple.py`

Demuestra los 5 tipos básicos de umbralización global:

- **THRESH_BINARY**: `valor = maxval if pixel > umbral else 0`
- **THRESH_BINARY_INV**: `valor = 0 if pixel > umbral else maxval`
- **THRESH_TRUNC**: `valor = umbral if pixel > umbral else pixel`
- **THRESH_TOZERO**: `valor = pixel if pixel > umbral else 0`
- **THRESH_TOZERO_INV**: `valor = 0 if pixel > umbral else pixel`

**Uso:**
```bash
python 01_umbralizacion_simple.py
```

### 2. `02_umbralizacion_adaptativa.py`

Umbralización adaptativa para imágenes con iluminación variable:

- **ADAPTIVE_THRESH_MEAN_C**: Umbral = media de vecinos - C
- **ADAPTIVE_THRESH_GAUSSIAN_C**: Umbral = suma ponderada gaussiana - C

Parámetros:
- `blockSize`: Tamaño del área de vecindad (debe ser impar)
- `C`: Constante que se resta del valor calculado

**Uso:**
```bash
python 02_umbralizacion_adaptativa.py
```

### 3. `03_umbralizacion_otsu.py`

Método de Otsu para cálculo automático del umbral óptimo:

- Analiza el histograma de la imagen
- Encuentra el umbral que minimiza la varianza intra-clase
- Funciona mejor con imágenes bimodales (dos picos en el histograma)

Incluye comparación con:
- Umbralización global manual
- Otsu sobre imagen ruidosa
- Otsu sobre imagen filtrada (Gaussiano)

**Uso:**
```bash
python 03_umbralizacion_otsu.py
```

## 🔧 Requisitos

```bash
pip install opencv-python numpy matplotlib
```

## 💡 Conceptos Clave

### Umbralización Global vs Adaptativa

| Característica | Global | Adaptativa |
|----------------|--------|------------|
| **Umbral** | Único para toda la imagen | Diferente para cada región |
| **Velocidad** | Rápida | Más lenta |
| **Iluminación variable** | No funciona bien | Funciona excelente |
| **Uso típico** | Iluminación uniforme | Documentos escaneados, sombras |

### Método de Otsu

**Ventajas:**
- Automático (no requiere especificar umbral)
- Óptimo para imágenes bimodales
- Robusto con preprocesamiento

**Limitaciones:**
- Asume distribución bimodal
- Sensible al ruido
- No funciona bien con iluminación no uniforme

## 📊 Cuándo usar cada método

1. **Umbralización Simple**
   - Iluminación controlada y uniforme
   - Cuando conoces el umbral adecuado
   - Procesamiento en tiempo real

2. **Umbralización Adaptativa**
   - Iluminación variable en la imagen
   - Documentos escaneados
   - Imágenes con sombras o degradados

3. **Método de Otsu**
   - Cuando no conoces el umbral óptimo
   - Imágenes con dos clases bien definidas (bimodales)
   - Después de aplicar filtros para reducir ruido

## 🔗 Referencias

- [OpenCV: Image Thresholding](https://docs.opencv.org/4.x/d7/d4d/tutorial_py_thresholding.html)
- [Otsu's Method](https://en.wikipedia.org/wiki/Otsu%27s_method)
- [Adaptive Thresholding](https://docs.opencv.org/4.x/d7/d1b/group__imgproc__misc.html#ga72b913f352e4a1b1b397736707afcde3)

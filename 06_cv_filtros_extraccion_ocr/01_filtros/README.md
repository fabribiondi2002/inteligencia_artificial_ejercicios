# 01 - Filtros de Imagen

Este módulo cubre la aplicación de diversos filtros para procesamiento y mejora de imágenes digitales.

## 📋 Contenido

### 01 - Filtro Gaussiano
**Archivo**: `01_filtro_gaussiano.py`

Aplicación de filtro gaussiano para suavizado de imágenes:
- Reducción de ruido
- Suavizado progresivo con diferentes valores de sigma
- Comparación visual de efectos

**Conceptos**:
- Distribución gaussiana
- Convolución con kernel gaussiano
- Parámetro sigma (desviación estándar)

### 02 - Filtro de Mediana
**Archivo**: `02_filtro_mediana.py`

Filtro no lineal que preserva bordes mientras elimina ruido:
- Eliminación de ruido tipo "sal y pimienta"
- Preservación de bordes
- Comparación con filtro gaussiano

**Conceptos**:
- Filtros no lineales
- Estadística de orden
- Preservación de bordes

### 03 - Filtro DoG (Difference of Gaussians)
**Archivo**: `03_filtro_dog.py`

Detección de características usando la diferencia de dos gaussianas:
- Detección de bordes y características
- Aproximación a Laplaciano de Gaussiana
- Análisis multiscala

**Conceptos**:
- Diferencia de gaussianas
- Detección de características
- Análisis de escala

### 04 - Unsharp Masking
**Archivo**: `04_filtro_unsharp_masking.py`

Técnica de mejora de nitidez y contraste:
- Aumento de nitidez
- Mejora de detalles
- Control de intensidad

**Conceptos**:
- Máscara desenfocada
- Mejora de contraste local
- Parámetros de control

### 05 - Transformada de Fourier
**Archivo**: `05_fourier.py`

Análisis de imágenes en el dominio de frecuencias:
- Transformada de Fourier 2D
- Espectro de potencia
- Filtrado en dominio de frecuencias

**Conceptos**:
- Transformada de Fourier
- Dominio de frecuencias
- Espectro de potencia

## 🔧 Requisitos

```bash
pip install opencv-python numpy matplotlib scikit-image
```

## 🚀 Uso

Ejecuta cada script desde esta carpeta:

```bash
# Filtro Gaussiano
python .\01_filtro_gaussiano.py

# Filtro de Mediana
python .\02_filtro_mediana.py

# Filtro DoG
python .\03_filtro_dog.py

# Unsharp Masking
python .\04_filtro_unsharp_masking.py

# Transformada de Fourier
python .\05_fourier.py
```

## 📚 Conceptos Clave

### Convolución
Operación matemática que aplica un kernel a cada píxel y sus vecinos.

### Kernel (Elemento Estructurante)
Matriz pequeña que define cómo se procesan los píxeles vecinos.

### Dominio Espacial vs Dominio de Frecuencias
- **Espacial**: Operaciones directas sobre píxeles
- **Frecuencias**: Análisis mediante transformadas (Fourier)

### Ruido
Variaciones aleatorias en los valores de píxeles que degradan la imagen.

## 💡 Consejos

1. Comienza con el filtro gaussiano para entender los conceptos básicos
2. Experimenta con diferentes tamaños de kernel y parámetros
3. Visualiza los resultados intermedios con matplotlib
4. Prueba los filtros con tus propias imágenes
5. Compara los resultados de diferentes filtros en la misma imagen

## 📖 Referencias

- [OpenCV - Image Filtering](https://docs.opencv.org/4.x/d4/d13/tutorial_py_filtering.html)
- [scikit-image - Filters](https://scikit-image.org/docs/stable/api/skimage.filters.html)
- [NumPy - Convolution](https://numpy.org/doc/stable/reference/generated/numpy.convolve.html)
- [Fourier Transform Basics](https://en.wikipedia.org/wiki/Fourier_transform)

---

**Última actualización**: Octubre 2025

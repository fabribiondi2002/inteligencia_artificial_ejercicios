# 03 - Pirámides de Imágenes

Este módulo cubre técnicas de multiresolución para análisis jerárquico de imágenes, incluyendo pirámides gaussianas, laplacianas y fusión de imágenes.

## 📋 Contenido

### 01 - Pirámides Gaussianas
**Archivo**: `01_piramides.py`

Construcción de pirámides gaussianas para análisis multiresolución:
- Reducción progresiva de resolución (downsampling)
- Aumento de resolución (upsampling)
- Redimensionamiento con escala arbitraria
- Visualización de diferentes niveles

**Conceptos**:
- Pirámides gaussianas
- Downsampling y upsampling
- Análisis multiresolución
- Interpolación

### 02 - Pirámides Laplacianas
**Archivo**: `02_paramide_laplaciana.py`

Extracción de detalles en diferentes escalas usando pirámides laplacianas:
- Cálculo de diferencias entre niveles
- Reconstrucción de imagen original
- Análisis de detalles por escala

**Conceptos**:
- Pirámides laplacianas
- Diferencia de gaussianas
- Extracción de detalles
- Compresión de imágenes

### 03 - Fusión de Imágenes
**Archivo**: `03_fusion_img.py`

Combinación de múltiples imágenes usando pirámides:
- Creación de máscaras
- Fusión con pirámides gaussianas y laplacianas
- Blending suave entre imágenes
- Reconstrucción de imagen fusionada

**Conceptos**:
- Fusión de imágenes
- Blending
- Máscaras de fusión
- Reconstrucción multiresolución

## 🔧 Requisitos

```bash
pip install opencv-python numpy matplotlib
```

## 🚀 Uso

Ejecuta cada script desde esta carpeta:

```bash
# Pirámides Gaussianas
python .\01_piramides.py

# Pirámides Laplacianas
python .\02_paramide_laplaciana.py

# Fusión de Imágenes
python .\03_fusion_img.py
```

## 📚 Conceptos Clave

### Pirámide Gaussiana
Secuencia de imágenes donde cada nivel es una versión suavizada y reducida del anterior.

**Proceso**:
1. Aplicar filtro gaussiano
2. Reducir resolución (cada píxel se toma cada 2 posiciones)
3. Repetir para crear niveles

### Pirámide Laplaciana
Secuencia de imágenes que contiene los detalles (diferencias) entre niveles de la pirámide gaussiana.

**Proceso**:
1. Tomar dos niveles consecutivos de la pirámide gaussiana
2. Expandir el nivel inferior
3. Calcular la diferencia

### Downsampling
Reducción de resolución eliminando píxeles alternos.

### Upsampling
Aumento de resolución insertando píxeles (generalmente ceros) entre píxeles existentes.

### Blending
Combinación suave de dos imágenes usando una máscara de transición.

## 💡 Consejos

1. Comienza con pirámides gaussianas para entender el concepto básico
2. Experimenta con diferentes números de niveles
3. Visualiza cada nivel de la pirámide para entender la progresión
4. Para fusión, crea máscaras claras que definan la región de transición
5. Prueba con imágenes de tamaños similares para mejores resultados

## 📖 Referencias

- [OpenCV - Image Pyramids](https://docs.opencv.org/4.x/dc/d52/tutorial_py_image_pyramids.html)
- [Image Pyramids - Wikipedia](https://en.wikipedia.org/wiki/Pyramid_(image_processing))
- [Laplacian Pyramid](https://en.wikipedia.org/wiki/Laplacian_pyramid)
- [Image Blending with Pyramids](https://docs.opencv.org/4.x/dc/d52/tutorial_py_image_pyramids.html)

## 📝 Notas Importantes

- Las pirámides son fundamentales en visión por computadora moderna
- Se usan en detección de características, reconocimiento de objetos y más
- La fusión de imágenes con pirámides produce transiciones suaves
- El número de niveles depende del tamaño de la imagen y la aplicación
- Las pirámides laplacianas son útiles para compresión de imágenes

## 🎯 Aplicaciones Prácticas

- **Reconocimiento de objetos**: Búsqueda a múltiples escalas
- **Fusión de imágenes**: Combinación de fotos con diferentes exposiciones
- **Compresión**: Almacenamiento eficiente de detalles
- **Análisis de texturas**: Extracción de características a diferentes escalas
- **Panoramas**: Fusión de múltiples imágenes para crear panoramas

---

**Última actualización**: Octubre 2025

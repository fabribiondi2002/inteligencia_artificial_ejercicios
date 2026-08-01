# Conversión a Escala de Grises

Este ejemplo demuestra cómo convertir imágenes a color a escala de grises utilizando OpenCV.

## 📝 Descripción

La conversión a escala de grises es un paso fundamental en el procesamiento de imágenes, reduciendo la complejidad de la información de color (3 canales) a un solo canal de intensidad.

## 🎯 Objetivo

Convertir una imagen RGB/BGR a escala de grises utilizando el **método de luminosidad**, que pondera los canales de color según la sensibilidad del ojo humano:

```
Gray = 0.299 × R + 0.587 × G + 0.114 × B
```

## 📋 Archivo

- **`gray_scale.py`**: Script principal que realiza la conversión

## 🔧 Requisitos

```bash
pip install opencv-python
```

## 🚀 Uso

```bash
python gray_scale.py
```

## 📊 Funcionalidad

1. **Carga de imagen**: Lee la imagen en color desde el archivo
2. **Conversión**: Aplica `cv2.cvtColor()` con `cv2.COLOR_BGR2GRAY`
3. **Visualización**: Muestra la imagen original y la convertida
4. **Guardado**: Exporta el resultado como `imagen_gris.jpg`

## 💡 Conceptos Clave

### Métodos de conversión a escala de grises

1. **Average (Promedio)**
   ```
   Gray = (R + G + B) / 3
   ```

2. **Weighted (Luminosidad)** ✅ *Usado en este ejemplo*
   ```
   Gray = 0.299*R + 0.587*G + 0.114*B
   ```
   - Más verde porque el ojo humano es más sensible al verde
   - Método utilizado por `cv2.cvtColor()`

3. **Lightness**
   ```
   Gray = (max(R,G,B) + min(R,G,B)) / 2
   ```

## 📌 Notas

- El método de luminosidad produce resultados más naturales que el promedio simple
- Las imágenes en escala de grises ocupan aproximadamente 1/3 del espacio de las imágenes a color
- Es un paso previo común para muchas operaciones de procesamiento de imágenes

## 🔗 Referencias

- [Documentación cv2.cvtColor()](https://docs.opencv.org/4.x/d8/d01/group__imgproc__color__conversions.html)
- [Grayscale Conversion Methods](https://en.wikipedia.org/wiki/Grayscale#Converting_color_to_grayscale)

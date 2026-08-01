import os

import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt

# Ruta de la imagen
ruta_imagen = "../img/water_coins.jpg"

# Verificar que el archivo existe
if not os.path.exists(ruta_imagen):
    print(f"Error: No se encuentra el archivo {ruta_imagen}")
    exit()

# Cargar la imagen
img = cv.imread(ruta_imagen)
if img is None:
    print(f"Error: No se pudo cargar la imagen desde {ruta_imagen}")
    exit()

# Convertir la imagen a escala de grises
gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

# Aplicar la umbralización inversa utilizando el método de Otsu
ret, thresh = cv.threshold(gray, 0, 255, cv.THRESH_BINARY_INV + cv.THRESH_OTSU)

# Eliminación de ruido mediante apertura morfológica
kernel = np.ones((3, 3), np.uint8)
opening = cv.morphologyEx(thresh, cv.MORPH_OPEN, kernel, iterations=2)

# Definir el área de fondo seguro mediante la dilatación
sure_bg = cv.dilate(opening, kernel, iterations=3)

# Encontrar el área de primer plano seguro usando la transformada de distancia
dist_transform = cv.distanceTransform(opening, cv.DIST_L2, 5)

# Aplicar umbralización para obtener el primer plano seguro
ret, sure_fg = cv.threshold(dist_transform, 0.7 * dist_transform.max(), 255, 0)
sure_fg = np.uint8(sure_fg)

# Encontrar la región desconocida (área entre el fondo y el primer plano)
unknown = cv.subtract(sure_bg, sure_fg)

# Etiquetar los marcadores para las regiones conectadas
ret, markers = cv.connectedComponents(sure_fg)

# Incrementar todas las etiquetas en uno para asegurarse de que el fondo seguro no sea 0, sino 1
markers = markers + 1

# Marcar la región desconocida con 0
markers[unknown == 255] = 0

# Aplicar el algoritmo Watershed
markers = cv.watershed(img, markers)

# Marcar los bordes (donde watershed identifica las fronteras) en color rojo
img_resultado = img.copy()
img_resultado[markers == -1] = [255, 0, 0]

# Preparar las imágenes para mostrar con Matplotlib
# Cada tupla contiene: (imagen, título descriptivo)
imagenes = [
    (gray, "1. Escala de grises"),
    (thresh, "2. Umbralización Otsu"),
    (opening, "3. Apertura morfológica"),
    (sure_bg, "4. Fondo seguro (dilatación)"),
    (dist_transform, "5. Transformada de distancia"),
    (sure_fg, "6. Primer plano seguro"),
    (unknown, "7. Región desconocida"),
    (img_resultado, "8. Resultado Final Watershed"),
]

# Mostrar las imágenes en una figura utilizando subplots (4 arriba, 4 abajo)
print("\n=== ALGORITMO WATERSHED ===")
print(f"Imagen procesada: {ruta_imagen}")
print(f"N\u00famero de objetos segmentados: {ret - 1}")  # -1 porque el fondo es el marcador 1
print("Mostrando proceso paso a paso...\n")

plt.figure(figsize=(14, 8))  # Tamaño de la figura
for i, (img_step, title) in enumerate(imagenes, 1):
    plt.subplot(2, 4, i)  # 2 filas, 4 columnas
    if len(img_step.shape) == 2:  # Imágenes en escala de grises
        plt.imshow(img_step, cmap="gray")
    else:  # Imágenes en BGR (color)
        plt.imshow(cv.cvtColor(img_step, cv.COLOR_BGR2RGB))
    plt.title(title, fontsize=10)
    plt.axis("off")

plt.suptitle("Algoritmo Watershed - Segmentaci\u00f3n de Objetos", fontsize=14, fontweight="bold")
plt.tight_layout()
print("Cerrando la ventana se finalizar\u00e1 el programa.")
plt.show()

"""
Umbralización Adaptativa (Adaptive Thresholding).

Este script demuestra la umbralización adaptativa, que calcula el umbral para
regiones pequeñas de la imagen. Es útil en imágenes con condiciones de
iluminación variables.
"""

import os

import cv2 as cv
from matplotlib import pyplot as plt


def main():
    # Ruta de la imagen
    ruta_imagen = "../img/02_escaneado.png"

    # Verificar que el archivo existe
    if not os.path.exists(ruta_imagen):
        print(f"Error: No se encontró la imagen en {ruta_imagen}")
        return

    # Cargar la imagen en escala de grises
    img = cv.imread(ruta_imagen, cv.IMREAD_GRAYSCALE)

    if img is None:
        print(f"Error: No se pudo cargar la imagen desde {ruta_imagen}")
        return

    print(f"Imagen cargada: {img.shape[1]}x{img.shape[0]} píxeles")

    # Aplicar filtro de mediana para reducir el ruido
    img = cv.medianBlur(img, 5)
    print("Filtro de mediana aplicado (kernel 5x5)")

    # Umbralización global (simple)
    umbral_global = 127
    ret, th1 = cv.threshold(img, umbral_global, 255, cv.THRESH_BINARY)
    print(f"Umbralización global aplicada (umbral={umbral_global})")

    # Umbralización adaptativa - Media
    # El umbral se calcula como la media de los vecinos en un área de 11x11 píxeles menos 2
    th2 = cv.adaptiveThreshold(
        img,
        255,
        cv.ADAPTIVE_THRESH_MEAN_C,
        cv.THRESH_BINARY,
        blockSize=11,  # Tamaño del área de vecindad
        C=2,  # Constante que se resta de la media
    )
    print("Umbralización adaptativa MEAN aplicada (blockSize=11, C=2)")

    # Umbralización adaptativa - Gaussiana
    # El umbral se calcula como la suma ponderada gaussiana de los vecinos menos 2
    th3 = cv.adaptiveThreshold(
        img,
        255,
        cv.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv.THRESH_BINARY,
        blockSize=11,  # Tamaño del área de vecindad
        C=2,  # Constante que se resta de la suma ponderada
    )
    print("Umbralización adaptativa GAUSSIAN aplicada (blockSize=11, C=2)")

    # Títulos y lista de imágenes
    titles = [
        "Imagen Original (con filtro)",
        f"Umbralización Global (umbral={umbral_global})",
        "Umbralización Adaptativa (Media)",
        "Umbralización Adaptativa (Gaussiana)",
    ]
    images = [img, th1, th2, th3]

    # Crear figura con subplots
    plt.figure(figsize=(14, 8))

    for i in range(4):
        plt.subplot(2, 2, i + 1)
        plt.imshow(images[i], "gray")
        plt.title(titles[i], fontsize=10)
        plt.xticks([])
        plt.yticks([])

    plt.suptitle(
        "Comparación de Umbralización Global vs Adaptativa", fontsize=14, fontweight="bold"
    )
    plt.tight_layout()
    plt.show()

    print("Visualización completada.")


if __name__ == "__main__":
    main()

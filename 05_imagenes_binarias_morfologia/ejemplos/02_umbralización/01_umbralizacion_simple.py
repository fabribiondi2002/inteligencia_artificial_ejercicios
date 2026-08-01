"""
Umbralización Simple (Thresholding).

Este script demuestra los diferentes tipos de umbralización global disponibles
en OpenCV. La umbralización convierte una imagen en escala de grises a binaria
usando un valor de umbral fijo.
"""

import os

import cv2 as cv
from matplotlib import pyplot as plt


def main():
    # Ruta de la imagen
    ruta_imagen = "../img/01_lapices.jpg"

    # Verificar que el archivo existe
    if not os.path.exists(ruta_imagen):
        print(f"Error: No se encontró la imagen en {ruta_imagen}")
        return

    # Cargar la imagen en escala de grises
    img = cv.imread(ruta_imagen, cv.IMREAD_GRAYSCALE)

    if img is None:
        print(f"Error: No se pudo cargar la imagen desde {ruta_imagen}")
        return

    # Valor de umbral y valor máximo
    umbral = 127
    valor_max = 255

    print(f"Aplicando umbralización con umbral={umbral} y valor_max={valor_max}")

    # Aplicar diferentes tipos de umbralización
    ret, thresh1 = cv.threshold(img, umbral, valor_max, cv.THRESH_BINARY)
    ret, thresh2 = cv.threshold(img, umbral, valor_max, cv.THRESH_BINARY_INV)
    ret, thresh3 = cv.threshold(img, umbral, valor_max, cv.THRESH_TRUNC)
    ret, thresh4 = cv.threshold(img, umbral, valor_max, cv.THRESH_TOZERO)
    ret, thresh5 = cv.threshold(img, umbral, valor_max, cv.THRESH_TOZERO_INV)

    # Títulos y lista de imágenes para visualización
    titles = [
        "Original (Escala de Grises)",
        "BINARY (>umbral=255)",
        "BINARY_INV (<umbral=255)",
        "TRUNC (>umbral=umbral)",
        "TOZERO (>umbral=original)",
        "TOZERO_INV (<umbral=original)",
    ]
    images = [img, thresh1, thresh2, thresh3, thresh4, thresh5]

    # Crear figura con subplots
    plt.figure(figsize=(15, 8))

    for i in range(6):
        plt.subplot(2, 3, i + 1)
        plt.imshow(images[i], "gray", vmin=0, vmax=255)
        plt.title(titles[i], fontsize=10)
        plt.xticks([])
        plt.yticks([])

    plt.suptitle("Tipos de Umbralización Simple", fontsize=14, fontweight="bold")
    plt.tight_layout()
    plt.show()

    print("Visualización completada.")


if __name__ == "__main__":
    main()

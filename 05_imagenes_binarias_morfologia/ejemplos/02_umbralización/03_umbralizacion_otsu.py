"""
Umbralización de Otsu.

Este script demuestra el método de Otsu para umbralización automática.
El algoritmo de Otsu calcula automáticamente el valor óptimo del umbral
para separar el fondo del primer plano basándose en el histograma de la imagen.
"""

import os

import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt


def main():
    # Ruta de la imagen
    ruta_imagen = "../img/04_noisy.png"

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

    # 1. Umbralización global simple
    umbral_manual = 127
    ret1, th1 = cv.threshold(img, umbral_manual, 255, cv.THRESH_BINARY)
    print(f"Umbralización global: umbral={umbral_manual}")

    # 2. Umbralización de Otsu (sin filtrado previo)
    ret2, th2 = cv.threshold(img, 0, 255, cv.THRESH_BINARY + cv.THRESH_OTSU)
    print(f"Umbralización de Otsu (imagen ruidosa): umbral calculado={ret2:.2f}")

    # 3. Filtrado Gaussiano + Umbralización de Otsu
    # El filtro Gaussiano reduce el ruido antes de aplicar Otsu
    blur = cv.GaussianBlur(img, (5, 5), 0)
    ret3, th3 = cv.threshold(blur, 0, 255, cv.THRESH_BINARY + cv.THRESH_OTSU)
    print(f"Umbralización de Otsu (imagen filtrada): umbral calculado={ret3:.2f}")

    # Preparar imágenes para visualización
    # Formato: [imagen, histograma, resultado_umbralización]
    images = [img, 0, th1, img, 0, th2, blur, 0, th3]

    titles = [
        "Imagen Original Ruidosa",
        "Histograma",
        f"Umbralización Global (v={umbral_manual})",
        "Imagen Original Ruidosa",
        "Histograma",
        f"Método de Otsu (v={ret2:.1f})",
        "Imagen con Filtro Gaussiano",
        "Histograma",
        f"Método de Otsu (v={ret3:.1f})",
    ]

    # Crear figura con subplots
    plt.figure(figsize=(16, 10))

    for i in range(3):
        # Mostrar imagen original/filtrada
        plt.subplot(3, 3, i * 3 + 1)
        plt.imshow(images[i * 3], "gray")
        plt.title(titles[i * 3], fontsize=10)
        plt.xticks([])
        plt.yticks([])

        # Mostrar histograma
        plt.subplot(3, 3, i * 3 + 2)
        plt.hist(images[i * 3].ravel(), bins=256, range=[0, 256])
        plt.title(titles[i * 3 + 1], fontsize=10)
        plt.xlabel("Valor de píxel")
        plt.ylabel("Frecuencia")
        plt.xticks([])
        plt.yticks([])

        # Mostrar resultado de umbralización
        plt.subplot(3, 3, i * 3 + 3)
        plt.imshow(images[i * 3 + 2], "gray")
        plt.title(titles[i * 3 + 2], fontsize=10)
        plt.xticks([])
        plt.yticks([])

    plt.suptitle(
        "Comparación: Umbralización Global vs Método de Otsu", fontsize=14, fontweight="bold"
    )
    plt.tight_layout()
    plt.show()

    print("\nVisualización completada.")
    print(f"\nConclusión:")
    print(f"  - Umbral manual: {umbral_manual}")
    print(f"  - Otsu (con ruido): {ret2:.2f}")
    print(f"  - Otsu (filtrada): {ret3:.2f}")


if __name__ == "__main__":
    main()

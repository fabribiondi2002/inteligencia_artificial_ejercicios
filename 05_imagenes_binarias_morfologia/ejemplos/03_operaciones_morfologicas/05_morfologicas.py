"""
Operaciones Morfológicas.

Este script demuestra las operaciones morfológicas básicas aplicadas a imágenes binarias:
- Erosión: Reduce el tamaño de objetos blancos
- Dilatación: Aumenta el tamaño de objetos blancos
- Apertura: Erosión seguida de dilatación (elimina ruido pequeño)
- Cierre: Dilatación seguida de erosión (rellena huecos pequeños)
- Gradiente: Diferencia entre dilatación y erosión (detecta bordes)
"""

import os

import cv2
import matplotlib.pyplot as plt
import numpy as np


def main():
    # Ruta de la imagen
    ruta_imagen = "../img/09_cebra.jpeg"

    # Verificar que el archivo existe
    if not os.path.exists(ruta_imagen):
        print(f"Error: No se encontró la imagen en {ruta_imagen}")
        return

    # Cargar la imagen en escala de grises
    img = cv2.imread(ruta_imagen, cv2.IMREAD_GRAYSCALE)

    if img is None:
        print(f"Error: No se pudo cargar la imagen desde {ruta_imagen}")
        return

    print(f"Imagen cargada: {img.shape[1]}x{img.shape[0]} píxeles")

    # Aplicar umbralización para obtener imagen binaria
    umbral = 127
    _, binary_img = cv2.threshold(img, umbral, 255, cv2.THRESH_BINARY)
    print(f"Umbralización aplicada (umbral={umbral})")

    # Definir elemento estructurante (kernel)
    kernel_size = 5
    kernel = np.ones((kernel_size, kernel_size), np.uint8)
    print(f"Kernel: {kernel_size}x{kernel_size}")

    print("\nAplicando operaciones morfológicas...")

    # 1. Erosión
    # Reduce el tamaño de los objetos blancos, elimina píxeles en los bordes
    erosion = cv2.erode(binary_img, kernel, iterations=1)
    print("  ✓ Erosión")

    # 2. Dilatación
    # Aumenta el tamaño de los objetos blancos, añade píxeles en los bordes
    dilation = cv2.dilate(binary_img, kernel, iterations=1)
    print("  ✓ Dilatación")

    # 3. Apertura (Opening)
    # Erosión seguida de dilatación
    # Útil para eliminar ruido pequeño manteniendo objetos grandes
    opening = cv2.morphologyEx(binary_img, cv2.MORPH_OPEN, kernel)
    print("  ✓ Apertura (erosión + dilatación)")

    # 4. Cierre (Closing)
    # Dilatación seguida de erosión
    # Útil para rellenar pequeños huecos en objetos
    closing = cv2.morphologyEx(binary_img, cv2.MORPH_CLOSE, kernel)
    print("  ✓ Cierre (dilatación + erosión)")

    # 5. Gradiente Morfológico
    # Diferencia entre dilatación y erosión
    # Útil para detectar los contornos de los objetos
    gradient = cv2.morphologyEx(binary_img, cv2.MORPH_GRADIENT, kernel)
    print("  ✓ Gradiente morfológico")

    # Visualizar resultados
    plt.figure(figsize=(15, 10))

    images = [binary_img, erosion, dilation, opening, closing, gradient]
    titles = [
        "Imagen Binaria Original",
        "Erosión\n(reduce objetos)",
        "Dilatación\n(agranda objetos)",
        "Apertura\n(elimina ruido)",
        "Cierre\n(rellena huecos)",
        "Gradiente\n(detecta bordes)",
    ]

    for i, (image, title) in enumerate(zip(images, titles)):
        plt.subplot(2, 3, i + 1)
        plt.imshow(image, cmap="gray")
        plt.title(title, fontsize=11, fontweight="bold")
        plt.axis("off")

    plt.suptitle(
        f"Operaciones Morfológicas (kernel {kernel_size}x{kernel_size})",
        fontsize=14,
        fontweight="bold",
    )
    plt.tight_layout()
    plt.show()

    print("\nVisualización completada.")
    print("\nResumen:")
    print("  - Erosión: Reduce objetos, elimina ruido pequeño")
    print("  - Dilatación: Agranda objetos, conecta regiones cercanas")
    print("  - Apertura: Elimina ruido sin cambiar mucho el tamaño")
    print("  - Cierre: Rellena huecos sin cambiar mucho el tamaño")
    print("  - Gradiente: Resalta los contornos de los objetos")


if __name__ == "__main__":
    main()

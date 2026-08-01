"""
Transformación de Rotación.

Este script demuestra cómo rotar una imagen alrededor de un punto (centro)
usando una matriz de transformación afín 2D.
"""

import os

import cv2
import numpy as np


def main():
    # Ruta de la imagen
    ruta_imagen = "../img/05_messi.jpg"

    # Verificar que el archivo existe
    if not os.path.exists(ruta_imagen):
        print(f"Error: No se encontró la imagen en {ruta_imagen}")
        return

    # Cargar la imagen
    img = cv2.imread(ruta_imagen)

    if img is None:
        print(f"Error: No se pudo cargar la imagen desde {ruta_imagen}")
        return

    print(f"Imagen cargada: {img.shape[1]}x{img.shape[0]} píxeles")

    # Dimensiones de la imagen original
    height, width = img.shape[:2]

    # Parámetros de rotación
    angle = 30  # Ángulo de rotación en grados (sentido antihorario)
    scale = 1.0  # Factor de escala (1.0 = sin cambio de tamaño)

    # Centro de rotación (centro de la imagen)
    center = (width // 2, height // 2)

    print(f"\nAplicando rotación:")
    print(f"  - Ángulo: {angle}° (sentido antihorario)")
    print(f"  - Centro: {center}")
    print(f"  - Escala: {scale}")

    # Obtener matriz de rotación 2D
    # cv2.getRotationMatrix2D(center, angle, scale) retorna matriz 2x3
    M = cv2.getRotationMatrix2D(center, angle, scale)

    # Aplicar la transformación de rotación
    rotated_img = cv2.warpAffine(img, M, (width, height))

    # Mostrar imágenes
    cv2.imshow("Imagen Original", img)
    cv2.imshow("Imagen Rotada", rotated_img)

    print("\nPresiona cualquier tecla para cerrar las ventanas...")
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    print("Operación completada.")


if __name__ == "__main__":
    main()

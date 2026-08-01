"""
Transformación de Traslación.

Este script demuestra cómo trasladar (desplazar) una imagen en el espacio 2D
usando una matriz de transformación afín.
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

    # Definir desplazamiento (tx, ty)
    tx = 200  # Desplazamiento en x (píxeles hacia la derecha)
    ty = 100  # Desplazamiento en y (píxeles hacia abajo)

    # Matriz de traslación 2x3
    # Formato: [[1, 0, tx],
    #           [0, 1, ty]]
    M = np.float32([[1, 0, tx], [0, 1, ty]])

    print(f"\nAplicando traslación:")
    print(f"  - Desplazamiento en X: {tx} píxeles (derecha)")
    print(f"  - Desplazamiento en Y: {ty} píxeles (abajo)")

    # Aplicar transformación de traslación
    translated_img = cv2.warpAffine(img, M, (width, height))

    # Mostrar imágenes
    cv2.imshow("Imagen Original", img)
    cv2.imshow("Imagen Trasladada", translated_img)

    print("\nPresiona cualquier tecla para cerrar las ventanas...")
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    print("Operación completada.")


if __name__ == "__main__":
    main()

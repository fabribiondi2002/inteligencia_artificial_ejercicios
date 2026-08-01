"""
Conversión de imágenes a color a escala de grises.

Este script demuestra cómo convertir una imagen a color (RGB/BGR) a escala de grises
utilizando el método de luminosidad, que pondera los canales RGB considerando la
sensibilidad del ojo humano: 0.299*R + 0.587*G + 0.114*B
"""

import os

import cv2


def main():
    # Ruta de la imagen de entrada
    ruta_imagen = "../img/01_lapices.jpg"

    # Verificar que la imagen existe
    if not os.path.exists(ruta_imagen):
        print(f"Error: No se encontró la imagen en {ruta_imagen}")
        return

    # Cargar imagen en color desde el archivo
    img_color = cv2.imread(ruta_imagen)

    if img_color is None:
        print(f"Error: No se pudo cargar la imagen desde {ruta_imagen}")
        return

    print(f"Imagen cargada: {img_color.shape[1]}x{img_color.shape[0]} píxeles")
    cv2.imshow("Imagen Original", img_color)

    # Convertir la imagen a escala de grises usando el método Luminosity
    # Este método pondera los canales BGR según la percepción humana
    img_gray = cv2.cvtColor(img_color, cv2.COLOR_BGR2GRAY)

    print(f"Imagen convertida a escala de grises: {img_gray.shape[1]}x{img_gray.shape[0]} píxeles")

    # Guardar y mostrar la imagen en escala de grises
    nombre_salida = "imagen_gris.jpg"
    cv2.imwrite(nombre_salida, img_gray)
    print(f"Imagen guardada como: {nombre_salida}")

    cv2.imshow("Imagen en Escala de Grises", img_gray)

    print("\nPresiona cualquier tecla para cerrar las ventanas...")
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()

"""
Transformación de Escalado (Redimensionamiento).

Este script demuestra diferentes métodos de interpolación para redimensionar imágenes.
Cada método tiene ventajas específicas según el caso de uso (ampliación vs reducción).
"""

import os

import cv2
import matplotlib.pyplot as plt


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

    # Dimensiones de la imagen original
    height, width = img.shape[:2]
    print(f"Imagen original: {width}x{height} píxeles")

    # Nuevas dimensiones (duplicar tamaño)
    factor_escala = 2
    nuevo_ancho = width * factor_escala
    nueva_altura = height * factor_escala

    print(f"Imagen redimensionada: {nuevo_ancho}x{nueva_altura} píxeles")
    print(f"Factor de escala: {factor_escala}x\n")

    # Métodos de interpolación disponibles
    interpolations = [
        cv2.INTER_NEAREST,
        cv2.INTER_LINEAR,
        cv2.INTER_CUBIC,
        cv2.INTER_AREA,
        cv2.INTER_LANCZOS4,
    ]

    # Nombres descriptivos de los métodos
    interp_names = [
        "INTER_NEAREST\n(Vecino más cercano)",
        "INTER_LINEAR\n(Bilineal)",
        "INTER_CUBIC\n(Bicúbica)",
        "INTER_AREA\n(Área)",
        "INTER_LANCZOS4\n(Lanczos 4x4)",
    ]

    # Descripción breve de cada método
    interp_descriptions = [
        "Rápido, resultados pixelados",
        "Bueno, velocidad media",
        "Mejor calidad, más lento",
        "Mejor para reducir tamaño",
        "Mejor calidad, muy lento",
    ]

    # Crear figura de Matplotlib
    plt.figure(figsize=(16, 10))

    print("Aplicando diferentes métodos de interpolación:")

    # Iterar sobre cada método de interpolación
    for i, (interp, name, desc) in enumerate(
        zip(interpolations, interp_names, interp_descriptions)
    ):
        print(f"  {i+1}. {name.split(chr(10))[0]}: {desc}")

        # Redimensionar la imagen con el método actual
        resized_img = cv2.resize(img, (nuevo_ancho, nueva_altura), interpolation=interp)

        # Mostrar la imagen (convertir de BGR a RGB para matplotlib)
        plt.subplot(2, 3, i + 1)
        plt.imshow(cv2.cvtColor(resized_img, cv2.COLOR_BGR2RGB))
        plt.title(name, fontsize=11, fontweight="bold")
        plt.axis("off")

    # Mostrar imagen original en el último subplot
    plt.subplot(2, 3, 6)
    plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    plt.title(f"ORIGINAL\n({width}x{height})", fontsize=11, fontweight="bold")
    plt.axis("off")

    # Título general
    plt.suptitle(
        f"Redimensionamiento con Diferentes Métodos de Interpolación ({factor_escala}x)",
        fontsize=14,
        fontweight="bold",
    )
    plt.tight_layout()
    plt.show()

    print("\nVisualización completada.")
    print("\nRecomendaciones:")
    print("  - Para AMPLIAR: INTER_CUBIC o INTER_LANCZOS4")
    print("  - Para REDUCIR: INTER_AREA")
    print("  - Para VELOCIDAD: INTER_LINEAR o INTER_NEAREST")


if __name__ == "__main__":
    main()

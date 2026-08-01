"""
Transformación de Perspectiva.

Este script demuestra cómo corregir la perspectiva de una imagen seleccionando
4 puntos de origen y mapeándolos a 4 puntos de destino (rectángulo).
Útil para escanear documentos, corregir ángulos de cámara, etc.
"""

import os

import cv2
import matplotlib.pyplot as plt
import numpy as np


def select_points(image):
    """
    Permite al usuario seleccionar 4 puntos en la imagen haciendo clic.

    Args:
        image: Imagen sobre la cual seleccionar puntos

    Returns:
        numpy.ndarray: Array de 4 puntos (x, y) seleccionados
    """
    # Copia de la imagen para no modificar la original
    img_copy = image.copy()
    points = []

    def on_mouse_click(event, x, y, flags, param):
        """Callback para manejar clics del mouse"""
        if event == cv2.EVENT_LBUTTONDOWN and len(points) < 4:
            points.append((x, y))
            # Dibujar círculo en el punto seleccionado
            cv2.circle(img_copy, (x, y), 8, (0, 255, 0), -1)
            # Dibujar número del punto
            cv2.putText(
                img_copy,
                str(len(points)),
                (x + 10, y - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 255, 0),
                2,
            )
            cv2.imshow("Seleccionar Puntos", img_copy)

    print("\nInstrucciones:")
    print("  1. Haz clic en la esquina SUPERIOR IZQUIERDA")
    print("  2. Haz clic en la esquina SUPERIOR DERECHA")
    print("  3. Haz clic en la esquina INFERIOR DERECHA")
    print("  4. Haz clic en la esquina INFERIOR IZQUIERDA")
    print("\nEspera a seleccionar los 4 puntos...")

    cv2.imshow("Seleccionar Puntos", img_copy)
    cv2.setMouseCallback("Seleccionar Puntos", on_mouse_click)

    # Esperar hasta que se seleccionen 4 puntos
    while len(points) < 4:
        key = cv2.waitKey(10)
        # Permitir cancelar con ESC
        if key == 27:  # ESC
            print("Selección cancelada")
            cv2.destroyAllWindows()
            return None

    print(f"Puntos seleccionados: {points}")
    cv2.destroyAllWindows()
    return np.array(points, dtype=np.float32)


def main():
    # Ruta de la imagen
    ruta_imagen = "../img/06_notredame.jpg"

    # Verificar que el archivo existe
    if not os.path.exists(ruta_imagen):
        print(f"Error: No se encontró la imagen en {ruta_imagen}")
        return

    # Cargar la imagen
    image = cv2.imread(ruta_imagen)

    if image is None:
        print(f"Error: No se pudo cargar la imagen desde {ruta_imagen}")
        return

    print(f"Imagen cargada: {image.shape[1]}x{image.shape[0]} píxeles")

    # Guardar copia de la imagen original
    original_image = image.copy()

    # Seleccionar 4 puntos de origen en la imagen
    points = select_points(image)

    if points is None:
        print("Operación cancelada por el usuario")
        return

    # Definir dimensiones de la imagen de destino
    width, height = 300, 400

    # Definir puntos de destino (rectángulo)
    # Orden: superior izquierda, superior derecha, inferior derecha, inferior izquierda
    dest_points = np.array(
        [
            [0, 0],  # Superior izquierda
            [width - 1, 0],  # Superior derecha
            [width - 1, height - 1],  # Inferior derecha
            [0, height - 1],  # Inferior izquierda
        ],
        dtype=np.float32,
    )

    print(f"\nDimensiones de salida: {width}x{height} píxeles")

    # Calcular matriz de transformación de perspectiva
    matrix = cv2.getPerspectiveTransform(points, dest_points)

    print("\nMatriz de transformación calculada")

    # Aplicar la transformación de perspectiva
    warped = cv2.warpPerspective(original_image, matrix, (width, height))

    print("Transformación aplicada exitosamente")

    # Visualizar resultados con matplotlib
    plt.figure(figsize=(14, 7))

    # Imagen original con puntos seleccionados
    plt.subplot(1, 2, 1)
    img_with_points = original_image.copy()
    for i, (x, y) in enumerate(points):
        cv2.circle(img_with_points, (int(x), int(y)), 8, (0, 255, 0), -1)
        cv2.putText(
            img_with_points,
            str(i + 1),
            (int(x) + 10, int(y) - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 255, 0),
            2,
        )
    plt.imshow(cv2.cvtColor(img_with_points, cv2.COLOR_BGR2RGB))
    plt.title("Imagen Original\n(con puntos seleccionados)", fontsize=12, fontweight="bold")
    plt.axis("off")

    # Imagen transformada
    plt.subplot(1, 2, 2)
    plt.imshow(cv2.cvtColor(warped, cv2.COLOR_BGR2RGB))
    plt.title(f"Imagen Transformada\n({width}x{height})", fontsize=12, fontweight="bold")
    plt.axis("off")

    plt.suptitle("Transformación de Perspectiva", fontsize=14, fontweight="bold")
    plt.tight_layout()
    plt.show()

    print("\nVisualización completada.")


if __name__ == "__main__":
    main()

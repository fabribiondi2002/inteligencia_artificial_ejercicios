import os

import cv2
import numpy as np

# Ruta de la imagen
ruta_imagen = "../img/colores.png"

# Verificar que el archivo existe
if not os.path.exists(ruta_imagen):
    print(f"Error: No se encuentra el archivo {ruta_imagen}")
    exit()

# Cargar la imagen desde un archivo
imagen = cv2.imread(ruta_imagen)

# Definir los rangos de color amarillo en el espacio HSV
# Estos son los límites inferior y superior para detectar el color amarillo
yellowBajo = np.array([20, 100, 100], np.uint8)  # Límite inferior del amarillo
yellowAlto = np.array([30, 255, 255], np.uint8)  # Límite superior del amarillo

# Verificar si la imagen fue cargada correctamente
if imagen is not None:
    # Convertir la imagen al espacio de color HSV
    frameHSV = cv2.cvtColor(imagen, cv2.COLOR_BGR2HSV)

    # Crear la máscara para el rango del color amarillo
    maskYellow = cv2.inRange(frameHSV, yellowBajo, yellowAlto)

    # Aplicar la máscara a la imagen original para visualizar solo las áreas amarillas
    maskYellowvis = cv2.bitwise_and(imagen, imagen, mask=maskYellow)

    # Mostrar la imagen original
    cv2.imshow("Imagen original", imagen)

    # Mostrar la máscara que detecta las áreas amarillas
    cv2.imshow("Mascara Amarillo", maskYellow)

    # Mostrar la imagen con solo las áreas amarillas visibles
    cv2.imshow("Resultado con áreas amarillas", maskYellowvis)

    # Esperar a que el usuario presione una tecla para cerrar las ventanas
    cv2.waitKey(0)
    cv2.destroyAllWindows()

else:
    print(f"Error: No se pudo cargar la imagen desde {ruta_imagen}")

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

# Definimos los rangos de color rojo en el espacio HSV
# Primer rango para tonos rojos (rojo más puro)
redBajo1 = np.array([0, 100, 20], np.uint8)  # Límite inferior del rojo (primer rango)
redAlto1 = np.array([8, 255, 255], np.uint8)  # Límite superior del rojo (primer rango)

# Segundo rango para tonos rojos (cercanos a 360 grados)
redBajo2 = np.array([175, 100, 20], np.uint8)  # Límite inferior del rojo (segundo rango)
redAlto2 = np.array([179, 255, 255], np.uint8)  # Límite superior del rojo (segundo rango)

# Verificar si la imagen fue cargada correctamente
if imagen is not None:
    # Convertimos la imagen al espacio de color HSV
    frameHSV = cv2.cvtColor(imagen, cv2.COLOR_BGR2HSV)

    # Creamos dos máscaras para los dos rangos de color rojo
    maskRed1 = cv2.inRange(frameHSV, redBajo1, redAlto1)  # Máscara para el primer rango de rojo
    maskRed2 = cv2.inRange(frameHSV, redBajo2, redAlto2)  # Máscara para el segundo rango de rojo

    # Combinar las dos máscaras de los rangos rojos
    maskRed = cv2.add(
        maskRed1, maskRed2
    )  # Suma las dos máscaras para cubrir todo el rango del color rojo

    # Aplicar la máscara a la imagen original para visualizar solo las áreas rojas
    maskRedvis = cv2.bitwise_and(imagen, imagen, mask=maskRed)

    # Mostrar la imagen original
    cv2.imshow("Imagen original", imagen)

    # Mostrar la máscara que detecta las áreas rojas
    cv2.imshow("Mascara Rojo", maskRed)

    # Mostrar la imagen con solo las áreas rojas visibles
    cv2.imshow("Resultado con áreas rojas", maskRedvis)

    # Esperar a que el usuario presione una tecla para cerrar las ventanas
    cv2.waitKey(0)
    cv2.destroyAllWindows()

else:
    print(f"Error: No se pudo cargar la imagen desde {ruta_imagen}")

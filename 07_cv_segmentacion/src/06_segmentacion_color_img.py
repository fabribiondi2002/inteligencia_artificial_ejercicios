import os

import cv2
import imutils
import numpy as np

# Definir los rangos de color rojo en el espacio HSV
rojoBajo1 = np.array([0, 140, 90], np.uint8)
rojoAlto1 = np.array([8, 255, 255], np.uint8)
rojoBajo2 = np.array([160, 140, 90], np.uint8)
rojoAlto2 = np.array([180, 255, 255], np.uint8)

# Ruta de la imagen
ruta_imagen = "../img/rosas.jpeg"

# Verificar que el archivo existe
if not os.path.exists(ruta_imagen):
    print(f"Error: No se encuentra el archivo {ruta_imagen}")
    exit()

# Leer y redimensionar la imagen
image = cv2.imread(ruta_imagen)
if image is None:
    print(f"Error: No se pudo cargar la imagen desde {ruta_imagen}")
    exit()

image = imutils.resize(image, width=640)

# Convertir la imagen a diferentes espacios de color
# 1. Convertir a escala de grises y luego de vuelta a BGR (para combinar después)
imageGray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
imageGray = cv2.cvtColor(imageGray, cv2.COLOR_GRAY2BGR)
# 2. Convertir a espacio HSV para detección de color
imageHSV = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

# Detectar el color rojo en la imagen
maskRojo1 = cv2.inRange(imageHSV, rojoBajo1, rojoAlto1)
maskRojo2 = cv2.inRange(imageHSV, rojoBajo2, rojoAlto2)
mask = cv2.add(maskRojo1, maskRojo2)
# Aplicar filtro mediano para suavizar la máscara y eliminar ruido
mask = cv2.medianBlur(mask, 7)
# Extraer solo las áreas rojas de la imagen original
redDetected = cv2.bitwise_and(image, image, mask=mask)

# Crear el fondo en escala de grises
# Invertir la máscara para obtener todo excepto las áreas rojas
invMask = cv2.bitwise_not(mask)
# Aplicar la máscara invertida a la imagen en grises
bgGray = cv2.bitwise_and(imageGray, imageGray, mask=invMask)

# Combinar el fondo en grises con las áreas rojas en color
finalImage = cv2.add(bgGray, redDetected)

# Visualización de resultados
cv2.imshow("Imagen Original", image)
cv2.imshow("Resultado: Rojo resaltado con fondo en grises", finalImage)
print("Presiona cualquier tecla para cerrar las ventanas...")
cv2.waitKey(0)
cv2.destroyAllWindows()

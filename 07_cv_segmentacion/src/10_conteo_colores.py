import os

import cv2
import numpy as np


def dibujarContorno(contornos, color):
    """Dibuja contornos y numera cada objeto detectado.

    Args:
        contornos: Lista de contornos detectados
        color: Color en formato BGR para dibujar los contornos
    """
    for i, c in enumerate(contornos):
        M = cv2.moments(c)
        # CORRECCIÓN: Cambiar == por = (asignación, no comparación)
        if M["m00"] == 0:
            M["m00"] = 1
        x = int(M["m10"] / M["m00"])
        y = int(M["m01"] / M["m00"])
        cv2.drawContours(imagen, [c], 0, color, 2)
        cv2.putText(imagen, str(i + 1), (x - 10, y + 10), 1, 2, (0, 0, 0), 2)


# Definir los rangos de color en el espacio HSV para cada color
amarilloBajo = np.array([20, 100, 20], np.uint8)
amarilloAlto = np.array([32, 255, 255], np.uint8)

violetaBajo = np.array([130, 100, 20], np.uint8)
violetaAlto = np.array([145, 255, 255], np.uint8)

verdeBajo = np.array([36, 100, 20], np.uint8)
verdeAlto = np.array([70, 255, 255], np.uint8)

rojoBajo1 = np.array([0, 100, 20], np.uint8)
rojoAlto1 = np.array([10, 255, 255], np.uint8)
rojoBajo2 = np.array([175, 100, 20], np.uint8)
rojoAlto2 = np.array([180, 255, 255], np.uint8)

# Ruta de la imagen
ruta_imagen = "../img/lunares.png"

# Verificar que el archivo existe
if not os.path.exists(ruta_imagen):
    print(f"Error: No se encuentra el archivo {ruta_imagen}")
    exit()

# Cargar la imagen
imagen = cv2.imread(ruta_imagen)
if imagen is None:
    print(f"Error: No se pudo cargar la imagen desde {ruta_imagen}")
    exit()

# Convertir la imagen al espacio de color HSV
imagenHSV = cv2.cvtColor(imagen, cv2.COLOR_BGR2HSV)

# Detectar colores creando máscaras para cada rango de color
maskAmarillo = cv2.inRange(imagenHSV, amarilloBajo, amarilloAlto)
maskVioleta = cv2.inRange(imagenHSV, violetaBajo, violetaAlto)
maskVerde = cv2.inRange(imagenHSV, verdeBajo, verdeAlto)
maskRojo1 = cv2.inRange(imagenHSV, rojoBajo1, rojoAlto1)
maskRojo2 = cv2.inRange(imagenHSV, rojoBajo2, rojoAlto2)
# Combinar las dos máscaras del color rojo
maskRojo = cv2.add(maskRojo1, maskRojo2)

# Encontrar contornos para cada color
contornosAmarillo = cv2.findContours(maskAmarillo, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0]
contornosVioleta = cv2.findContours(maskVioleta, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0]
contornosVerde = cv2.findContours(maskVerde, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0]
contornosRojo = cv2.findContours(maskRojo, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0]

# Dibujar y numerar los contornos para cada color
dibujarContorno(contornosAmarillo, (0, 255, 255))  # Amarillo en BGR
dibujarContorno(contornosVioleta, (140, 40, 120))  # Violeta en BGR
dibujarContorno(contornosVerde, (0, 255, 0))  # Verde en BGR
dibujarContorno(contornosRojo, (0, 0, 255))  # Rojo en BGR

# Crear imagen de resumen con el conteo de cada color
imgResumen = 255 * np.ones((210, 100, 3), dtype=np.uint8)

# Dibujar círculos de colores en el resumen
cv2.circle(imgResumen, (30, 30), 15, (0, 255, 255), -1)  # Amarillo
cv2.circle(imgResumen, (30, 70), 15, (140, 40, 120), -1)  # Violeta
cv2.circle(imgResumen, (30, 110), 15, (0, 255, 0), -1)  # Verde
cv2.circle(imgResumen, (30, 150), 15, (0, 0, 255), -1)  # Rojo

# Agregar el conteo de cada color
cv2.putText(imgResumen, str(len(contornosAmarillo)), (65, 40), 1, 2, (0, 0, 0), 2)
cv2.putText(imgResumen, str(len(contornosVioleta)), (65, 80), 1, 2, (0, 0, 0), 2)
cv2.putText(imgResumen, str(len(contornosVerde)), (65, 120), 1, 2, (0, 0, 0), 2)
cv2.putText(imgResumen, str(len(contornosRojo)), (65, 160), 1, 2, (0, 0, 0), 2)

# Calcular y mostrar el total
totalCnts = (
    len(contornosAmarillo) + len(contornosVioleta) + len(contornosVerde) + len(contornosRojo)
)
cv2.putText(imgResumen, str(totalCnts), (55, 200), 1, 2, (0, 0, 0), 2)

# Imprimir resumen en consola
print(f"\n=== RESUMEN DE CONTEO ===")
print(f"Amarillo: {len(contornosAmarillo)}")
print(f"Violeta:  {len(contornosVioleta)}")
print(f"Verde:    {len(contornosVerde)}")
print(f"Rojo:     {len(contornosRojo)}")
print(f"TOTAL:    {totalCnts}")
print(f"========================\n")

cv2.imshow("Resumen", imgResumen)

# Mostrar las máscaras individuales (descomentarlas si se desea visualizar)
# cv2.imshow('maskAmarillo', maskAmarillo)
# cv2.imshow('maskVioleta', maskVioleta)
# cv2.imshow('maskVerde', maskVerde)
# cv2.imshow('maskRojo', maskRojo)

# Mostrar la imagen con los contornos dibujados
cv2.imshow("Imagen con Conteo por Color", imagen)

# Guardar la imagen resultante
cv2.imwrite("conteo.png", imagen)
print("Imagen guardada como 'conteo.png'")
print("Presiona cualquier tecla para cerrar...")

cv2.waitKey(0)
cv2.destroyAllWindows()

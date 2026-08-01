import cv2
import numpy as np

# Inicializar la captura de video desde la cámara web
# Para Windows: usar índice 0 (cámara por defecto)
cap = cv2.VideoCapture(0)

# CONFIGURACIÓN PARA LINUX:
# Si la cámara no funciona con el índice 0, prueba con otros índices:
# cap = cv2.VideoCapture(1)  # o 2, 3, etc.
#
# Para sistemas Linux con v4l2, usa:
# cap = cv2.VideoCapture(0, cv2.CAP_V4L2)
#
# Verifica las cámaras disponibles en Linux con: ls /dev/video*

# Definir los rangos de color rojo en el espacio HSV
# El rojo requiere dos rangos porque está en los extremos del círculo de matiz (0° y 360°)
redBajo1 = np.array([0, 100, 20], np.uint8)  # Límite inferior del rojo (primer rango)
redAlto1 = np.array([8, 255, 255], np.uint8)  # Límite superior del rojo (primer rango)

redBajo2 = np.array([175, 100, 20], np.uint8)  # Límite inferior del rojo (segundo rango)
redAlto2 = np.array([179, 255, 255], np.uint8)  # Límite superior del rojo (segundo rango)

# Verificar que la cámara se haya abierto correctamente
if not cap.isOpened():
    print("Error: No se pudo acceder a la cámara")
    exit()

print("Cámara iniciada correctamente. Presiona 's' para salir.")

while True:
    ret, frame = cap.read()

    if ret:
        # Convertir el frame al espacio de color HSV
        frameHSV = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # Crear dos máscaras para los dos rangos de color rojo
        maskRed1 = cv2.inRange(frameHSV, redBajo1, redAlto1)
        maskRed2 = cv2.inRange(frameHSV, redBajo2, redAlto2)

        # Combinar las dos máscaras
        maskRed = cv2.add(maskRed1, maskRed2)

        # Aplicar la máscara al frame original
        maskRedvis = cv2.bitwise_and(frame, frame, mask=maskRed)

        # Mostrar los resultados
        cv2.imshow("Frame Original", frame)
        cv2.imshow("Mascara Rojo", maskRed)
        cv2.imshow("Areas Rojas Detectadas", maskRedvis)

        # Salir al presionar 's'
        if cv2.waitKey(1) & 0xFF == ord("s"):
            break
    else:
        print("Error: No se pudo leer el frame de la cámara")
        break

# Liberar recursos
cap.release()
cv2.destroyAllWindows()
print("Programa finalizado correctamente")

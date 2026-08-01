import cv2
import imutils
import numpy as np

# Capturar video desde archivo
cap = cv2.VideoCapture("../img/angry.mp4")

# NOTA: Para usar la cámara web en lugar de un archivo de video:
# cap = cv2.VideoCapture(0)  # Windows/Mac
#
# CONFIGURACIÓN PARA LINUX CON CÁMARA:
# Si la cámara no funciona con el índice 0, prueba con otros índices:
# cap = cv2.VideoCapture(1)  # o 2, 3, etc.
#
# Para sistemas Linux con v4l2, usa:
# cap = cv2.VideoCapture(0, cv2.CAP_V4L2)
#
# Verifica las cámaras disponibles en Linux con: ls /dev/video*

# Definir los rangos de color rojo en el espacio HSV
rojoBajo1 = np.array([0, 140, 90], np.uint8)
rojoAlto1 = np.array([8, 255, 255], np.uint8)
rojoBajo2 = np.array([160, 140, 90], np.uint8)
rojoAlto2 = np.array([180, 255, 255], np.uint8)

# Verificar que el video se haya abierto correctamente
if not cap.isOpened():
    print("Error: No se pudo abrir el video")
    exit()

print("Video iniciado. Presiona 'ESC' para salir.")

while True:
    ret, frame = cap.read()

    # Si no hay más frames, salir del bucle
    if not ret:
        print("Fin del video")
        break

    # Redimensionar el frame para procesamiento más rápido
    frame = imutils.resize(frame, width=640)

    # Pasamos las imágenes de BGR a: GRAY (esta a BGR nuevamente) y a HSV
    frameGray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    frameGray = cv2.cvtColor(frameGray, cv2.COLOR_GRAY2BGR)
    frameHSV = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Detectamos el color rojo
    maskRojo1 = cv2.inRange(frameHSV, rojoBajo1, rojoAlto1)
    maskRojo2 = cv2.inRange(frameHSV, rojoBajo2, rojoAlto2)
    mask = cv2.add(maskRojo1, maskRojo2)
    mask = cv2.medianBlur(mask, 7)
    redDetected = cv2.bitwise_and(frame, frame, mask=mask)

    # Fondo en grises
    invMask = cv2.bitwise_not(mask)
    bgGray = cv2.bitwise_and(frameGray, frameGray, mask=invMask)

    # Sumamos bgGray y redDetected
    finalframe = cv2.add(bgGray, redDetected)

    # Visualización
    cv2.imshow("Frame", frame)
    cv2.imshow("finalframe", finalframe)

    # Salir al presionar ESC (tecla 27)
    if cv2.waitKey(1) & 0xFF == 27:
        break

# Liberar recursos
cap.release()
cv2.destroyAllWindows()
print("Programa finalizado correctamente")

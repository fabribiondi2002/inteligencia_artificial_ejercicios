import cv2
import numpy as np


def dibujar(mask, color):
    """Detecta y dibuja contornos de objetos en el frame basándose en una máscara de color.

    Args:
        mask: Máscara binaria con las áreas del color detectado
        color: Color en formato BGR para dibujar los contornos
    """
    contornos, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for c in contornos:
        area = cv2.contourArea(c)
        # Filtrar contornos pequeños (ruido)
        if area > 3000:
            # Calcular el centroide del contorno
            M = cv2.moments(c)
            if M["m00"] == 0:
                M["m00"] = 1
            x = int(M["m10"] / M["m00"])
            y = int(M["m01"] / M["m00"])

            # Crear un contorno convexo suavizado
            nuevoContorno = cv2.convexHull(c)

            # Dibujar el centroide y sus coordenadas
            cv2.circle(frame, (x, y), 7, (0, 255, 0), -1)
            cv2.putText(
                frame, "{},{}".format(x, y), (x + 10, y), font, 0.75, (0, 255, 0), 1, cv2.LINE_AA
            )

            # Dibujar el contorno del objeto
            cv2.drawContours(frame, [nuevoContorno], 0, color, 3)


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

# Definir los rangos de color azul en el espacio HSV
azulBajo = np.array([100, 100, 20], np.uint8)
azulAlto = np.array([125, 255, 255], np.uint8)

# Definir los rangos de color amarillo en el espacio HSV
amarilloBajo = np.array([15, 100, 20], np.uint8)
amarilloAlto = np.array([45, 255, 255], np.uint8)

# Definir los rangos de color rojo en el espacio HSV
redBajo1 = np.array([0, 100, 20], np.uint8)
redAlto1 = np.array([5, 255, 255], np.uint8)
redBajo2 = np.array([175, 100, 20], np.uint8)
redAlto2 = np.array([179, 255, 255], np.uint8)

# Definir la fuente para mostrar las coordenadas del centroide
font = cv2.FONT_HERSHEY_SIMPLEX

# Verificar que la cámara se haya abierto correctamente
if not cap.isOpened():
    print("Error: No se pudo acceder a la cámara")
    exit()

print("Cámara iniciada correctamente. Presiona 's' para salir.")

# Bucle principal de procesamiento de video
while True:
    ret, frame = cap.read()  # Leer un frame desde la cámara

    if ret == True:
        # Invertir la imagen horizontalmente (efecto espejo)
        frame = cv2.flip(frame, 1)

        # Convertir la imagen al espacio de color HSV
        frameHSV = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # Crear las máscaras para los diferentes colores
        maskAzul = cv2.inRange(frameHSV, azulBajo, azulAlto)  # Máscara para azul
        maskAmarillo = cv2.inRange(frameHSV, amarilloBajo, amarilloAlto)  # Máscara para amarillo
        maskRed1 = cv2.inRange(frameHSV, redBajo1, redAlto1)  # Primer rango de rojo
        maskRed2 = cv2.inRange(frameHSV, redBajo2, redAlto2)  # Segundo rango de rojo

        # Combinar las dos máscaras del color rojo
        maskRed = cv2.add(maskRed1, maskRed2)

        # Dibujar los objetos detectados para cada color
        dibujar(maskAzul, (255, 0, 0))  # Dibujar los objetos azules
        dibujar(maskAmarillo, (0, 255, 255))  # Dibujar los objetos amarillos
        dibujar(maskRed, (0, 0, 255))  # Dibujar los objetos rojos

        # Mostrar el frame original con los contornos dibujados
        cv2.imshow("frame", frame)

        # Si el usuario presiona 's', se rompe el bucle
        if cv2.waitKey(1) & 0xFF == ord("s"):
            break
    else:
        print("Error: No se pudo leer el frame de la cámara")
        break

# Liberar la captura de video y cerrar todas las ventanas
cap.release()
cv2.destroyAllWindows()
print("Programa finalizado correctamente")

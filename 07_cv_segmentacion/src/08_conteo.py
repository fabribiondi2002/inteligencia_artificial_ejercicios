import os

import cv2

# Ruta de la imagen
ruta_imagen = "../img/monedas.jpg"

# Verificar que el archivo existe
if not os.path.exists(ruta_imagen):
    print(f"Error: No se encuentra el archivo {ruta_imagen}")
    exit()

# Cargar la imagen
imagen = cv2.imread(ruta_imagen)
if imagen is None:
    print(f"Error: No se pudo cargar la imagen desde {ruta_imagen}")
    exit()

# Convertir la imagen a escala de grises
grises = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)

# Aplicar umbralización binaria inversa
# Los objetos oscuros sobre fondo claro se convierten en blancos
_, th = cv2.threshold(grises, 240, 255, cv2.THRESH_BINARY_INV)

# Encontrar contornos externos en la imagen umbralizada
cnts, _ = cv2.findContours(th, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Dibujar todos los contornos en azul
cv2.drawContours(imagen, cnts, -1, (255, 0, 0), 2)
print(f"Número de contornos encontrados: {len(cnts)}")

# Fuente para el texto
font = cv2.FONT_HERSHEY_SIMPLEX

# Procesar cada contorno individualmente
for i, c in enumerate(cnts):
    # Calcular los momentos del contorno para obtener el centroide
    M = cv2.moments(c)
    if M["m00"] == 0:
        M["m00"] = 1
    x = int(M["m10"] / M["m00"])
    y = int(M["m01"] / M["m00"])

    # Crear el mensaje con el número de objeto
    mensaje = f"Num: {i + 1}"
    cv2.putText(imagen, mensaje, (x - 40, y), font, 0.75, (255, 0, 0), 2, cv2.LINE_AA)
    cv2.drawContours(imagen, [c], 0, (255, 0, 0), 2)

    # Mostrar la imagen con el objeto actual resaltado
    cv2.imshow("Imagen", imagen)
    cv2.waitKey(0)

print(f"\nConteo completado: {len(cnts)} objetos detectados")
cv2.destroyAllWindows()

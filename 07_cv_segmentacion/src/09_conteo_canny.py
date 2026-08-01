import os

import cv2

# Ruta de la imagen
ruta_imagen = "../img/cartas.png"

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

# Detectar bordes usando el algoritmo de Canny
# Parámetros: umbral mínimo (100) y máximo (200)
bordes = cv2.Canny(grises, 100, 200)

# Encontrar contornos externos en la imagen de bordes
ctns, _ = cv2.findContours(bordes, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Dibujar todos los contornos en rojo
cv2.drawContours(imagen, ctns, -1, (0, 0, 255), 2)

# Mostrar información del conteo
num_contornos = len(ctns)
print(f"Número de contornos encontrados: {num_contornos}")
texto = f"Contornos encontrados: {num_contornos}"

# Agregar texto con el número de contornos en la imagen
cv2.putText(imagen, texto, (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 1)

# Mostrar la imagen con los contornos detectados
cv2.imshow("Contornos Detectados con Canny", imagen)
print("Presiona cualquier tecla para cerrar...")
cv2.waitKey(0)
cv2.destroyAllWindows()

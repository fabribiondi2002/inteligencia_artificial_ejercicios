# Importamos librerías para manejo de tiempo
import time

import cv2 as cv
import matplotlib.pyplot as plt
import numpy as np

img = cv.imread("../img/chewbacca.jpg")
gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

# Suavizado Gaussiano
# ====================
start = time.time()

blur = cv.GaussianBlur(gray, (5, 5), 0)

elapsed = time.time() - start
print("Blur {} segundos".format(elapsed))

# Gradientes
# ===========
start = time.time()

# Aplicamos Sobelx en 'float32' y luego convertimos de nuevo a 8-bit para evitar overflow
sobelx_64 = cv.Sobel(blur, cv.CV_32F, 1, 0, ksize=3)
absx_64 = np.absolute(sobelx_64)
sobelx_8u1 = absx_64 / absx_64.max() * 255
sobelx_8u = np.uint8(sobelx_8u1)

# De igual modo para Sobely
sobely_64 = cv.Sobel(blur, cv.CV_32F, 0, 1, ksize=3)
absy_64 = np.absolute(sobely_64)
sobely_8u1 = absy_64 / absy_64.max() * 255
sobely_8u = np.uint8(sobely_8u1)

# De los gradiente calculamos Magnitud y lo pasamos a 8-bit (Opcional)
mag = np.hypot(sobelx_8u, sobely_8u)
mag = mag / mag.max() * 255
mag = np.uint8(mag)

# Encontramos la Dirección y la pasamos a grados
theta = np.arctan2(sobely_64, sobelx_64)
angle = np.rad2deg(theta)

elapsed = time.time() - start
print("Gradientes {} segundos".format(elapsed))

# Supresión de no-máximos
# ========================
start = time.time()

# Encontramos los píxels vecinos (b,c) en la dirección (redondeadea) del gradiente y aplicamos la supresión de no-máximos
M, N = mag.shape
Non_max = np.zeros((M, N), dtype=np.uint8)

for i in range(1, M - 1):
    for j in range(1, N - 1):
        # Horizontal 0
        if (
            (0 <= angle[i, j] < 22.5)
            or (157.5 <= angle[i, j] <= 180)
            or (-22.5 <= angle[i, j] < 0)
            or (-180 <= angle[i, j] < -157.5)
        ):
            b = mag[i, j + 1]
            c = mag[i, j - 1]
        # Diagonal 45
        elif (22.5 <= angle[i, j] < 67.5) or (-157.5 <= angle[i, j] < -112.5):
            b = mag[i + 1, j + 1]
            c = mag[i - 1, j - 1]
        # Vertical 90
        elif (67.5 <= angle[i, j] < 112.5) or (-112.5 <= angle[i, j] < -67.5):
            b = mag[i + 1, j]
            c = mag[i - 1, j]
        # Diagonal 135
        elif (112.5 <= angle[i, j] < 157.5) or (-67.5 <= angle[i, j] < -22.5):
            b = mag[i + 1, j - 1]
            c = mag[i - 1, j + 1]

            # Supresión de no-máximos
        if (mag[i, j] >= b) and (mag[i, j] >= c):
            Non_max[i, j] = mag[i, j]
        else:
            Non_max[i, j] = 0

elapsed = time.time() - start
print("No-máximos {} segundos".format(elapsed))

# Umbralizado por histéresis
# ===========================
start = time.time()

UmbralAlto = 21
UmbralBajo = 15

M, N = Non_max.shape
out = np.zeros((M, N), dtype=np.uint8)

# Si la intensidad de un borde es mayor a 'UmbralAlto' es seguro un umbral, debajo de 'UmbralBajo' seguro no es
strong_i, strong_j = np.where(Non_max >= UmbralAlto)
zeros_i, zeros_j = np.where(Non_max < UmbralBajo)

# Bordes débiles
weak_i, weak_j = np.where((Non_max <= UmbralAlto) & (Non_max >= UmbralBajo))

# Setear el mismo valor a todos los tipos de píxel
out[strong_i, strong_j] = 255
out[zeros_i, zeros_j] = 0
out[weak_i, weak_j] = 75

elapsed = time.time() - start
print("Histéresis {} segundos".format(elapsed))

# Armo la imagen de bordes
# =========================
start = time.time()
M, N = out.shape
for i in range(1, M - 1):
    for j in range(1, N - 1):
        if out[i, j] == 75:
            if 255 in [
                out[i + 1, j - 1],
                out[i + 1, j],
                out[i + 1, j + 1],
                out[i, j - 1],
                out[i, j + 1],
                out[i - 1, j - 1],
                out[i - 1, j],
                out[i - 1, j + 1],
            ]:
                out[i, j] = 255
            else:
                out[i, j] = 0

elapsed = time.time() - start
print("Armado imagen bordes {} segundos".format(elapsed))

# Muestro la imagen
# ==================
cv.imshow("Canny", out)

cv.waitKey(0)
cv.destroyAllWindows()

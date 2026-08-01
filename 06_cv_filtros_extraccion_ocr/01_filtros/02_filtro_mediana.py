import cv2 as cv
import numpy as np
from skimage.util import random_noise

# el segundo argumento '0' indica que la imagen se cargará en escala de grises
img2 = cv.imread("../img/tapitas.jpg")

# Agregar ruido salt&pepper a la
# 'mode="s&p"' indica el tipo de ruido (salt & pepper),
# 'amount=0.3' define la cantidad de ruido que se añadirá
noise_img = random_noise(img2, mode="s&p", amount=0.3)

# Convertimos la imagen ruidosa a un array de enteros sin signo de 8 bits (uint8)
# random_noise devuelve una imagen en formato float
noise_img = np.array(255 * noise_img, dtype="uint8")

# Otra manera de agregar ruido (no es salt&pepper) con numpy
# gauss = np.random.normal(0,1,img2.size)
# gauss = gauss.reshape(img2.shape[0],img2.shape[1]).astype('uint8')
# noise_img = img2 + img2 * gauss

# Aplicar el filtro de media
# 'cv.blur' aplica un filtro de media con un kernel de 5x5, suavizando la imagen y reduciendo el ruido
mean = cv.blur(noise_img, (5, 5))

# Aplicar el filtro de mediana
# 'cv.medianBlur' aplica un filtro de mediana con un kernel de 5x5,
# que es especialmente efectivo para eliminar ruido tipo "salt and pepper"
median = cv.medianBlur(noise_img, 5)

# Mostrar la imagen
cv.imshow("Original", img2)
cv.imshow("Original - S&P", noise_img)
cv.imshow("Media", mean)
cv.imshow("Mediana", median)

cv.waitKey(0)
cv.destroyAllWindows()

import cv2 as cv
import matplotlib.pyplot as plt
import numpy as np

# Cargamos la imagen a procesar
img = cv.imread("../img/justiceleague.jpg")

# 1. Bajamos resolución con pirámides (Gaussianas)

print("\nTamaño imagen: {} pix".format(img.shape))

# Nivel 1
img_nivel_1 = cv.pyrDown(img)
print("\nTamaño imagen: {} pix".format(img_nivel_1.shape))

# Nivel 2
img_nivel_2 = cv.pyrDown(img_nivel_1)
print("\nTamaño imagen: {} pix".format(img_nivel_2.shape))

# Nivel 3
img_nivel_3 = cv.pyrDown(img_nivel_2)
print("\nTamaño imagen: {} pix".format(img_nivel_3.shape))

# Muestro los resultados
cv.imshow("Imagen Original", img)
cv.imshow("Imagen Nivel 1", img_nivel_1)
cv.imshow("Imagen Nivel 2", img_nivel_2)
cv.imshow("Imagen Nivel 3", img_nivel_3)

"""
# 2. Subimos un nivel (desde el último)

# Esto aumenta la resolución inyectando filas y columnas de ceros intercaladas y luego
# convolucionando el resultado con el núcleo gaussiano 5 × 5 multiplicado por 4
img_nivel_2 = cv.pyrUp(img_nivel_3)

# Muestro el resultado por subir el nivel
cv.imshow("Imagen Nivel 2", img_nivel_2)

# Otra forma de modificar la resolucion (util para downscaling o upscaling con escala arbitraria)

img = cv.imread('../img/origami.jpg')
print(f'Tamaño original: {img.shape}')

scales = np.linspace(0.5, 2, 5)
resized_imgs = list()

# generamos nuestra "piramide" de tamaños arbitrarios
print(f'Dimensiones generadas:')
for scale in scales:
    resized_imgs.append(cv.resize(img, None, fx=scale, fy=scale))
    print(resized_imgs[-1].shape)

# mostramos las imagenes
for i, img in enumerate(resized_imgs):
    cv.imshow(f'nivel-{i}', img)
"""
cv.waitKey(0)
cv.destroyAllWindows()

import cv2 as cv
import matplotlib.pyplot as plt
import numpy as np

img = cv.imread("../img/origami.jpg")
print(f"Tamaño original: {img.shape}")

base = img.copy()

# Creamos la pirámide Gaussiana
piramide_gauss = [base]
for i in range(3):
    base = cv.pyrDown(base)
    piramide_gauss.append(base)

# El último nivel de la Gaussiana permanece en el mismo lugar en la Laplaciana
punta_laplaciana = piramide_gauss[-1]

# Creamos la pirámide Laplaciana
piramide_laplace = [punta_laplaciana]
for i in range(3, 0, -1):
    size = (piramide_gauss[i - 1].shape[1], piramide_gauss[i - 1].shape[0])
    gaussiana_expandida = cv.pyrUp(piramide_gauss[i], dstsize=size)
    laplaciana = cv.subtract(piramide_gauss[i - 1], gaussiana_expandida)
    piramide_laplace.append(laplaciana)
    cv.imshow("nivel-{}".format(i - 1), laplaciana)

cv.waitKey(0)
cv.destroyAllWindows()

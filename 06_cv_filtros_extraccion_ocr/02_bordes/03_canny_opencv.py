# Importamos librerías para manejo de tiempo
import time

import cv2 as cv
import matplotlib.pyplot as plt
import numpy as np

# Cargo la imagen
# ================
img = cv.imread("../img/chewbacca.jpg")
gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

# Aplico Canny
# =============
start = time.time()
edges = cv.Canny(img, threshold1=10, threshold2=50)
elapsed = time.time() - start
print("Tiempo de procesamiento {} segundos".format(elapsed))

# Muestro la imagen
# ==================
cv.imshow("CannyCV", edges)

cv.waitKey(0)
cv.destroyAllWindows()

import cv2 as cv

# Cargamos la imagen
img_orig = cv.imread("../img/tapitas.jpg", 0)  # detectamos bordes
# img_orig = cv.imread('../img/chewbacca.jpg',0) # detectamos caracteristicas/textura

# Aplicamos un suavizado Gaussiano de 5x5
low_sigma = cv.GaussianBlur(img_orig, (5, 5), sigmaX=1)
high_sigma = cv.GaussianBlur(img_orig, (5, 5), sigmaX=1.5)

# Calculamos el DoG por sustracción
dog = low_sigma - high_sigma

# Aplico filtro de mediana para mejorar el resultado
median = cv.medianBlur(dog, 5)

# Mostramos la imagen
out1 = cv.hconcat([img_orig, dog, median])
cv.namedWindow("DoG", 2)
cv.imshow("DoG", out1)

cv.waitKey(0)
cv.destroyAllWindows()

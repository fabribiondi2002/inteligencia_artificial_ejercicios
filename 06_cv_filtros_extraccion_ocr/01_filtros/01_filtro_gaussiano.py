import cv2 as cv
import numpy as np

# Parámetros:
# ksize - Tamaño del núcleo, positivo impar (3,5,...)
# sigma - Desvío estándar de la Gaussiana. Si no es positivo,
#          se calcula como sigma = 0.3*((ksize-1)*0.5 - 1) + 0.8
# ktype - Tipo de coeficientes del filtro (Optional). Puede ser CV_32F o CV_64F

# Genera un kernel gaussiano unidimensional con tamaño 5 y sigma 1.5
nucleo_g = cv.getGaussianKernel(ksize=5, sigma=1.5)

# Imprime el núcleo gaussiano unidimensional
print(nucleo_g)

# Imprime la suma de los productos de los elementos del núcleo por su transpuesta,
# que debería ser 1 para un kernel gaussiano normalizado.
print(np.sum(nucleo_g * nucleo_g.T))

# Multiplica el núcleo unidimensional por su transpuesta para crear un kernel 2D
kernel = nucleo_g * nucleo_g.T
print(kernel)

# Imprime la suma de todos los elementos del kernel 2D para verificar que está normalizado
print(np.sum(kernel))

# Suavizado Gaussiano usando el Kernel
# =====================================
img_orig = cv.imread("../img/chewbacca.jpg")

# Creamos un núcleo gaussiano unidimensional con tamaño 17 y sigma 5 para la dirección X
kX = cv.getGaussianKernel(ksize=17, sigma=5)

# Creamos un núcleo gaussiano unidimensional con tamaño 17 y sigma 5 para la dirección Y
kY = cv.getGaussianKernel(ksize=17, sigma=5)

# Aplicamos filtro gaussiano separable a la imagen utilizando los núcleos kX y kY
result_a = cv.sepFilter2D(img_orig, ddepth=-1, kernelX=kX, kernelY=kY)

# ----------------------  Más fácil utilizando una única línea
# SOLO cuando el kernel es cuadrado!!

# filtro gaussiano directamente usando la función GaussianBlur
result_b = cv.GaussianBlur(img_orig, ksize=(17, 17), sigmaX=5, sigmaY=5)

# Combina horizontalmente las imágenes filtradas 'result_b' y 'result_a' para compararlas
out1 = cv.hconcat([result_b, result_a])
out2 = cv.hconcat([img_orig, result_b])

# Crea una ventana para mostrar la imagen combinada
cv.namedWindow("Chewbacca - sepFilter2D", 2)

# Muestra la imagen combinada en la ventana creada
cv.imshow("Chewbacca - sepFilter2D", out1)

cv.namedWindow("Chewbacca - GaussianBlur", 2)
cv.imshow("Chewbacca - GaussianBlur", out2)

cv.waitKey(0)
cv.destroyAllWindows()

import cv2 as cv
import matplotlib.pyplot as plt
import numpy as np

# Paso 1
# =======
# Cargamos las imágenes
img1 = cv.imread("../img/justiceleague.jpg")
img2 = cv.imread("../img/guason.png")
# Modificamos los tamaños de las imágenes si fuese necesario (en nuestro caso tienen el mismo tamaño)
img1 = cv.resize(img1, (1920, 1080))
img2 = cv.resize(img2, (1920, 1080))

# Muestro las imágenes para elegir los límites de la máscara
plt.imshow(img1)
plt.figure()
plt.imshow(img2)


# Paso 2
# =======
# Encontrar las pirámides Gaussianas de las dos imágenes y la máscara
def gaussian_pyramid(img, num_levels):
    lower = img.copy()
    gaussian_pyr = [lower]
    for i in range(num_levels):
        lower = cv.pyrDown(lower)
        gaussian_pyr.append(np.float32(lower))
    return gaussian_pyr


# Paso 3
# =======
# Calcular la pirámide Laplaciana
def laplacian_pyramid(gaussian_pyr):
    laplacian_top = gaussian_pyr[-1]
    num_levels = len(gaussian_pyr) - 1

    laplacian_pyr = [laplacian_top]
    for i in range(num_levels, 0, -1):
        size = (gaussian_pyr[i - 1].shape[1], gaussian_pyr[i - 1].shape[0])
        gaussian_expanded = cv.pyrUp(gaussian_pyr[i], dstsize=size)
        laplacian = np.subtract(gaussian_pyr[i - 1], gaussian_expanded)
        laplacian_pyr.append(laplacian)
    return laplacian_pyr


# Paso 4
# =======
# Fusionar las dos imagenes según la máscara indicada
def blend(laplacian_A, laplacian_B, mask_pyr):
    LS = []
    for la, lb, mask in zip(laplacian_A, laplacian_B, mask_pyr):
        ls = lb * mask + la * (1.0 - mask)
        LS.append(ls)
    return LS


# Paso 5
# =======
# Reconstruir la imagen original
def reconstruct(laplacian_pyr):
    laplacian_top = laplacian_pyr[0]
    laplacian_lst = [laplacian_top]
    num_levels = len(laplacian_pyr) - 1
    for i in range(num_levels):
        size = (laplacian_pyr[i + 1].shape[1], laplacian_pyr[i + 1].shape[0])
        laplacian_expanded = cv.pyrUp(laplacian_top, dstsize=size)
        laplacian_top = cv.add(laplacian_pyr[i + 1], laplacian_expanded)
        laplacian_lst.append(laplacian_top)
    return laplacian_lst


# Crear la máscara
# mask = cv.imread('justiceleague_mask.png')
mask = np.zeros((1080, 1920, 3), dtype="float32")
mask[130:430, 605:825, :] = (1, 1, 1)

num_levels = 7

# Para la 1er imagen, calcular Gaussiana y Laplaciana
gaussian_pyr_1 = gaussian_pyramid(img1, num_levels)
laplacian_pyr_1 = laplacian_pyramid(gaussian_pyr_1)
# Para la 2da imagen, calcular Gaussiana y Laplaciana
gaussian_pyr_2 = gaussian_pyramid(img2, num_levels)
laplacian_pyr_2 = laplacian_pyramid(gaussian_pyr_2)
# Calcular la pirámide Gaussiana para la máscara e invertirla
mask_pyr_final = gaussian_pyramid(mask, num_levels)
mask_pyr_final.reverse()
# Armar pirámide de fusión de las imágenes
add_laplace = blend(laplacian_pyr_1, laplacian_pyr_2, mask_pyr_final)
# Reconstruir la imagen
final = reconstruct(add_laplace)

# Guardo en disco
imagen_normalizada = cv.normalize(final[num_levels], None, 0, 255, cv.NORM_MINMAX, cv.CV_8U)
cv.imwrite("fusion.png", imagen_normalizada)

cv.waitKey(0)
cv.destroyAllWindows()

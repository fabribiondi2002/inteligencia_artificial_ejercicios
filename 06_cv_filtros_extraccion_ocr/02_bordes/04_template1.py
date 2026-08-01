import cv2 as cv
import matplotlib.pyplot as plt
import numpy as np

# Cargamos la imagen a procesar
img = cv.imread("../img/batman_lego.jpg")

img_rgb = cv.cvtColor(img, cv.COLOR_BGR2RGB)
img_gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
template = cv.imread("../img/patron.png", 0)

plt.figure()
plt.subplot(1, 2, 1)
plt.imshow(template, cmap="gray")
plt.subplot(1, 2, 2)
plt.imshow(img_rgb)

w, h = template.shape[::-1]
# Los 6 métodos posibles para comparación:
methods = [
    "cv.TM_CCOEFF",
    "cv.TM_CCOEFF_NORMED",
    "cv.TM_CCORR",
    "cv.TM_CCORR_NORMED",
    "cv.TM_SQDIFF",
    "cv.TM_SQDIFF_NORMED",
]

for meth in methods:
    # Hago una copia de la imagen porque ciclo a ciclo le dibujo rectángulos
    img_salida = img_rgb.copy()

    method = eval(meth)

    # Aplicamos la coincidencia de patrones
    # --------------------------------------
    res = cv.matchTemplate(img_gray, template, method)

    # Encontramos los valores máximos y mínimos
    min_val, max_val, min_loc, max_loc = cv.minMaxLoc(res)

    # Si el método es TM_SQDIFF o TM_SQDIFF_NORMED, tomamos el mínimo
    if method in [cv.TM_SQDIFF, cv.TM_SQDIFF_NORMED]:
        top_left = min_loc
    else:
        top_left = max_loc

    # Marcamos el lugar donde lo haya encontrado
    # ----------------------------------------
    bottom_right = (top_left[0] + w, top_left[1] + h)
    cv.rectangle(img_salida, top_left, bottom_right, 255, 2)

    # Graficamos el procesamiento y la salida
    # ----------------------------------------
    plt.figure()

    # Resultado de coincidencia
    plt.subplot(121), plt.imshow(res, cmap="gray")
    plt.title("Matching Result"), plt.xticks([]), plt.yticks([])

    # Imagen original con recuadros
    plt.subplot(122), plt.imshow(img_salida)
    plt.title("Detected Point"), plt.xticks([]), plt.yticks([])

    plt.suptitle(meth)
    plt.show()

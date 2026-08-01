import cv2 as cv
import matplotlib.pyplot as plt

# Cargar la imagen (la carga como BGR)
img_orig = cv.imread("../img/chewbacca.jpg")

# La convertimos a RGB
img_orig = cv.cvtColor(img_orig, cv.COLOR_BGR2RGB)

# Suavizamos la imagen con un filtro Gaussiano
gauss = cv.GaussianBlur(img_orig, (7, 7), 0.5)

# Aplicamos la máscara de enfoque usando cv.addWeighted
# Esta operación crea una imagen enfocada combinando la imagen original y la imagen suavizada
# El parámetro alpha=2 multiplica la imagen original y beta=-1 multiplica la imagen suavizada
# La imagen resultante es una versión enfocada de la imagen original
img_sharp = cv.addWeighted(img_orig, 2, gauss, -1, 0)

# Más enfocada (k=1.5)
k = 1.5
img_sharp2 = cv.addWeighted(img_orig, k + 1, gauss, -k, 0)

# Re enfocada (k=50)
k = 50
img_sharp3 = cv.addWeighted(img_orig, k + 1, gauss, -k, 0)

# Crear una nueva figura para mostrar las imágenes
fig = plt.figure()

# Mostrar la imagen original
ax1 = plt.subplot(221)
ax1.set_title("Original")
ax1.imshow(img_orig)

# Mostrar la imagen con enfoque (k=1)
ax2 = plt.subplot(222)
ax2.set_title("Enfocada (k=1)")
ax2.imshow(img_sharp)

# Mostrar la imagen más enfocada (k=1.5)
ax3 = plt.subplot(223)
ax3.set_title("Más enfocada (k=1.5)")
ax3.imshow(img_sharp2)

# Mostrar la imagen re enfocada (k=50)
ax4 = plt.subplot(224)
ax4.set_title(f"Re enfocada (k={k})")
ax4.imshow(img_sharp3)

# Mostrar la figura con todas las sub-imágenes
plt.show()

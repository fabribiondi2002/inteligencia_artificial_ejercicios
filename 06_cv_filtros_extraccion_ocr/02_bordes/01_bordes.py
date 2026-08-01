import cv2 as cv
import matplotlib.pyplot as plt

img = cv.imread("../img/golazo.jpg", 0)

grises = False
# grises=False
if grises:
    # En escala de grises
    laplacian = cv.Laplacian(img, cv.CV_64F)
    sobelx = cv.Sobel(img, cv.CV_64F, 1, 0, ksize=3)
    sobely = cv.Sobel(img, cv.CV_64F, 0, 1, ksize=3)
else:
    # En blanco y negro
    laplacian = cv.Laplacian(img, cv.CV_8U)
    sobelx = cv.Sobel(img, cv.CV_8U, 1, 0, ksize=3)
    sobely = cv.Sobel(img, cv.CV_8U, 0, 1, ksize=3)

ax1 = plt.subplot(2, 2, 1), plt.imshow(img, cmap="gray")
plt.title("Original"), plt.xticks([]), plt.yticks([])
ax2 = plt.subplot(2, 2, 2), plt.imshow(laplacian, cmap="gray")
plt.title("Laplaciano"), plt.xticks([]), plt.yticks([])
ax3 = plt.subplot(2, 2, 3), plt.imshow(sobelx, cmap="gray")
plt.title("Sobel X"), plt.xticks([]), plt.yticks([])
ax4 = plt.subplot(2, 2, 4), plt.imshow(sobely, cmap="gray")
plt.title("Sobel Y"), plt.xticks([]), plt.yticks([])

plt.show()

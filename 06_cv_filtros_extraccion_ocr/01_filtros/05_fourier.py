import cv2 as cv
import matplotlib.pyplot as plt
import numpy as np

# Leemos ambas imagenes
img_low_freq = cv.imread("../img/fft_hf.jpg", cv.IMREAD_GRAYSCALE)
img_hig_freq = cv.imread("../img/fft_lf.jpg", cv.IMREAD_GRAYSCALE)

# Aplico la transformada
img_fft_low = np.fft.fft2(img_low_freq)
img_fft_hig = np.fft.fft2(img_hig_freq)

# llevo la baja frec al origen para acomodar la visualizacion
img_fft_low = np.fft.fftshift(img_fft_low)
img_fft_hig = np.fft.fftshift(img_fft_hig)

# obtengo el modulo
img_fft_low = 20 * np.log(np.abs(img_fft_low))
img_fft_hig = 20 * np.log(np.abs(img_fft_hig))

# Tomamos un "perfil" de una fila por cada imagen
low_freq_sg = img_low_freq[50, 10:60]
hig_freq_sg = img_hig_freq[50, 10:60]

# Graficamos los resultados
plt.figure(figsize=(12, 12))
plt.subplot(3, 2, 1)
plt.imshow(img_low_freq, cmap="gray")
plt.subplot(3, 2, 2)
plt.imshow(img_hig_freq, cmap="gray")

plt.subplot(3, 2, 3)
plt.plot(low_freq_sg)
plt.subplot(3, 2, 4)
plt.plot(hig_freq_sg)

plt.subplot(3, 2, 5)
plt.imshow(img_fft_low, cmap="jet")
plt.subplot(3, 2, 6)
plt.imshow(img_fft_hig, cmap="jet")

plt.show()

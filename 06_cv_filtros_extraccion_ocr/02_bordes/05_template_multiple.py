import cv2 as cv
import matplotlib.pyplot as plt
import numpy as np

img_rgb = cv.imread("../img/batman_lego.jpg")
img_gray = cv.cvtColor(img_rgb, cv.COLOR_BGR2GRAY)
template = cv.imread("../img/patron.png", 0)

w, h = template.shape[::-1]
res = cv.matchTemplate(img_gray, template, cv.TM_CCOEFF_NORMED)
# Fijamos un umbral de "coincidencia"
threshold = 0.99

loc = np.where(res >= threshold)
for pt in zip(*loc[::-1]):
    cv.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0, 0, 255), 2)

cv.imshow("batmans", img_rgb)
# cv.imwrite('res.png',img_rgb)

cv.waitKey(0)
cv.destroyAllWindows()

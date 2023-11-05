from PyQt6.QtWidgets import QApplication, QWidget
import cv2
import numpy as np

img = cv2.imread('luna.tif')
c = 100

# cambiar tipo a "float"
img2 = img.astype(float)

# transformación Logaritmo :  s = c log(1 + r)
img2 = c * np.log(1 + img2)

# regresar tipo a uint8
img2 = img2.astype(np.uint8)

cv2.imshow('Original', img)
cv2.imshow('Log', img2)
cv2.waitKey(0)
cv2.destroyAllWindows()

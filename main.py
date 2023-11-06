from PyQt6.QtWidgets import (QApplication, QPushButton, QMainWindow, QFileDialog,
                             QLabel, QWidget, QHBoxLayout, QVBoxLayout)
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import QSize, Qt
import sys
import cv2
import numpy as np


class VentanaPrincipal(QMainWindow):
    def __init__(self):
        super().__init__()

        self.img = QLabel(self)
        self.setWindowTitle("Transformación logaritmo")
        self.setFixedSize(QSize(1280, 720))

        button_sel_img = QPushButton("Abrir imagen")
        button_sel_img.setFixedSize(QSize(200, 100))
        button_sel_img.clicked.connect(self.select_img_click)

        h_layout = QHBoxLayout()
        h_layout.addWidget(button_sel_img)
        h_layout.addWidget(self.img)

        contenedor = QWidget()
        contenedor.setLayout(h_layout)

        self.setCentralWidget(contenedor)
        # self.setCentralWidget(button_sel_img)

    def select_img_click(self, c):
        img_name = QFileDialog.getOpenFileName(self, 'Open file', '/home')
        orig_pix_map = QPixmap(img_name[0])
        scaled_pix_map = orig_pix_map.scaled(QSize(256, 256),
                                             Qt.AspectRatioMode.KeepAspectRatio)
        self.img.setPixmap(scaled_pix_map)


app = QApplication(sys.argv)

ventana = VentanaPrincipal()
ventana.show()

sys.exit(app.exec())
# img = cv2.imread('luna.tif')
# c = 100

# cambiar tipo a "float"
# img2 = img.astype(float)

# transformación Logaritmo :  s = c log(1 + r)
# img2 = c * np.log(1 + img2)

# regresar tipo a uint8
# img2 = img2.astype(np.uint8)

# cv2.imshow('Original', img)
# cv2.imshow('Log', img2)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

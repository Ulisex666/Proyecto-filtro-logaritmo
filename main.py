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

        self.setWindowTitle("Transformación logaritmo")
        self.setFixedSize(QSize(1280, 720))

        self.img_original = QLabel(self)
        self.ruta = None

        boton_select_img = QPushButton("Abrir imagen")
        boton_select_img.setFixedSize(QSize(200, 100))
        boton_select_img.clicked.connect(self.select_img_click)

        boton_filtro_log = QPushButton("Aplicar filtro")
        boton_filtro_log.setFixedSize(QSize(200, 100))
        boton_filtro_log.clicked.connect(self.filtro_img_click)

        h_layout = QHBoxLayout()
        h_layout.addWidget(boton_select_img)
        h_layout.addWidget(boton_filtro_log)
        h_layout.addWidget(self.img_original)

        contenedor = QWidget()
        contenedor.setLayout(h_layout)

        self.setCentralWidget(contenedor)
        # self.setCentralWidget(button_sel_img)

    def select_img_click(self):
        img_name = QFileDialog.getOpenFileName(self, 'Abrir archivo', '/home', '*.tif')
        self.ruta = img_name[0]
        orig_pix_map = QPixmap(self.ruta)
        scaled_pix_map = orig_pix_map.scaled(QSize(256, 256),
                                             Qt.AspectRatioMode.KeepAspectRatio)
        self.img_original.setPixmap(scaled_pix_map)
        self.img_original.setAlignment(Qt.AlignmentFlag.AlignTop)

    def filtro_img_click(self):
        if not self.ruta:
            return 0
        else:
            img_no_filtro = cv2.imread(self.ruta)
            img2 = img_no_filtro.astype(float)
            img2 = 50 * np.log(1 + img_no_filtro)
            img2 = img2.astype(np.uint8)
            cv2.imshow('wey', img2)


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

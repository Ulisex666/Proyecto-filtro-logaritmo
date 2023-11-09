from PyQt6.QtWidgets import (QApplication, QPushButton, QMainWindow, QFileDialog,
                             QLabel, QWidget, QDoubleSpinBox, QGridLayout, QHBoxLayout,
                             QStyle)
from PyQt6.QtGui import QPixmap, QImage
from PyQt6.QtCore import QSize, Qt
import sys
import cv2
import numpy as np


class VentanaPrincipal(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Transformación logaritmo")
        self.setFixedSize(QSize(1280, 720))
        icon = self.style().standardIcon(QStyle.StandardPixmap.SP_TrashIcon)
        self.setWindowIcon(icon)

        self.img_original = QLabel(self)
        self.img_final = QLabel(self)
        self.ruta = None

        boton_select_img = QPushButton("Abrir imagen")
        boton_select_img.setFixedSize(QSize(100, 50))
        boton_select_img.clicked.connect(self.select_img_click)

        boton_filtro_log = QPushButton("Aplicar filtro")
        boton_filtro_log.setFixedSize(QSize(100, 50))
        boton_filtro_log.clicked.connect(self.filtro_img_click)

        boton_filtro_opt = QPushButton("Aplicar filtro \n"
                                       "óptimo")
        boton_filtro_opt.setFixedSize(QSize(100, 50))
        boton_filtro_opt.clicked.connect(self.filtro_opt_click)

        self.parametro = QDoubleSpinBox()
        self.parametro.setRange(1, 100)
        self.parametro.setPrefix('C=')
        self.parametro.setFixedSize(QSize(75, 20))

        tuto_label = QLabel('Selecciones una imagen para \n'
                            'aplicar la transformación logaritmo. \n'
                            'Mientras más aumente el factor C, \n'
                            'aumentara el brillo de la imagen. \n'
                            )
        tuto_label.setFixedSize(QSize(200, 100))

        layout_grid = QGridLayout()
        layout_grid.setSpacing(20)
        layout_botones = QGridLayout()
        layout_botones.setSpacing(10)
        layout_img = QGridLayout()

        layout_botones.addWidget(boton_select_img, 0, 0)
        layout_botones.addWidget(boton_filtro_log, 0, 1)
        layout_botones.addWidget(boton_filtro_opt, 1, 0)
        layout_botones.addWidget(self.parametro, 1, 1)
        layout_botones.addWidget(tuto_label, 2, 0)

        layout_img.addWidget(self.img_original, 0, 0)
        layout_img.addWidget(self.img_final, 0, 1)

        layout_grid.addLayout(layout_botones, 0, 0)
        layout_grid.addLayout(layout_img, 0, 1)

        contenedor = QWidget()
        contenedor.setLayout(layout_grid)

        self.setCentralWidget(contenedor)

    def select_img_click(self):
        img_name = QFileDialog.getOpenFileName(self, 'Abrir archivo', '/home/',
                                               '*.tif *.jpg *.png *.jpeg')
        self.ruta = img_name[0]
        orig_pix_map = QPixmap(self.ruta)
        scaled_pix_map = orig_pix_map.scaled(QSize(400, 400),
                                             Qt.AspectRatioMode.KeepAspectRatio)
        self.img_original.setPixmap(scaled_pix_map)
        # self.img_original.setAlignment(Qt.AlignmentFlag.AlignTop)

    def filtro_img_click(self):
        if not self.ruta:
            return 0
        else:
            img_no_filtro = cv2.imread(self.ruta)
            img_no_filtro = cv2.cvtColor(img_no_filtro, cv2.COLOR_RGB2GRAY)
            c = self.parametro.value()
            img_no_filtro = img_no_filtro.astype(float)
            img_filtro = c * np.log(img_no_filtro + 1)
            img_filtro = img_filtro.astype(np.uint8)
            img_filtro = QImage(img_filtro, img_filtro.shape[1], img_filtro.shape[0],
                                img_filtro.strides[0], QImage.Format.Format_Grayscale8)
            pix_map_filtro = QPixmap.fromImage(img_filtro)
            scaled_pix_map_filtro = pix_map_filtro.scaled(QSize(400, 400),
                                                          Qt.AspectRatioMode.KeepAspectRatio)
            self.img_final.setPixmap(scaled_pix_map_filtro)
            # self.img_final.setAlignment(Qt.AlignmentFlag.AlignCenter)

    def filtro_opt_click(self):
        if not self.ruta:
            return 0
        else:
            img_no_filtro = cv2.imread(self.ruta)
            img_no_filtro = cv2.cvtColor(img_no_filtro, cv2.COLOR_RGB2GRAY)
            img_no_filtro = img_no_filtro.astype(float)
            c = 255 / np.log(1 + np.max(img_no_filtro))
            self.parametro.setValue(c)
            img_filtro = c * np.log(img_no_filtro + 1)
            img_filtro = img_filtro.astype(np.uint8)
            img_filtro = QImage(img_filtro, img_filtro.shape[1], img_filtro.shape[0],
                                img_filtro.strides[0], QImage.Format.Format_Grayscale8)
            pix_map_filtro = QPixmap.fromImage(img_filtro)
            scaled_pix_map_filtro = pix_map_filtro.scaled(QSize(400, 400),
                                                          Qt.AspectRatioMode.KeepAspectRatio)
            self.img_final.setPixmap(scaled_pix_map_filtro)
            # self.img_final.setAlignment(Qt.AlignmentFlag.AlignCenter)


app = QApplication(sys.argv)

ventana = VentanaPrincipal()
ventana.show()

sys.exit(app.exec())

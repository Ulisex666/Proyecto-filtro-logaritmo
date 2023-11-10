from PyQt6.QtWidgets import (QApplication, QPushButton, QMainWindow, QFileDialog,
                             QLabel, QWidget, QDoubleSpinBox, QGridLayout, QHBoxLayout,
                             QStyle, QStatusBar)
from PyQt6.QtGui import QPixmap, QImage, QAction, QKeySequence
from PyQt6.QtCore import QSize, Qt
import sys
import cv2
import numpy as np


class VentanaPrincipal(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Transformación logaritmo")
        self.setFixedSize(QSize(1280, 720))
        icon = self.style().standardIcon(QStyle.StandardPixmap.SP_MessageBoxCritical)
        self.setWindowIcon(icon)

        self.img_original = QLabel(self)
        self.img_final = QLabel(self)
        self.pix_map_filtro = QPixmap()

        self.bandera_img_final = False
        self.ruta = None

        accion_abrir_file = QAction('Abrir imagen', self)
        accion_abrir_file.triggered.connect(self.select_img_click)
        accion_abrir_file.setShortcut(QKeySequence('Ctrl+A'))

        accion_save_file = QAction('Guardar imagen transformada', self)
        accion_save_file.triggered.connect(self.save_file)
        accion_save_file.setShortcut(QKeySequence('Ctrl+S'))

        accion_clear_img_original = QAction('Borrar imagen original', self)
        accion_clear_img_original.triggered.connect(self.clear_img_original)
        accion_clear_img_original.setShortcut(QKeySequence('Ctrl+D'))

        accion_clear_img_filtro = QAction('Borrar imagen transformada', self)
        accion_clear_img_filtro.triggered.connect(self.clear_img_final)
        accion_clear_img_filtro.setShortcut(QKeySequence('Ctrl+Alt+D'))

        menu_bar = self.menuBar()
        menu_archivo = menu_bar.addMenu('&Archivo')
        menu_archivo.addSeparator()
        menu_archivo.addAction(accion_abrir_file)
        menu_archivo.addAction(accion_save_file)
        menu_archivo.addAction(accion_clear_img_original)
        menu_archivo.addAction(accion_clear_img_filtro)

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

        self.error_label = QLabel()
        self.error_label.setFixedSize(QSize(200, 50))

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
        layout_botones.addWidget(self.error_label, 3, 0)

        layout_img.addWidget(self.img_original, 0, 0)
        layout_img.addWidget(self.img_final, 0, 1)

        layout_grid.addLayout(layout_botones, 0, 0)
        layout_grid.addLayout(layout_img, 0, 1)

        contenedor = QWidget()
        contenedor.setLayout(layout_grid)

        self.setCentralWidget(contenedor)

    def select_img_click(self):
        self.error_label.clear()
        self.error_label.setStyleSheet('background-color:none')
        img_name = QFileDialog.getOpenFileName(self, 'Abrir archivo', '/home/',
                                               '*.tif *.jpg *.png *.jpeg')
        self.ruta = img_name[0]
        orig_pix_map = QPixmap(self.ruta)
        scaled_pix_map = orig_pix_map.scaled(QSize(400, 400),
                                             Qt.AspectRatioMode.KeepAspectRatio)
        self.img_original.setPixmap(scaled_pix_map)

    def filtro_img_click(self):
        if not self.ruta:
            self.error_label.setStyleSheet('background-color:red; font: 15pt Times New Roman')
            self.error_label.setText('¡No hay ninguna imagen \n'
                                     ' para transformar!')
        else:
            img_no_filtro = cv2.imread(self.ruta)
            img_no_filtro = cv2.cvtColor(img_no_filtro, cv2.COLOR_RGB2GRAY)
            c = self.parametro.value()
            img_no_filtro = img_no_filtro.astype(float)
            img_filtro = c * np.log(img_no_filtro + 1)
            img_filtro = img_filtro.astype(np.uint8)
            img_filtro = QImage(img_filtro, img_filtro.shape[1], img_filtro.shape[0],
                                img_filtro.strides[0], QImage.Format.Format_Grayscale8)
            self.pix_map_filtro = QPixmap.fromImage(img_filtro)
            scaled_pix_map_log = self.pix_map_filtro.scaled(QSize(400, 400),
                                                       Qt.AspectRatioMode.KeepAspectRatio)
            self.img_final.setPixmap(scaled_pix_map_log)
            self.bandera_img_final = True

    def filtro_opt_click(self):
        if not self.ruta:
            self.error_label.setStyleSheet('background-color:red; font: 15pt Times New Roman')
            self.error_label.setText('¡No hay ninguna imagen \n'
                                     ' para transformar!')
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
            self.pix_map_filtro = QPixmap.fromImage(img_filtro)
            scaled_pix_map_opt = self.pix_map_filtro.scaled(QSize(400, 400),
                                                       Qt.AspectRatioMode.KeepAspectRatio)
            self.img_final.setPixmap(scaled_pix_map_opt)
            self.bandera_img_final = True

    def save_file(self):
        if self.bandera_img_final is False:
            self.error_label.setStyleSheet('background-color:red; font: 15pt Times New Roman')
            self.error_label.setText('¡No hay ninguna imagen \n'
                                     ' para guardar!')
        else:
            self.error_label.clear()
            self.error_label.setStyleSheet('background-color:none')
            save_img = self.pix_map_filtro
            save_name = QFileDialog.getSaveFileName(self, 'Guardar archivo', '', '*.jpg')
            save_img.save(save_name[0], 'JPG')


    def clear_img_original(self):
        self.img_original.clear()

    def clear_img_final(self):
        self.img_final.clear()


app = QApplication(sys.argv)

ventana = VentanaPrincipal()
ventana.show()

sys.exit(app.exec())

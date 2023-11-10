from PyQt6.QtWidgets import (QApplication, QPushButton, QMainWindow, QFileDialog,
                             QLabel, QWidget, QDoubleSpinBox, QGridLayout, QHBoxLayout,
                             QStyle, QToolBar, QMessageBox)
from PyQt6.QtGui import QPixmap, QImage, QAction, QKeySequence, QIcon
from PyQt6.QtCore import QSize, Qt
import sys
import cv2
import numpy as np


class VentanaFullScreen(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Imagen transformada')
        self.setWindowIcon(QIcon('icons/image.png'))
        self.setMaximumSize(QSize(1080, 720))


class VentanaPrincipal(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Transformación logaritmo")
        self.setFixedSize(QSize(1280, 720))
        icon = self.style().standardIcon(QStyle.StandardPixmap.SP_DesktopIcon)
        self.setWindowIcon(icon)

        self.img_original = QLabel(self)
        self.img_final = QLabel(self)
        self.pix_map_filtro = QPixmap()

        self.bandera_img_final = False
        self.ruta = None
        self.img_fullscreen = None

        accion_abrir_file = QAction(QIcon('icons/folder-open-document.png'), 'Abrir imagen', self)
        accion_abrir_file.setToolTip('Ctrl + a')
        accion_abrir_file.triggered.connect(self.select_img_click)
        accion_abrir_file.setShortcut(QKeySequence('Ctrl+A'))

        accion_save_file = QAction(QIcon('icons/disk-black.png'), 'Guardar imagen transformada', self)
        accion_save_file.setToolTip('Ctrl + s')
        accion_save_file.triggered.connect(self.save_file_click)
        accion_save_file.setShortcut(QKeySequence('Ctrl+S'))

        accion_img_fullscreen = QAction(QIcon('icons/image.png'), 'Mostrar imagen transformada', self)
        accion_img_fullscreen.setToolTip('Ctrl + f')
        # accion_img_fullscreen.setCheckable(True)
        accion_img_fullscreen.triggered.connect(self.show_img_fullscreen_toggle)
        accion_img_fullscreen.setShortcut(QKeySequence('Ctrl+F'))

        accion_clear_img_original = QAction(QIcon('icons/cross.png'), 'Borrar imagen original', self)
        accion_clear_img_original.setToolTip('Ctrl + d')
        accion_clear_img_original.triggered.connect(self.clear_img_original_click)
        accion_clear_img_original.setShortcut(QKeySequence('Ctrl+D'))

        accion_clear_img_filtro = QAction(QIcon('icons/cross-circle.png'),
                                          'Borrar imagen transformada', self)
        accion_clear_img_filtro.setToolTip('Ctrl+Alt+d')
        accion_clear_img_filtro.triggered.connect(self.clear_img_final_click)
        accion_clear_img_filtro.setShortcut(QKeySequence('Ctrl+Alt+D'))

        accion_clear_all = QAction(QIcon('icons/cross-circle-frame.png'), 'Borrar todo', self)
        accion_clear_all.setToolTip('Ctrl + Shift + d')
        accion_clear_all.setShortcut(QKeySequence('Ctrl+Shift+d'))
        accion_clear_all.triggered.connect(self.clear_img_original_click)
        accion_clear_all.triggered.connect(self.clear_img_final_click)

        toolbar = QToolBar('Barra de herramientas')
        toolbar.setIconSize(QSize(32, 32))
        toolbar.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextBesideIcon)
        self.addToolBar(toolbar)
        toolbar.addAction(accion_abrir_file)
        toolbar.addAction(accion_save_file)
        toolbar.addAction(accion_img_fullscreen)
        toolbar.addAction(accion_clear_img_original)
        toolbar.addAction(accion_clear_img_filtro)
        toolbar.addAction(accion_clear_all)

        boton_select_img = QPushButton("Abrir imagen")
        boton_select_img.setFixedSize(QSize(100, 50))
        boton_select_img.clicked.connect(self.select_img_click)

        boton_filtro_log = QPushButton("Aplicar filtro")
        boton_filtro_log.setFixedSize(QSize(100, 50))
        boton_filtro_log.setShortcut(QKeySequence('Ctrl+L'))
        boton_filtro_log.clicked.connect(self.filtro_img_click)

        boton_filtro_opt = QPushButton("Aplicar filtro \n"
                                       "óptimo")
        boton_filtro_opt.setFixedSize(QSize(100, 50))
        boton_filtro_opt.setShortcut(QKeySequence('Ctrl+O'))
        boton_filtro_opt.clicked.connect(self.filtro_opt_click)

        self.parametro = QDoubleSpinBox()
        self.parametro.setRange(1, 100)
        self.parametro.setPrefix('C=')
        self.parametro.setValue(40)
        self.parametro.setFixedSize(QSize(75, 20))

        tuto_label = QLabel('Seleccione una imagen para \n'
                            'aplicar la transformación logaritmo. \n'
                            'Mientras más aumente el factor C, \n'
                            'aumentara el brillo de la imagen. \n'
                            'Ctrl + L aplica el filtro seleccionado. \n'
                            'Ctrl + O aplica el filtro óptimo.'
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

    def filtro_img_click(self):
        if not self.ruta:
            QMessageBox.warning(self, 'Error', '¡No hay ninguna imagen para transformar!')

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
            QMessageBox.warning(self, 'Error', '¡No hay ninguna imagen para transformar!')
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

    def save_file_click(self):
        if self.bandera_img_final is False:
            QMessageBox.warning(self, 'Error', '¡No hay ninguna imagen para guardar!')
        else:
            save_img = self.pix_map_filtro
            save_name = QFileDialog.getSaveFileName(self, 'Guardar archivo', '', '*.jpg')
            save_img.save(save_name[0], 'JPG')

    def show_img_fullscreen_toggle(self):
        if not self.bandera_img_final:
            QMessageBox.warning(self, 'Error', '¡No hay ninguna imagen para mostrar!')
        else:
            self.img_fullscreen = VentanaFullScreen()
            img_fullscreen_label = QLabel(self)
            img_fullscreen_label.setPixmap(self.pix_map_filtro.scaled(QSize(1080, 720),
                                                                      Qt.AspectRatioMode.KeepAspectRatio))
            self.img_fullscreen.setCentralWidget(img_fullscreen_label)
            self.img_fullscreen.show()

    def clear_img_original_click(self):
        self.img_original.clear()
        self.ruta = None

    def clear_img_final_click(self):
        self.img_final.clear()
        self.bandera_img_final = False


app = QApplication(sys.argv)

ventana = VentanaPrincipal()
ventana.show()

sys.exit(app.exec())

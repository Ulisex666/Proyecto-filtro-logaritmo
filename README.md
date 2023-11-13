# Proyecto-filtro-logaritmo
Creación de una interfaz visual utilizando PyQT6 que permita aplicar la transformación logaritmo a las imágenes que se deseen, aplicando esta transformación con las funciones de la paquetería OpenCV2.

## Introducción
Con la realización de este programa se espera obtener una herramienta que pueda ser útil a la hora de trabajar con visión por computadora, por lo que se empezará definiendo este concepto. La visión por computadora o visión artificial es una rama de la inteligencia artificial que se encarga del análisis de imágenes digitales, videos y otros medios visuales utilizando computadoras y sistemas informáticos. La visión digital se inspira en la visión humana, pero con la diferencia de la capacidad de las computadoras de analizar datos de forma extremadamente rápida a comparación del tiempo que le toma a un humano, por lo que se pueden analizar miles de imágenes por minuto. 

Para que la computadora sea capaz de recibir la información visual necesaria se necesita de dispositivos como cámaras fotográficas o de vídeo, sensores de diversos tipos, procesadores y software especializado en este tipo de técnicas. En suma a esto, se necesita una gran cantidad de datos para entrenar a la computadoras. Actualmente existen una gran cantidad de aplicaciones para estas tecnologías, destacando el reconocimiento facil con propósitos de seguridad o de autenticación, por ejemplo, el sistema Face ID de Apple que le permite a un usuario desbloquear su iPhone simplemente escaneando su rostro.

Otro elemento importante en el desarrollo de este proyecto fueron las interfaces gráficas de usuario o GUI por sus siglas en inglés. Estos son programas que permiten la interacción entre un usuario y su computador de forma sencilla, ya que se basa en el uso de imágenes y elementos gráficos para la interacción con el programa. Son considerados como una evolución de las interfaces basadas en líneas de comando. Se suelen utilizar diferentes widgets que permiten la interacción "correcta" entre el usuario y el programa, por ejemplo, una caja de texto para ingresar un nombre de usuario, spinboxes para elegir entre una cantidad determinada de datos númericos, etc.

El uso de interfaces visuales permite hacer más accesibles las aplicaciones para personas con poco conocimiento del uso de computadoras, debido a su uso de elementos visuales fáciles de entender (suponiendo que se hayan desarrollado de forma adecuada).

## Materiales
El lenguaje de programación con el que se desarrollo este programa fue Python 3.11, eligiendo un enfoque de programación de objetos ya que este permite un mejor desarrollo de la GUI. El uso de este lenguaje se debe a la facilidad para programar en este lenguaje, su enfoque multiparadigma y la existencia de muchas paqueterías para el desarrollo de IA. Se utilizó el entorno de programación PyCharm 2023.2.3 con una licencia de estudiante, lo que permitió un desarrollo más eficaz del programa, aunque se encontraron algunos errores a la hora de utilizar algunas librerías.

Para el desarrollo de la GUI se ocupó la paqueteria PyQt6, que permite utilizar el software Qt con el lenguaje de Python. Se utilizaron muchos de los widgets disponibles, como Qlabel para mostrar texto e imágenes, QDoubleSpinBox para permitir la selección de un parámetro numérico, y también se utilzaron las QAction para desarrollar una barra de herramientas con muchos atajos de teclado para un uso más rápido del programa.

OpenCV2 fue la librería que se utilizó para aplicar el filtro a las imágenes. Su uso fue limitado, ya que solamente se necesitó para poder abrir las imágenes como una lista de vectores. Para aplicar la transformación en sí se utilizó la función logaritmo de la librería numpy. Un problema importante a la hora de leer imágenes es que OpenCV2 no soporta rutas de imágenes que contengan tildes, lo que no permite utilizar las imágenes que se encuentran en la carpeta "Imágenes" del computador.

Finalmente, aunque se permitió abrir imágenes con otros formatos, las imágenes con las que se puso a prueba el programa se encuentran en formato TIFF. La ventaja de este formato comparado con otros es que mantiene la imagen con una calidad muy alta y no tiene ninguna perdida, lo que es importante para la visión por computadora. Sin embargo, tiene la desventaja de que es mucho más pesado que otros formatos como el .jpg o .png, lo que impide su uso para conjuntos muy grandes de datos visuales.

## Método
Para poder desarrollar el programa, primero fue necesario investigar qué es la transformación logaritmo y para que se utiliza.

### Transformación visual logaritmo.
Empecemos aclarando que esta transformación solo se aplica a imágenes en escala de grises. Aunque se desarrolló el programa para permitir trabajar con imágenes a color, estas son transformadas a grayscale de 8 bits utilizando cv2, como por ejemplo en la lína de código

``` python
 img_no_filtro = cv2.cvtColor(img_no_filtro, cv2.COLOR_RGB2GRAY)
```

Así, a la hora de abrir la imagen con cv2, el programa la lee como una matriz de n*m elementos, donde n es el alto y m el ancho de la imagen, y cada elemento es un pixel. A cada pixel se le asigna un valor entre 0 y 255, que corresponde a su intensidad. Con esto, la fórmula utilizada para la transformación logaritmo es 

$$
\text{pixel transformado} = c \cdot \log(r + 1)
$$

Donde $r$ es la intensidad del pixel original y $c$ es un parámetro a elegir. Recordemos que $\log 0$ no está definido, por lo que es necesario sumar 1 a todos los valores para el caso en el que un pixel tenga intensidad 0. El valor de la base del logaritmo nos es indiferente en este caso, por lo que se toma base 10. Para entender que hace el parámetro $c$, es necesario analizar la transformación a profundidad.

Veamos que le sucede a los valores en el rango $[0, 255]$ 

<img src="https://github.com/Sesilu00/Proyecto-filtro-logaritmo/assets/142864667/75636eae-85f7-49e7-92ff-cff72e8c02f6" alt="Transformación sin parámetro C" width="500"/>

Notemos que los valores se quedan en el rango $[0, 2.5)$, es decir, todas toman valores muy oscuros. Si no multiplicaramos por el factor de ajuste $c$, todas las imágenes se verían como una imagen en negro. Así, para elegir $c$ de forma óptima, es necesario que mande a el elemento con la mayor intensidad en la imagen original a una intensidad de 255 en la imagen final. Esto es

$$
255 = c \cdot \log(r_{max} + 1)
$$

o, despejando a c

$$
c = \dfrac{\log(r_{max} + 1)}{255}.
$$

Para tener una idea más visual de lo que hace esta transformación, veamos que le sucede a la siguiente imagen:

![grayscale](https://github.com/Sesilu00/Proyecto-filtro-logaritmo/assets/142864667/4c3df90b-5c59-427d-8109-a3ae214d3085)

Esta es una banda que representa todos los valores de intensidad en escala de grises, empezando con 0 en la izquierda y llegando a 255 en la derecha. Bajo la transformación con un parámetro óptimo, esta banda se ve de la siguiente forma:


![grayscale_log](https://github.com/Sesilu00/Proyecto-filtro-logaritmo/assets/142864667/2b4c8d94-e5ea-47ad-8d14-ce47703a6f2f)

Resulta claro que la imagen es mucho más brillante, con tonos más claros. Esto toma sentido considerando que los valores de intensidad 0 y 15 se transforman a 0 y 127 (se toman valores enteros después de aplicar la transformación). Así, dos valores que apenas tendrían diferencia a simple vista toman una diferencia muy grande, que permitirá apreciar un mejor contraste en la imagen transformada. Sim embargo, en el otro extremo, pixeles con valores originales de 205 y 255 se transforman en 245 y 255. Así, dos pixeles que tendrían una gran diferencia en la imagen original se ven idénticos después de la transformación.

Por lo tanto, la transformación visual logaritmo nos permite apreciar con más claridad los detalles en las zonas más oscuras de la imagen, pero a cambio se pierden aquello en las zonas más claras. Entonces, este filtro es muy útil a la hora de aclarar imágenes que por distintos motivos se vean más oscuras de lo que se desea, por ejemplo a la hora de tomar fotos a contraluz.

## Mockup e implementación

Teniendo en cuenta como funciona la transformación, se diseñó el siguiente bosquejo o mockup para la GUI:

![mockup](https://github.com/Sesilu00/Proyecto-filtro-logaritmo/assets/142864667/59b43aff-c783-4917-928f-15b3eb8e1e04)

Para empezar se decidió que eran necesarios 3 botones, uno que permita seleccionar cualquier imagen soportada por el programa, otro que permita aplicar el filtro con el parámetro $c$ seleccionado y uno que permita aplicar el parámetro $c$ óptimo de forma automática. El widget *QPushButton* fue ideal para esta aplicación. A su vez, se necesitaba una forma de poder seleccionar el parámetro $c$ de forma que se limitara solamente a valores reales, y se eligió el widget *QDoubleSpinBox* limitado a los valores en el rango $(0, 100)$. Se podría considerar innecesario el dar la libertad de elegir el parámetro $c$ de forma libre si existe una forma matemática de optimizarlo, pero se decidió dar esta opción para pdoer apreciar de forma más clara como funciona la transformación.

También se pensó en mostrar la imagen original y la imagen tranformada una al lado de la otra, para poder apreciar claramente el cambio. A la hora de la implementación se decidió mostrar las imágenes a color sin transformalas a escala de grises. Además, se fijo el tamaño de la ventana del programa a 720 x 1080 pixeles, con la idea de que no se llene la pantalla del computador a la hora de ejecutar el programa. También se limitó el tamaño de las imágenes a 400 x 400 pixeles, para evitar abarcar todo el espacio del programa.

Para el funcionamiento del programa se utiliza un widget `QFileDialog.getOpenFileName` para obtener la ruta del archivo en el computador. Con esto, se genera un *QPixMap* y se le asigna a una *QLabel*, que es la imagen original que se muestra en el programa. Cuando se presiona el botón 'Aplicar filtro':
1. Se abre la ruta de la imagen con cv2, que la lee como una matriz.
2. Se tranforma a formato de escala de grises utilizando cv2.
3. Se utiliza numpy para aplicar la fórmula tomando el valor de $c$ dado.
4. Esta matriz de reales se transforma a una matriz de enteros.
5. Se genera una *QImage* utilizando esta matriz.
6. Se tranforma esta imagen a un *QPixMap* y se ajusta su tamaño.
7. Se le asigna este mapa de pixeles a una *QLabel* y esta es la imagen transformada que se muestra en el programa.

El botón 'Aplicar filtro óptimo' funciona de forma casi idéntica, la única diferencia es que el parámetro $c$ se calcula automáticamente con la fórmula antes dada.

## Resultados

A continuación se muestra una captura de pantalla de la aplicación después de aplicar el filtro óptimo.

![app_opt](https://github.com/Sesilu00/Proyecto-filtro-logaritmo/assets/142864667/dbb6cd20-8a28-4e3e-89d2-d5901073f84e)

La mayor diferencia entre el resultado final y el mockup es la adición de una barra de herramientas, a la que se le agregaron atajos de teclado que permiten utilizar el programa con mayor facilidad. Las funciones que se agregaron que no eran parte del diseño original es la capacidad de borrar la imagen original, borrar la imagen transformada, borrar ambas imágenes, guardar la imagen transformada y mostrar la imagen transformada en una nueva ventana para poder apreciarla con mayor claridad. También se agregaron mensajes de error para algunas situaciones en específico. A continuación se muestran capturas de la búsqueda de imágenes en la aplicación, una imagen tranformada con un parámetro muy alto, un mensaje de error, una imagen en tamaño completo y un ejemplo de una imagen que se guardo después de la transformación:

![app_open_file](https://github.com/Sesilu00/Proyecto-filtro-logaritmo/assets/142864667/869335ea-6afc-4ec0-844b-4a3a97cb9032)

![app_mal_parametro](https://github.com/Sesilu00/Proyecto-filtro-logaritmo/assets/142864667/0a6885b2-f340-4c18-a0a9-09aec6a35a52)

![app_error](https://github.com/Sesilu00/Proyecto-filtro-logaritmo/assets/142864667/e9fe19a3-1309-4ff2-8796-6015988a19a3)

![app_fullscreen](https://github.com/Sesilu00/Proyecto-filtro-logaritmo/assets/142864667/958edc8e-1acb-443f-9beb-f703d0ad41c6)

<img src="https://github.com/Sesilu00/Proyecto-filtro-logaritmo/assets/142864667/85814776-fb0c-4087-9878-8f374714ff93" alt="Rosa transformada" width="500"/>

Como se menciono antes, y como se aprecia en las capturas, a pesar de que el proyecto se inició con la idea de aplicar la transformación a imágenes en formato TIFF, esto se amplio para poder transformar imágenes en formato JPG, JPEG y PNG. Se consiguieron implementar todas las funcionalidades que se buscaban e inclusive varias que no se habían previsto pero resultan útiles para el análisis de imágenes. Por lo tanto, este programa se puede considerar un éxito.

## Referencias y atribuciones

Algunos iconos por [Yusuke Kamiyamane](https://p.yusukekamiyamane.com/). Bajo una Licencia Creative Commons Atribución 3.0.
Para la investigación sobre la transformación logaritmo se consultó la página [Packt Pub](https://subscription.packtpub.com/book/data/9781784391454/1/ch01lvl1sec16/logarithmic-transformations). Se consultaron las páginas [Clandestina HDS](https://clandestina-hds.com/curso-pyqt.html) y [Phyton GUIs](https://www.pythonguis.com/pyqt6/) para la implementación de PyQT6.

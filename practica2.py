import xml.etree.ElementTree as ET
arbolXML = ET.parse('almacen1.xml') #carga el archivo almacen
raiz = arbolXML.getroot()

import sys
from PySide6.QtCore import *
from PySide6.QtGui import QPainter, QBrush, QColor
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QApplication, QPushButton, QLineEdit, QLabel, QComboBox,QWidget


class Figura(QWidget):
    # Clase Figura derivada de la clase Widget para programar el comportamiento
    # de un widget personalizado
    def __init__(self,parent=None):  # Constructor
        QWidget.__init__(self, parent)  # Llama al constructor de la clase base
        self.__puntos = []  # Crea una lista para las posiciones
        self.estado=0
        self.temporizador = QTimer()  # Crea el temporizador
        self.listaparpadeo = [] #lista de puntos a parpadear
        self.temporizador.timeout.connect(buclemultiple)  # Asocia el evento timeout a la función

    def mousePressEvent(self, evento):  # Se ejecuta cada vez que se pulsa el ratón dentro del widget
        self.temporizador.stop()
        x = int(evento.position().x())  # Obtiene la coordenada X del ratón
        y = int(evento.position().y())  # Obtiene la coordenada Y del ratón
        for r in self.listaparpadeo: #restaura los valores que hasta ahora estaba parpadeando
            if not r in self.__puntos:
                self.__puntos.append(r)
        self.listaparpadeo=[]
        for r in self.__puntos: #busca si hay unas coordenadas que coincidan con un palet dentro de unos márgenes
            if r[0]<=x<=r[0]+10 and r[1]<=y<=r[1]+10:
                self.listaparpadeo.append(r)
                self.estado=0
                self.temporizador.start(500)
                resultado.setText('Palet:{} Producto:{} Litros:{} Tipo:{}  Fecha de fabricación:{}  Estantería:{} Balda:{} Posición:{} {}'.format(r[13],r[5],r[6],r[7],r[8],r[9],r[10],r[11],r[12]))


    def actualiza(self, x,y,color,id,litros,tipo,fabricacion,estanteria,balda,palet,delante,total):  #Se ejecuta al arrancar el programa para marcar los puntos a pintar
        n=0
        contador=0
        for r in color: #busca los colores de cada producto
            if n == 2:
                B=int(color[contador:])
            if n==1 and r==',':
                G=int(color[coma1+1:contador])
                n=2
            if n==0 and r==',':
                R=int(color[0:contador])
                n=1
                coma1=contador
            contador += 1
        self.__puntos.append([x,y,R,G,B,id,litros,tipo,fabricacion,estanteria,balda,palet,delante,total])  # Añade la posición del ratón a la lista
        self.update()
        # Llama al método update() recibido mediante herencia desde la clase base. Se utiliza para
        # provocar el redibujado del widget.

    def arranqueparpadeo(self,tipo): #busca cuales son los palets que deben parpadear
        self.temporizador.stop()
        for r in self.listaparpadeo: #restaura los valores que hasta ahora estaba parpadeando
            if not r in self.__puntos:
                self.__puntos.append(r)
        self.listaparpadeo = []
        if not tipo == 'Nada': #si no se selecciona Nada entonces busca los productos que encajen con el dato introducido
            for r in self.__puntos:
                if tipo==r[7] :
                    self.listaparpadeo.append(r)
                    self.estado=0
                    self.temporizador.start(500)
                if tipo==r[5] :
                    self.listaparpadeo.append(r)
                    self.estado=0
                    self.temporizador.start(500)
        else:
            resultado.setText('Todos los productos Litros:{}  Palets usados:{}'.format(litros, palets))
        self.update()

    def buclemultiple(self): #función que alterna entre 2 estados
        for r in self.listaparpadeo:
            if self.estado==0: #en este estado borra de la lista el/los puntos a parpadear
                self.__puntos.remove(r)
            else: #en este estado añade a la lista el/los puntos a parpadear
                self.__puntos.append(r)
        if self.estado == 0: #cambia el estado para que en el siguiente bucle haga lo contrario
            self.estado = 1
        else:
            self.estado = 0
        self.update()

    def cancela(self): #función que desactiva cualquier selección
        self.temporizador.stop()
        for r in self.listaparpadeo:  #restaura los valores que hasta ahora estaba parpadeando
            if not r in self.__puntos:
                self.__puntos.append(r)
        self.update()

    def buscar(self,num): #busca el número de palet que corresponde
        self.temporizador.stop()
        for r in self.listaparpadeo: #restaura los valores que hasta ahora estaba parpadeando
            if not r in self.__puntos:
                self.__puntos.append(r)
        self.listaparpadeo = []
        for r in self.__puntos: #busca cual es el palet que corresponde con el número
            if r[13]==num:
                resultado.setText('Palet:{} Producto:{} Litros:{} Tipo:{}  Fecha de fabricación:{}  Estantería:{} Balda:{} Posición:{} {}'.format(r[13], r[5], r[6], r[7], r[8], r[9], r[10], r[11], r[12]))
                self.listaparpadeo.append(r)
                self.estado = 0
                self.temporizador.start(500)
            else:
                resultado.setText('Palet no encontrado')
        self.update()

    def paintEvent(self, e):  # Se ejecuta cuando es necesario redibujar el widget
        pintor = QPainter(self)  # Objeto para dibujar en el widget
        brocha = QBrush()  # Expresa un color para rellenar una zona
        brocha.setColor(QColor(255, 255, 255))
        brocha.setStyle(Qt.SolidPattern)  # Patrón de relleno de un único color
        pos=[23,153,283,413]
        coordprevia=23
        for y in pos:
            valor=y
            while not valor==(coordprevia+8*15):
                rectangulo = QRect(28, valor, 360, 13)
            # Rectángulo con esquina superior izquierda en el punto, con ancho=alto=10
                pintor.fillRect(rectangulo, brocha)
                rectangulo = QRect(478, valor, 360, 13)
                # Rectángulo con esquina superior izquierda en el punto, con ancho=alto=10
                pintor.fillRect(rectangulo, brocha)
                valor+=15
            coordprevia=y+8*15+10
        for punto in self.__puntos:  # Para cada punto en la lista ...
            brocha.setColor(QColor(punto[2], punto[3], punto[4]))  # Establece color
            brocha.setStyle(Qt.SolidPattern)  # Patrón de relleno de un único color
            rectangulo = QRect(punto[0], punto[1], 10, 10)
            # Rectángulo con esquina superior izquierda en el punto, con ancho=alto=10
            pintor.fillRect(rectangulo, brocha)  # Dibuja el rectángulo


def buclemultiple(): #clase intermediaria que asegura que el bucle del parpadeo se mantiene
    Figura.buclemultiple(figura)

def selecciontipo(): #clase intermediaria al seleccionar un tipo de producto en el desplegable
    global cant
    Figura.arranqueparpadeo(figura,tproducto.currentText())
    for r in cant:
        if r==tproducto.currentText():
            resultado.setText('{} Litros:{}  Palets usados:{}'.format(r,cant[r][0],cant[r][1]))
def seleccionproducto(): #clase intermediaria al seleccionar un producto en el desplegable
    global dic
    Figura.arranqueparpadeo(figura,producto.currentText())
    for r in dic:
        if r==producto.currentText():
            resultado.setText('{} Tipo:{} Litros:{} Palets usados:{}'.format(r, dic[r][2],dic[r][0], dic[r][1]))
def cancela(): #clase intermediaria al cancelar selección
    Figura.cancela(figura)
    resultado.setText('Todos los productos Litros:{}  Palets usados:{}'.format(litros, palets))
def buscar(): #clase intermediaria al buscar un número de palet
    try:
        Figura.buscar(figura,int(editorpalet.text()))
    except Exception as EX:
        resultado.setText('Debes meter un número')


aplicacion = QApplication(sys.argv)
archivoUi = QFile("practica2.ui") # Crea un objeto para manejar el archivo interfaz.ui
archivoUi.open(QFile.ReadOnly) # Lo abre para lectura
cargador = QUiLoader() # Crea un objeto para leer el contenido del archivo
cargador.registerCustomWidget(Figura) # Registra la clase Figura para un widget personalizado
ventana = cargador.load(archivoUi) # Lee su contenido y lo guarda en un objeto
archivoUi.close()

editorpalet = ventana.findChild(QLineEdit, "editorpalet")
cancelar = ventana.findChild(QPushButton, "cancelar")
buscarpalet= ventana.findChild(QPushButton, "buscarpalet")
resultado = ventana.findChild(QLabel, "resultado")
producto=ventana.findChild(QComboBox,'producto')
tproducto=ventana.findChild(QComboBox,'tproducto')
figura = ventana.findChild(Figura, "figura")

color={} #productos con color y tipo
for r in raiz[1]:
    for i in raiz[0]:
        if r.attrib['idTipoProducto']==i.attrib['id']:
            color[r.attrib['id']] = [i.attrib['color'],r.attrib['idTipoProducto']]

tipos=['Nada'] #lista para el desplegable de tipos de producto
productos=['Nada'] #lista para el desplegable de productos
for r in color:
    if not (color[r][1] in tipos):
        tipos.append(color[r][1])
    if not (r in productos):
        productos.append(r)
for r in tipos:
    tproducto.addItem(r)
for r in productos:
    producto.addItem(r)

litros=0 #contador de litros totales
palets=0 #contador de palets totales
altura=130 #altura a la que se pintará el cuadrado
dic={} #productos y características
cant={} #cantidad de cada tipo de producto
numestanteria=1
for estanteria in raiz[2]: #recorre todo el archivo para crear una lista de posiciones y datos
    numbalda=1
    for balda in estanteria:
        if altura==10:
            altura=260
        if altura==140:
            altura=390
        if altura==270:
            altura=520
        despldelante=30 #posición inicial en el eje x de delante
        despldetras=480 #posición inicial en el eje x de detrás
        coord=1
        for palet in balda:
            while not (int(palet.attrib['posicion'])==coord): #calcula en que distancia en x que debe estar el palet a visualizar
                coord+=1
                despldelante += 15
                despldetras += 15
            for r in color:
                if palet.attrib['idProducto']==r:
                    if palet.attrib['delante']=='True':
                        Figura.actualiza(figura,despldelante,altura,color[r][0],r,palet.attrib['litros'],color[r][1],palet.attrib['fabricacion'],numestanteria,numbalda,coord,'delante',int(palet.attrib['id']))
                    if palet.attrib['delante']=='False':
                        Figura.actualiza(figura,despldetras,altura,color[r][0],r,palet.attrib['litros'],color[r][1],palet.attrib['fabricacion'],numestanteria,numbalda,coord,'detrás',int(palet.attrib['id']))
            if palet.attrib['idProducto'] in dic:
                dic[palet.attrib['idProducto']][0]+=int(palet.attrib['litros'])
                dic[palet.attrib['idProducto']][1] +=1
            if not palet.attrib['idProducto'] in dic:
                dic[palet.attrib['idProducto']]=[int(palet.attrib['litros']),1]
            coord=1
            despldelante = 30
            despldetras = 480
            litros+=int(palet.attrib['litros'])
            palets+=1
        numbalda+=1
        altura -= 15
    numestanteria+=1

for p in raiz[1]: #añade a cada producto su tipo de producto
    for i in dic:
        if p.attrib['id'] == i:
            dic[i].append(p.attrib['idTipoProducto'])

for p in dic: #cálculo litros y palets totales y creo un diccionario con cada tipo de producto y sus características
    if dic[p][2] in cant:
        cant[dic[p][2]][0]+=dic[p][0]
        cant[dic[p][2]][1]+=dic[p][1]
    if not dic[p][2] in cant:
        cant[dic[p][2]]=[dic[p][0],dic[p][1]]


tproducto.currentIndexChanged.connect(selecciontipo)
producto.currentIndexChanged.connect(seleccionproducto)
cancelar.clicked.connect(cancela)
buscarpalet.clicked.connect(buscar)

resultado.setText('Todos los productos Litros:{}  Palets usados:{}'.format(litros,palets))

ventana.show()
sys.exit(aplicacion.exec())
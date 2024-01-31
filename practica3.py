import xml.etree.ElementTree as ET
from datetime import datetime

arbolXML = ET.parse('almacen1.xml') #carga el archivo almacen
raiz = arbolXML.getroot()

import sys
from OPCUA import OPC_UA
from PySide6.QtCore import *
from PySide6.QtGui import QPainter, QBrush, QColor, QPixmap
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QApplication, QPushButton, QLineEdit, QLabel, QComboBox, QWidget, QFontComboBox, \
    QMessageBox, QDateEdit, QCheckBox

auto1act=False
auto2act=False
op1=0
op2=0

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


    def actualiza(self, x,y,color,id,litros,tipo,fabricacion,estanteria,balda,palet,delante,numpalet):  #Se ejecuta al arrancar el programa para marcar los puntos a pintar
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
        self.__puntos.append([x,y,R,G,B,id,litros,tipo,fabricacion,estanteria,balda,palet,delante,numpalet])  # Añade la posición del ratón a la lista
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
            pal=1
            lit=0
            a=0
            for r in self.__puntos:
                if tipo==r[7] :
                    a=1
                    pal+=1
                    lit += int(r[6])
                    self.listaparpadeo.append(r)
                    self.estado=0
                if tipo==r[5] :
                    a=2
                    b=r[7]
                    pal += 1
                    lit += int(r[6])
                    self.listaparpadeo.append(r)
                    self.estado=0
            self.temporizador.start(500)
            if a==1:
                resultado.setText('{} Litros:{}  Palets usados:{}'.format(tipo,str(lit),str(pal)))
            if a==2:
                resultado.setText('{} Tipo:{} Litros:{} Palets usados:{}'.format(tipo, b,str(lit),str(pal)))
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
        self.listaparpadeo=[]
        lit=0
        pal=1
        for r in self.__puntos:
            pal += 1
            lit += int(r[6])
        resultado.setText('Todos los productos Litros:{}  Palets usados:{}'.format(str(lit), str(pal)))
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

    def extraerpalet(self):
        global op1,op2,auto2act,auto1act
        self.temporizador.stop()
        for r in self.listaparpadeo: #restaura los valores que hasta ahora estaba parpadeando
            if not r in self.__puntos:
                self.__puntos.append(r)
        self.listaparpadeo = []
        p=int(editorextraer.text())
        esta=False
        for r in self.__puntos:
            if r[-1]==p:
                esta=True
                if not auto1act:
                    clienteOPC.escribeTag('Canal.Automata1.Operacion.Origen.Balda',r[-4])
                    if r[-2]=='delante':
                        clienteOPC.escribeTag('Canal.Automata1.Operacion.Origen.Delante', True)
                    else:
                        clienteOPC.escribeTag('Canal.Automata1.Operacion.Origen.Delante', False)
                    clienteOPC.escribeTag('Canal.Automata1.Operacion.Origen.Estanteria', r[-5])
                    clienteOPC.escribeTag('Canal.Automata1.Operacion.Origen.Posicion', r[-3])
                    clienteOPC.escribeTag('Canal.Automata1.Operacion.Marcha', True)
                    clienteOPC.escribeTag('Canal.Automata1.Operacion.Operacion', 2)
                    op1=2
                    self.__puntos.remove(r)
                elif not auto2act:
                    clienteOPC.escribeTag('Canal.Automata2.Operacion.Origen.Balda', r[-4])
                    if r[-2] == 'delante':
                        clienteOPC.escribeTag('Canal.Automata2.Operacion.Origen.Delante', True)
                    else:
                        clienteOPC.escribeTag('Canal.Automata2.Operacion.Origen.Delante', False)
                    clienteOPC.escribeTag('Canal.Automata2.Operacion.Origen.Estanteria', r[-5])
                    clienteOPC.escribeTag('Canal.Automata2.Operacion.Origen.Posicion', r[-3])
                    clienteOPC.escribeTag('Canal.Automata2.Operacion.Marcha', True)
                    clienteOPC.escribeTag('Canal.Automata2.Operacion.Operacion', 2)
                    op2=2
                    self.__puntos.remove(r)
                else:
                    QMessageBox.warning(ventana, "Error", "Todos los transelevadores ocupados")
        if not esta:
            QMessageBox.warning(ventana, "Error", "Palet no encontrado")
        figura.cancela()
        self.update()

    def introduccion(self,tipoproducto,producto,fecha,numpalet,litros,estanteria,balda,posicion,delante,color):
        global op1, op2, auto2act, auto1act
        self.temporizador.stop()
        for r in self.listaparpadeo:  # restaura los valores que hasta ahora estaba parpadeando
            if not r in self.__puntos:
                self.__puntos.append(r)
        self.listaparpadeo = []
        esta=False
        if delante:
            com ='delante'
        else:
            com = 'detrás'
        for r in self.__puntos:
            if r[-5]==estanteria and r[-4]==balda and r[-3]==posicion and com==r[-2]:
                esta=True
        if esta:
            QMessageBox.warning(ventana, "Error", "Posición ya ocupada")
        else:
            n = 0
            contador = 0
            for r in color:  # busca los colores de cada producto
                if n == 2:
                    B = int(color[contador:])
                if n == 1 and r == ',':
                    G = int(color[coma1 + 1:contador])
                    n = 2
                if n == 0 and r == ',':
                    R = int(color[0:contador])
                    n = 1
                    coma1 = contador
                contador += 1
            altura = 130  # altura a la que se pintará el cuadrado
            for est in range(1,5):
                for bal in range(1,9):
                    if altura == 10:
                        altura = 260
                    if altura == 140:
                        altura = 390
                    if altura == 270:
                        altura = 520
                    despldelante = 30  # posición inicial en el eje x de delante
                    despldetras = 480  # posición inicial en el eje x de detrás
                    for pal in range(1,25):  # calcula en que distancia en x que debe estar el palet a visualizar
                        if est==estanteria and bal==balda and pal==posicion:
                            if not auto1act:
                                clienteOPC.escribeTag('Canal.Automata1.Operacion.Destino.Balda', balda)
                                clienteOPC.escribeTag('Canal.Automata1.Operacion.Destino.Delante', delante)
                                clienteOPC.escribeTag('Canal.Automata1.Operacion.Destino.Estanteria', estanteria)
                                clienteOPC.escribeTag('Canal.Automata1.Operacion.Destino.Posicion', posicion)
                                clienteOPC.escribeTag('Canal.Automata1.Operacion.Operacion', 1)
                                clienteOPC.escribeTag('Canal.Automata1.Operacion.Marcha', True)
                                op1 = 1
                                if delante:
                                    self.__puntos.append([despldelante, altura, R, G, B, producto, litros, tipoproducto,
                                                          fecha, estanteria, balda, posicion, 'delante', numpalet])
                                else:
                                    self.__puntos.append([despldetras, altura, R, G, B, producto, litros, tipoproducto,
                                                          fecha, estanteria, balda, posicion, 'detrás', numpalet])
                            elif not auto2act:
                                clienteOPC.escribeTag('Canal.Automata2.Operacion.Destino.Balda', balda)
                                clienteOPC.escribeTag('Canal.Automata2.Operacion.Destino.Delante', delante)
                                clienteOPC.escribeTag('Canal.Automata2.Operacion.Destino.Estanteria', estanteria)
                                clienteOPC.escribeTag('Canal.Automata2.Operacion.Destino.Posicion', posicion)
                                clienteOPC.escribeTag('Canal.Automata2.Operacion.Operacion', 1)
                                clienteOPC.escribeTag('Canal.Automata2.Operacion.Marcha', True)
                                op2 = 1
                                if delante:
                                    self.__puntos.append([despldelante, altura, R, G, B, producto, litros, tipoproducto,
                                                          fecha, estanteria, balda, posicion, 'delante', numpalet])
                                else:
                                    self.__puntos.append([despldetras, altura, R, G, B, producto, litros, tipoproducto,
                                                          fecha, estanteria, balda, posicion, 'detrás', numpalet])
                            else:
                                QMessageBox.warning(ventana, "Error", "Todos los transelevadores ocupados")
                        despldelante += 15
                        despldetras += 15
                    altura -= 15
        self.update()

    def mover(self,palet,estanteria,balda,posicion,delante):
        global op1, op2, auto2act, auto1act
        esta=False
        self.temporizador.stop()
        for r in self.listaparpadeo:  # restaura los valores que hasta ahora estaba parpadeando
            if not r in self.__puntos:
                self.__puntos.append(r)
        self.listaparpadeo = []
        for r in self.__puntos:
            if r[-2] == 'delante':
                com = True
            else:
                com = False
            if r[-5] == estanteria and r[-4] == balda and r[-3] == posicion and com == delante:
                esta = True
        if esta:
            QMessageBox.warning(ventana, "Error", "Posición ya ocupada")
        else:
            for r in self.__puntos:
                if r[-1]==palet:
                    altura = 130  # altura a la que se pintará el cuadrado
                    for est in range(1, 5):
                        for bal in range(1, 9):
                            if altura == 10:
                                altura = 260
                            if altura == 140:
                                altura = 390
                            if altura == 270:
                                altura = 520
                            despldelante = 30  # posición inicial en el eje x de delante
                            despldetras = 480  # posición inicial en el eje x de detrás
                            for pal in range(1, 25):  # calcula en que distancia en x que debe estar el palet a visualizar
                                if est == estanteria and bal == balda and pal == posicion:
                                    if delante:
                                        if not auto1act:
                                            clienteOPC.escribeTag('Canal.Automata1.Operacion.Origen.Balda', r[-4])
                                            if r[-2] == 'delante':
                                                clienteOPC.escribeTag('Canal.Automata1.Operacion.Origen.Delante', True)
                                            else:
                                                clienteOPC.escribeTag('Canal.Automata1.Operacion.Origen.Delante', False)
                                            clienteOPC.escribeTag('Canal.Automata1.Operacion.Origen.Estanteria', r[-5])
                                            clienteOPC.escribeTag('Canal.Automata1.Operacion.Origen.Posicion', r[-3])
                                            clienteOPC.escribeTag('Canal.Automata1.Operacion.Destino.Balda', balda)
                                            clienteOPC.escribeTag('Canal.Automata1.Operacion.Destino.Delante', delante)
                                            clienteOPC.escribeTag('Canal.Automata1.Operacion.Destino.Estanteria',
                                                                  estanteria)
                                            clienteOPC.escribeTag('Canal.Automata1.Operacion.Destino.Posicion',
                                                                  posicion)
                                            clienteOPC.escribeTag('Canal.Automata1.Operacion.Marcha', True)
                                            clienteOPC.escribeTag('Canal.Automata1.Operacion.Operacion', 3)
                                            op1 = 3
                                        elif not auto2act:
                                            clienteOPC.escribeTag('Canal.Automata2.Operacion.Origen.Balda', r[-4])
                                            if r[-2] == 'delante':
                                                clienteOPC.escribeTag('Canal.Automata2.Operacion.Origen.Delante', True)
                                            else:
                                                clienteOPC.escribeTag('Canal.Automata2.Operacion.Origen.Delante', False)
                                            clienteOPC.escribeTag('Canal.Automata2.Operacion.Origen.Estanteria', r[-5])
                                            clienteOPC.escribeTag('Canal.Automata2.Operacion.Origen.Posicion', r[-3])
                                            clienteOPC.escribeTag('Canal.Automata2.Operacion.Destino.Balda', balda)
                                            clienteOPC.escribeTag('Canal.Automata2.Operacion.Destino.Delante', delante)
                                            clienteOPC.escribeTag('Canal.Automata2.Operacion.Destino.Estanteria',
                                                                  estanteria)
                                            clienteOPC.escribeTag('Canal.Automata2.Operacion.Destino.Posicion',
                                                                  posicion)
                                            clienteOPC.escribeTag('Canal.Automata2.Operacion.Marcha', True)
                                            clienteOPC.escribeTag('Canal.Automata2.Operacion.Operacion', 3)
                                            op2 = 3
                                        else:
                                            QMessageBox.warning(ventana, "Error", "Todos los transelevadores ocupados")
                                        self.__puntos.append(
                                            [despldelante, altura, r[2], r[3], r[4], r[5], r[6], r[7],
                                             r[8], estanteria, balda, posicion, 'delante', r[-1]])
                                        self.__puntos.remove(r)
                                    else:
                                        if not auto1act:
                                            clienteOPC.escribeTag('Canal.Automata1.Operacion.Origen.Balda', r[-4])
                                            if r[-2] == 'delante':
                                                clienteOPC.escribeTag('Canal.Automata1.Operacion.Origen.Delante', True)
                                            else:
                                                clienteOPC.escribeTag('Canal.Automata1.Operacion.Origen.Delante', False)
                                            clienteOPC.escribeTag('Canal.Automata1.Operacion.Origen.Estanteria', r[-5])
                                            clienteOPC.escribeTag('Canal.Automata1.Operacion.Origen.Posicion', r[-3])
                                            clienteOPC.escribeTag('Canal.Automata1.Operacion.Destino.Balda', balda)
                                            clienteOPC.escribeTag('Canal.Automata1.Operacion.Destino.Delante', delante)
                                            clienteOPC.escribeTag('Canal.Automata1.Operacion.Destino.Estanteria',
                                                                  estanteria)
                                            clienteOPC.escribeTag('Canal.Automata1.Operacion.Destino.Posicion',
                                                                  posicion)
                                            clienteOPC.escribeTag('Canal.Automata1.Operacion.Operacion', 3)
                                            clienteOPC.escribeTag('Canal.Automata1.Operacion.Marcha', True)
                                            op1 = 3
                                        elif not auto2act:
                                            clienteOPC.escribeTag('Canal.Automata2.Operacion.Origen.Balda', r[-4])
                                            if r[-2] == 'delante':
                                                clienteOPC.escribeTag('Canal.Automata2.Operacion.Origen.Delante', True)
                                            else:
                                                clienteOPC.escribeTag('Canal.Automata2.Operacion.Origen.Delante', False)
                                            clienteOPC.escribeTag('Canal.Automata2.Operacion.Origen.Estanteria', r[-5])
                                            clienteOPC.escribeTag('Canal.Automata2.Operacion.Origen.Posicion', r[-3])
                                            clienteOPC.escribeTag('Canal.Automata2.Operacion.Destino.Balda', balda)
                                            clienteOPC.escribeTag('Canal.Automata2.Operacion.Destino.Delante', delante)
                                            clienteOPC.escribeTag('Canal.Automata2.Operacion.Destino.Estanteria',
                                                                  estanteria)
                                            clienteOPC.escribeTag('Canal.Automata2.Operacion.Destino.Posicion',
                                                                  posicion)
                                            clienteOPC.escribeTag('Canal.Automata2.Operacion.Operacion', 3)
                                            clienteOPC.escribeTag('Canal.Automata2.Operacion.Marcha', True)
                                            op2 = 3
                                        else:
                                            QMessageBox.warning(ventana, "Error", "Todos los transelevadores ocupados")
                                        self.__puntos.append(
                                            [despldetras, altura, r[2], r[3], r[4], r[5], r[6], r[7],
                                             r[8], estanteria, balda, posicion, 'detrás', r[-1]])
                                        self.__puntos.remove(r)
                                despldelante += 15
                                despldetras += 15
                            altura -= 15
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
    figura.buclemultiple()

def selecciontipo(): #clase intermediaria al seleccionar un tipo de producto en el desplegable
    Figura.arranqueparpadeo(figura,tproducto.currentText())

def seleccionproducto(): #clase intermediaria al seleccionar un producto en el desplegable
    Figura.arranqueparpadeo(figura,producto.currentText())

def cancela(): #clase intermediaria al cancelar selección
    Figura.cancela(figura)

def buscar(): #clase intermediaria al buscar un número de palet
    try:
        Figura.buscar(figura,int(editorpalet.text()))
    except Exception as EX:
        resultado.setText('Debes meter un número')
def extraerpalet2():
  figura.extraerpalet()

lamparaEncendida=True
def funalarmaextraer():
    global lamparaEncendida,auto1act,auto2act,op1,op2
    lamparaEncendida = not lamparaEncendida
    if ((auto2act and op2==2) or (auto1act and op1==2)) and lamparaEncendida:
        alarmaextraer.setPixmap(QPixmap('LamparaRoja.png'))
    else:
        alarmaextraer.setPixmap(QPixmap('LamparaGris.png'))

def introduccion():
    global color
    if introducirproducto.currentText()=='Nada':
        resultado.setText('Introduzca nombre del producto')
    else:
        if introducirtproducto.currentText()=='Nada':
            for r in color:
                if r==introducirproducto.currentText():
                    figura.introduccion(color[r][1],introducirproducto.currentText(),
                                        fechas.date().toString('dd/MM/yyyy'),int(introducirbarrapalet.text()),
                                        int(introducirlitros.text()),int(introducirestanteria.currentText()),
                                        int(introducirbalda.currentText()),int(introducirposicion.currentText()),
                                        introducirdelante.isChecked(),color[r][0])
        else:
            act=True
            for r in color:
                if r==introducirproducto.currentText() and r[1]==introducirtproducto.currentText():
                    figura.introduccion(r[1], introducirproducto.currentText(),
                                        fechas.date().toString('dd/MM/yyyy'), int(introducirbarrapalet.text()),
                                        int(introducirlitros.text()), int(introducirestanteria.currentText()),
                                        int(introducirbalda.currentText()), int(introducirposicion.currentText()),
                                        introducirdelante.isChecked(), r[0])
                    act=False
            if act:
                resultado.setText('Producto no pertenece al tipo de producto indicado')

lamparaEncendida2=True
def funalarmaintroducir():
    global lamparaEncendida2,auto1act,auto2act,op1,op2
    lamparaEncendida2 = not lamparaEncendida2
    if ((auto2act and op2==1) or (auto1act and op1==1)) and lamparaEncendida2:
        alarmaintroducir.setPixmap(QPixmap('LamparaRoja.png'))
    else:
        alarmaintroducir.setPixmap(QPixmap('LamparaGris.png'))

def mover():
    figura.mover(int(editormoverpalet.text()),int(moverestanteria.currentText()),int(moverbalda.currentText()),
                 int(moverposicion.currentText()),moverdelante.isChecked())

lamparaEncendida3=True
def funalarmamover():
    global lamparaEncendida3,auto1act,auto2act,op1,op2
    lamparaEncendida3 = not lamparaEncendida3
    if ((auto2act and op2==3) or (auto1act and op1==3)) and lamparaEncendida3:
        alarmamover.setPixmap(QPixmap('LamparaRoja.png'))
    else:
        alarmamover.setPixmap(QPixmap('LamparaGris.png'))

def comprovacionautomata():
    global auto1act,auto2act
    if int(clienteOPC.leeTag('Canal.Automata2.Estado.Fase'))==0:
        auto2act=False
    else:
        auto2act=True
    if int(clienteOPC.leeTag('Canal.Automata1.Estado.Fase'))==0:
        auto1act = False
    else:
        auto1act = True

aplicacion = QApplication(sys.argv)
archivoUi = QFile("practica3.ui") # Crea un objeto para manejar el archivo interfaz.ui
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
editorextraer=ventana.findChild(QLineEdit,'editorextraer')
extraerpalet=ventana.findChild(QPushButton,'extraerpalet')
alarmaextraer=ventana.findChild(QLabel,'alarmaextraer')
introducirtproducto=ventana.findChild(QComboBox,'introducirtproducto')
introducirproducto=ventana.findChild(QComboBox,'introducirproducto')
fechas=ventana.findChild(QDateEdit,'fechas')
introducirbarrapalet=ventana.findChild(QLineEdit,'introducirbarrapalet')
introducirlitros=ventana.findChild(QLineEdit,'introducirlitros')
introducirestanteria=ventana.findChild(QComboBox,'introducirestanteria')
introducirbalda=ventana.findChild(QComboBox,'introducirbalda')
introducirposicion=ventana.findChild(QComboBox,'introducirposicion')
introducirpalet=ventana.findChild(QPushButton,'introducirpalet')
alarmaintroducir=ventana.findChild(QLabel,'alarmaintroducir')
introducirdelante=ventana.findChild(QCheckBox,'introducirdelante')
moverdelante=ventana.findChild(QCheckBox,'moverdelante')
editormoverpalet=ventana.findChild(QLineEdit,'editormoverpalet')
moverestanteria=ventana.findChild(QComboBox,'moverestanteria')
moverbalda=ventana.findChild(QComboBox,'moverbalda')
moverposicion=ventana.findChild(QComboBox,'moverposicion')
moverpalet=ventana.findChild(QPushButton,'moverpalet')
alarmamover=ventana.findChild(QLabel,'alarmamover')

try:
    clienteOPC = OPC_UA("opc.tcp://@localhost:49320")
except Exception as e:
    QMessageBox.warning(ventana, "Error", "Error en la conexión con el servidor OPC UA")
    sys.exit()
# Conexión al servidor OPC UA

for transelevador in range(2):  # Por cada transelevador ...

    dispositivo = "Canal.Automata" + str(transelevador + 1)
    # En el servidor OPC UA se configura un dispositivo por cada autómata

    clienteOPC.registraTag(dispositivo + ".Operacion.Operacion", OPC_UA.UINT16)
    clienteOPC.registraTag(dispositivo + ".Operacion.Marcha", OPC_UA.BOOL)
    clienteOPC.registraTag(dispositivo + ".Operacion.Destino.Delante", OPC_UA.BOOL)
    clienteOPC.registraTag(dispositivo + ".Operacion.Destino.Estanteria", OPC_UA.UINT16)
    clienteOPC.registraTag(dispositivo + ".Operacion.Destino.Balda", OPC_UA.UINT16)
    clienteOPC.registraTag(dispositivo + ".Operacion.Destino.Posicion", OPC_UA.UINT16)
    clienteOPC.registraTag(dispositivo + ".Operacion.Origen.Delante", OPC_UA.BOOL)
    clienteOPC.registraTag(dispositivo + ".Operacion.Origen.Estanteria", OPC_UA.UINT16)
    clienteOPC.registraTag(dispositivo + ".Operacion.Origen.Balda", OPC_UA.UINT16)
    clienteOPC.registraTag(dispositivo + ".Operacion.Origen.Posicion", OPC_UA.UINT16)
    clienteOPC.registraTag(dispositivo + ".Estado.Fase", OPC_UA.UINT16)
    clienteOPC.registraTag(dispositivo + ".Estado.ConPalet", OPC_UA.BOOL)
    clienteOPC.registraTag(dispositivo + ".Estado.X", OPC_UA.FLOAT)
    clienteOPC.registraTag(dispositivo + ".Estado.Y", OPC_UA.FLOAT)
    clienteOPC.registraTag(dispositivo + ".Estado.Z", OPC_UA.FLOAT)


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
    introducirtproducto.addItem(r)
for r in productos:
    producto.addItem(r)
    introducirproducto.addItem(r)

for r in list(range(1,5)):
    r=str(r)
    introducirestanteria.addItem(r)
    moverestanteria.addItem(r)
for r in list(range(1,9)):
    r=str(r)
    introducirbalda.addItem(r)
    moverbalda.addItem(r)
for r in list(range(1,25)):
    r = str(r)
    introducirposicion.addItem(r)
    moverposicion.addItem(r)

litros=0 #contador de litros totales
palets=1 #contador de palets totales
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
extraerpalet.clicked.connect(extraerpalet2)
introducirpalet.clicked.connect(introduccion)
moverpalet.clicked.connect(mover)

temporizador1 = QTimer()
temporizador1.timeout.connect(funalarmaextraer)
temporizador1.start(500)
temporizador2 = QTimer()
temporizador2.timeout.connect(funalarmaintroducir)
temporizador2.start(500)
temporizador3 = QTimer()
temporizador3.timeout.connect(funalarmamover)
temporizador3.start(500)
temporizadorauto = QTimer()
temporizadorauto.timeout.connect(comprovacionautomata)
temporizadorauto.start(1000)

fechas.setDate(datetime.now())
#fechas.setMinimumDateTime(datetime.today())

resultado.setText('Todos los productos Litros:{}  Palets usados:{}'.format(litros,palets))

ventana.show()
sys.exit(aplicacion.exec())

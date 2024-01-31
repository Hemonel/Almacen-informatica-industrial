
import sys
from OPCUA import OPC_UA
from PySide6.QtCore import QTimer, QFile
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QApplication, QMessageBox, QLabel, QPushButton
import math

aplicacion = QApplication(sys.argv)

archivoUi = QFile("simulador.ui")
archivoUi.open(QFile.ReadOnly)
cargador = QUiLoader()
ventana = cargador.load(archivoUi)
archivoUi.close()
# Lee el archivo que describe la interfaz Qt

etiquetaOperacion = [ventana.findChild(QLabel, "etiquetaOperacion1"), ventana.findChild(QLabel, "etiquetaOperacion2")]
etiquetaFase = [ventana.findChild(QLabel, "etiquetaFase1"), ventana.findChild(QLabel, "etiquetaFase2")]
etiquetaConPalet = [ventana.findChild(QLabel, "etiquetaConPalet1"), ventana.findChild(QLabel, "etiquetaConPalet2")]
etiquetaEstanteriaOrigen = [ventana.findChild(QLabel, "etiquetaEstanteriaOrigen1"), ventana.findChild(QLabel, "etiquetaEstanteriaOrigen2")]
etiquetaBaldaOrigen = [ventana.findChild(QLabel, "etiquetaBaldaOrigen1"), ventana.findChild(QLabel, "etiquetaBaldaOrigen2")]
etiquetaPosicionOrigen = [ventana.findChild(QLabel, "etiquetaPosicionOrigen1"), ventana.findChild(QLabel, "etiquetaPosicionOrigen2")]
etiquetaDelanteOrigen = [ventana.findChild(QLabel, "etiquetaDelanteOrigen1"), ventana.findChild(QLabel, "etiquetaDelanteOrigen2")]
etiquetaEstanteriaDestino = [ventana.findChild(QLabel, "etiquetaEstanteriaDestino1"), ventana.findChild(QLabel, "etiquetaEstanteriaDestino2")]
etiquetaBaldaDestino = [ventana.findChild(QLabel, "etiquetaBaldaDestino1"), ventana.findChild(QLabel, "etiquetaBaldaDestino2")]
etiquetaPosicionDestino = [ventana.findChild(QLabel, "etiquetaPosicionDestino1"), ventana.findChild(QLabel, "etiquetaPosicionDestino2")]
etiquetaDelanteDestino = [ventana.findChild(QLabel, "etiquetaDelanteDestino1"), ventana.findChild(QLabel, "etiquetaDelanteDestino2")]
etiquetaX = [ventana.findChild(QLabel, "etiquetaX1"), ventana.findChild(QLabel, "etiquetaX2")]
etiquetaY = [ventana.findChild(QLabel, "etiquetaY1"), ventana.findChild(QLabel, "etiquetaY2")]
etiquetaZ = [ventana.findChild(QLabel, "etiquetaZ1"), ventana.findChild(QLabel, "etiquetaZ2")]
botones = [ventana.findChild(QPushButton, "boton1"), ventana.findChild(QPushButton, "boton2")]
# Localiza todos los elementos de la interfaz y los guarda en listas. Cada lista tiene dos elementos iguales, cada
# uno para cada transelevador

botones[0].setVisible(False)
botones[1].setVisible(False)
# Inicialmente los botones no son visibles

try:
    clienteOPC = OPC_UA("opc.tcp://@localhost:49320")
except Exception as e:
    print(e)
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

#--------------------------------------------------------------------------------------------------
# Tipos de operaciones que ejecutan los transelevadores

OPERACION_NINGUNA = 0  # no está ejecutando ninguna operación de transporte de palets
OPERACION_INTRODUCIR = 1  # introducción de un nuevo palet en el almacén
OPERACION_EXTRAER = 2  # extracción de un palet del almacén
OPERACION_MOVER = 3  # movimiento de un palet existente en el almacén de una posición a otra posición

# Las operaciones ejecutadas por los transelevadores pasan por varias fases
FASE_REPOSO = 0  # el transelevador está en reposo en x=y=z=0
FASE_OPERARIO_CARGANDO_PALET = 1  # en x=y=z=0 y esperando a que el operario cargue un palet
FASE_OPERARIO_DESCARGANDO_PALET = 2  # en x=y=z=0 y esperando a que el operario descargue un palet del transelevador
FASE_YENDO_A_RECOGIDA = 3  # yendo al lugar de recogida de un palet en el almacén
FASE_EXTENDIENDO_EN_RECOGIDA = 4  # extendiendo palas para recoger un palet en el almacén
FASE_RETRAYENDO_EN_RECOGIDA = 5  # el palet se recogió en el almacén y retrayendo palas
FASE_YENDO_A_REPOSO = 6  # moviéndose hacia posición de reposo en x=y=z=0
FASE_YENDO_A_DESTINO = 7  # moviéndose hace lugar donde dejar un palet en el almacén
FASE_EXTENDIENDO_EN_DESTINO = 8  # extendiendo palas para dejar un palet en el almacén
FASE_RETRAYENDO_EN_DESTINO = 9 # retrayendo palas después de dejar un palet en el almacén

# ------------------------------------------------------------------------------------------------

class Transelevador:
    # Cada objeto de esta clase contiene los datos necesarios para manejar un transelevador

    def __init__(self):  # Constructor

        self.x = self.y = self.z = 0
        # Coordenadas donde se encuentra el transelevador en metros

        self.xObjetivo = self.yObjetivo = self.zObjetivo = 0
        # Coordenadas a dónde hay que llevar el transelevador

        self.operacion = OPERACION_NINGUNA
        # Operación en ejecución. Inicialmente no está ejecutando ninguna operación.

        self.fase = FASE_REPOSO
        # Fase en la que se encuentra la ejecución de la operación

        self.conPalet = False  # Indica si hay palet en el transelevador

        self.estanteriaDestino = 0
        self.baldaDestino = 0
        self.posicionDestino = 0
        self.delanteDestino = False
        # Indica a qué lugar del almacén hay que transportar un palet

        self.estanteriaOrigen = 0
        self.baldaOrigen = 0
        self.posicionOrigen = 0
        self.delanteOrigen = False
        # Indican dónde hay que recoger un palet en el almacén


transelevadores = [Transelevador(), Transelevador()]
# Lista con objetos para representar a los dos transelevadores

#-------------------------------------------------------------------------------------------

# Dimensiones en metros
anchoPalet = largoPalet = altoPalet = 1.2  # dimensiones de cada palet
margenPalets = 0.3  # separación entre palets
altoBalda = 0.3  # grosor de cada balda
separacionBaldas = 1.5  # separación entre baldas consecutivas
anchoPasillo = 2  # ancho de los pasillos por donde circulan los transelevadores
anchoBarraTranselevador = 0.5  # ancho de la barra vertical del transelevador
anchoPlataformaTranselevador = 1.2  # ancho de la plataforma donde se depositan palets en el transelevador

# Largo total de cada balda
largoBalda = anchoPalet * 24 + margenPalets * 25

# Incrementos de movimiento de los transelevadores a cada 500 ms. para simular el funcionamiento
# de los transelevadores
incrementoX = 0.4
incrementoY = 0.2
incrementoZ = 0.1


def coordenadasAlmacen(estanteria, balda, posicion, delante):
    # Devuelve las coordenadas x, y, z del transelevador para dejar o coger un palet donde
    # indican los parámetros:
    # estantería de 1 a 4
    # balda de 1 a 8
    # posicion de 1 a 24
    # delante es True o False

    x = anchoBarraTranselevador + largoPalet + (posicion - 1) * (largoPalet + margenPalets)
    y = (balda - 1) * (separacionBaldas + altoBalda)
    z = (anchoPasillo - anchoPlataformaTranselevador) / 2 + margenPalets + anchoPalet
    if not delante:
        z += margenPalets + anchoPalet
    if estanteria == 2 or estanteria == 4:
        z = -z
    return x, y, z  # devuelve las tres coordenadas en una tupla

# -------------------------------------------------------------------------
# Tratamiento de los botones de la interfaz

def atiendeBoton(nBoton):  # Atiende el botón 1 o 2 indicado por parámetro

    t = transelevadores[nBoton - 1]  # Objeto con los datos del transelevador

    dispositivo = "Canal.Automata" + str(nBoton)
    # dispositivo OPC UA que corresponde al autómata que maneja el transelevador

    if t.operacion == OPERACION_INTRODUCIR:
        # si se está introduciendo un nuevo palet en el almacén cuando el operario pulsa el botón,
        # es para que el operario confirme que ya ha cargado el palet en el transelevador

        t.conPalet = True  # al pulsar el botón, el operario confirma que ha cargado el palet en el transelevador
        etiquetaConPalet[nBoton-1].setText("Con palet")  # mensaje en pantalla confirmando que el transelevador tiene palet
        t.fase = FASE_YENDO_A_DESTINO  # hay que mover el palet a su posición destino en el almacén
        etiquetaFase[nBoton - 1].setText("Fase: a destino")  # indica en pantalla que va a moverse a la posición destino

    elif t.operacion == OPERACION_EXTRAER:
        # si se pulsa el botón durante una extracción de un palet del almacén es porque el operario
        # confirma que descargó el palet del transelevador

        t.conPalet = False  # indica que el transelevador ya no tiene palet

        etiquetaConPalet[nBoton-1].setText("Sin palet")  # muestra en pantalla que el transelevador no tiene palet

        t.operacion = OPERACION_NINGUNA  # finalizó la extracción del palet del almacén

        clienteOPC.escribeTag(dispositivo + ".Operacion.Operacion", OPERACION_NINGUNA)
        # indica en el servidor OPC UA que la extracción finalizó

        etiquetaOperacion[nBoton - 1].setText("Operación: ninguna")
        # muestra en pantalla que el transelevador no está ejecutando ninguna operación

        t.fase = FASE_REPOSO  # el transelevador está en reposo

        clienteOPC.escribeTag(dispositivo + ".Estado.Fase", FASE_REPOSO)
        # indica en el servidor OPC UA que el transelevador está en reposo

        etiquetaFase[nBoton - 1].setText("Fase: reposo")  # muestra en pantalla que está en reposo

    botones[nBoton - 1].setVisible(False)
    # hay que ocultar el botón cuando se pulsa


def boton1Click():  # función para atender al primer botón
    atiendeBoton(1)

def boton2Click():  # función para atender al segundo botón
    atiendeBoton(2)

botones[0].clicked.connect(boton1Click)
botones[1].clicked.connect(boton2Click)
# asocia los botones de la interfaz a las funciones

#-------------------------------------------------------------------------
# Código que se ejecuta en un temporizador

def temporizadorTick():  # Se ejecuta a cada 500 ms.

    for i in range(2):  # para cada transelevador

        dispositivo = "Canal.Automata" + str(i + 1)  # dispositovo OPC UA del autómata de cada transelevador
        t = transelevadores[i]  # objeto para manejo del transelevador

        if t.operacion == OPERACION_NINGUNA:
            # si el transelevador no está ejecutando ninguna operación ...

            marcha = clienteOPC.leeTag(dispositivo + ".Operacion.Marcha")
            if marcha:
                # si el cliente OPC UA indica a través del servidor que quiere comenzar la ejecución de una operación ...

                clienteOPC.escribeTag(dispositivo + ".Operacion.Marcha", False)
                # resetea la señal de marcha en el servidor

                t.operacion = clienteOPC.leeTag(dispositivo + ".Operacion.Operacion")
                # recoge el tipo de operación solicitada por el cliente

                if t.operacion == OPERACION_INTRODUCIR:
                    # si se solicita introducir un nuevo palet en el almacén ...

                    etiquetaOperacion[i].setText("Operación: introducir")
                    # muestra en pantalla la operación solicitada

                    t.fase = FASE_OPERARIO_CARGANDO_PALET
                    # inicialmente se espera a que el operario introduzca el palet en el transelevador

                    etiquetaFase[i].setText("Fase: cargando")
                    # indica en pantalla que se está esperando a la carga del palet en el transelevador

                    botones[i].setText("Cargado")
                    botones[i].setVisible(True)
                    # hace visible el botón que el operario tiene que pulsar cuando haya cargado el palet

                    t.estanteriaDestino = clienteOPC.leeTag(dispositivo + ".Operacion.Destino.Estanteria")
                    t.baldaDestino = clienteOPC.leeTag(dispositivo + ".Operacion.Destino.Balda")
                    t.posicionDestino = clienteOPC.leeTag(dispositivo + ".Operacion.Destino.Posicion")
                    t.delanteDestino = clienteOPC.leeTag(dispositivo + ".Operacion.Destino.Delante")
                    # recoge del servidor OPC UA los datos puestos por el cliente que indican dónde hay que
                    # depositar el palet en el almacén

                    t.xObjetivo, t.yObjetivo, t.zObjetivo = coordenadasAlmacen(t.estanteriaDestino, t.baldaDestino,
                        t.posicionDestino, t.delanteDestino)
                    # obtiene las coordenadas x,y,z en metros de la posición del almacén donde hay que
                    # depositar el palet

                elif t.operacion == OPERACION_EXTRAER:
                    # si el cliente solicita la extracción de un palet del almacén ...

                    etiquetaOperacion[i].setText("Operación: extraer")
                    # muestra en pantalla la operación solicitada

                    t.fase = FASE_YENDO_A_RECOGIDA
                    etiquetaFase[i].setText("Fase: a recogida")
                    # inicialmente el transelevador tiene que moverse a la posición donde está el palet

                    t.estanteriaOrigen = clienteOPC.leeTag(dispositivo + ".Operacion.Origen.Estanteria")
                    t.baldaOrigen = clienteOPC.leeTag(dispositivo + ".Operacion.Origen.Balda")
                    t.posicionOrigen = clienteOPC.leeTag(dispositivo + ".Operacion.Origen.Posicion")
                    t.delanteOrigen = clienteOPC.leeTag(dispositivo + ".Operacion.Origen.Delante")
                    # recoge del servidor OPC UA los datos puestos por el cliente que indican dónde hay
                    # que coger el palet en el almacén

                    t.xObjetivo, t.yObjetivo, t.zObjetivo = coordenadasAlmacen(t.estanteriaOrigen, t.baldaOrigen,
                        t.posicionOrigen, t.delanteOrigen)
                    # obtiene las coordenadas x,y,z en metros de la posición donde hay que recoger el palet

                elif t.operacion == OPERACION_MOVER:
                    # si el cliente solicita mover un palet en el almacén de una posición a otra posición ...

                    etiquetaOperacion[i].setText("Operación: mover")
                    t.fase = FASE_YENDO_A_RECOGIDA
                    etiquetaFase[i].setText("Fase: a recogida")
                    # indica que se está ejecutando esa operación y que el transelevador se está moviendo para
                    # recoger el palet

                    t.estanteriaOrigen = clienteOPC.leeTag(dispositivo + ".Operacion.Origen.Estanteria")
                    t.baldaOrigen = clienteOPC.leeTag(dispositivo + ".Operacion.Origen.Balda")
                    t.posicionOrigen = clienteOPC.leeTag(dispositivo + ".Operacion.Origen.Posicion")
                    t.delanteOrigen = clienteOPC.leeTag(dispositivo + ".Operacion.Origen.Delante")
                    # datos indicados por el cliente para señalar la posición donde hay que coger el palet

                    t.xObjetivo, t.yObjetivo, t.zObjetivo = coordenadasAlmacen(t.estanteriaOrigen, t.baldaOrigen,
                        t.posicionOrigen, t.delanteOrigen)
                    # posición x,y,z en metros donde hay que recoger el palet

                    t.estanteriaDestino = clienteOPC.leeTag(dispositivo + ".Operacion.Destino.Estanteria")
                    t.baldaDestino = clienteOPC.leeTag(dispositivo + ".Operacion.Destino.Balda")
                    t.posicionDestino = clienteOPC.leeTag(dispositivo + ".Operacion.Destino.Posicion")
                    t.delanteDestino = clienteOPC.leeTag(dispositivo + ".Operacion.Destino.Delante")
                    # datos indicados por el cliente para señalar la posición donde hay que dejar el palet

        if t.fase == FASE_YENDO_A_RECOGIDA:
            # si el transelevador se está moviendo a una posición donde va a recoger un palet ...

            if t.xObjetivo - t.x > incrementoX:
                t.x += incrementoX
            else:
                t.x = t.xObjetivo
            if t.yObjetivo - t.y > incrementoY:
                t.y += incrementoY
            else:
                t.y = t.yObjetivo
            # actualiza las coordenadas x e y aplicando un incremento a cada temporización para simular el movimiento

            if t.x == t.xObjetivo and t.y == t.yObjetivo:
                # si el transelevador llegó a la posición de recogida ...

                t.fase = FASE_EXTENDIENDO_EN_RECOGIDA
                etiquetaFase[i].setText("Fase: extendiendo")
                # el transelevador pasa a extender las palas para recoger el palet

        elif t.fase == FASE_EXTENDIENDO_EN_RECOGIDA:
            # si está extendiendo las palas para recoger un palet ...

            if math.fabs(t.z - t.zObjetivo) > incrementoZ:
                if t.zObjetivo > t.z:
                    t.z += incrementoZ
                else:
                    t.z -= incrementoZ
                # incrementa la coordenada z a cada temporización para simular el movimiento de las palas

            else:  # si extendió las palas ...

                t.z = t.zObjetivo  # las extendió completamente

                t.fase = FASE_RETRAYENDO_EN_RECOGIDA
                etiquetaFase[i].setText("Fase: retrayendo")
                # a continuación va a retraer las palas

                t.conPalet = True
                etiquetaConPalet[i].setText("Con palet")
                # indica que hay palet en el transelevador

        elif t.fase == FASE_RETRAYENDO_EN_RECOGIDA:
            # si está retrayendo las palas cuando está recogiendo un palet ...

            if math.fabs(t.z) > incrementoZ:
                if t.z > 0:
                    t.z -= incrementoZ
                else:
                    t.z += incrementoZ
                # incrementa la coordenada z a cada temporización para simular el movimiento de las palas

            else:  # si ya están retraídas ...

                t.z = 0  # palas retraídas

                if t.operacion == OPERACION_EXTRAER:
                    # si se está extrayendo un palet del almacén ...

                    t.fase = FASE_YENDO_A_REPOSO
                    etiquetaFase[i].setText("Fase: a reposo")
                    # el transelevador tiene que transportar el palet a x=y=z=0

                elif t.operacion == OPERACION_MOVER:
                    # si se está moviendo un palet de posición en el almacén ...

                    t.fase = FASE_YENDO_A_DESTINO
                    etiquetaFase[i].setText("Fase: a destino")
                    # a continuación hay que ir a la posición destino donde hay que dejar el palet

                    t.xObjetivo, t.yObjetivo, t.zObjetivo = coordenadasAlmacen(t.estanteriaDestino, t.baldaDestino,
                        t.posicionDestino, t.delanteDestino)
                    # coordenadas x,y,z en metros donde hay que dejar el palet

        elif t.fase == FASE_YENDO_A_REPOSO:
            # si el transelevador se está moviendo a la posición de reposo x=y=z=0 ...

            if t.x > incrementoX:
                t.x -= incrementoX
            else:
                t.x = 0
            if t.y > incrementoY:
                t.y -= incrementoY
            else:
                t.y = 0
            # simula el movimiento añadiendo incrementos a las coordenadas x e y a cada temporización

            if t.x == 0 and t.y == 0:  # si llegó a la posición de reposo ...

                if t.operacion == OPERACION_EXTRAER:
                    # si se está extrayendo un palet del almacén ...

                    t.fase = FASE_OPERARIO_DESCARGANDO_PALET
                    etiquetaFase[i].setText("Fase: descargando")
                    # hay que esperar a que el operario descargue el palet del transelevador

                    botones[i].setText("Descargado")
                    botones[i].setVisible(True)
                    # muestra el botón que tiene que el operario tiene que pulsar después de haber
                    # descargado el palet

                else:  # si no es una extracción de un palet del almacén ...

                    t.fase = FASE_REPOSO
                    etiquetaFase[i].setText("Fase: reposo")
                    t.operacion = OPERACION_NINGUNA
                    clienteOPC.escribeTag(dispositivo + ".Operacion.Operacion", OPERACION_NINGUNA)
                    etiquetaOperacion[i].setText("Operación: ninguna")
                    # el transelevador pasa a modo reposo

        elif t.fase == FASE_YENDO_A_DESTINO :
            # si el transelevador está moviéndose a una posición donde hay que dejar un palet ...

            if math.fabs(t.xObjetivo - t.x) > incrementoX:
                if t.xObjetivo > t.x:
                    t.x += incrementoX
                else:
                    t.x -= incrementoX
            else:
                t.x = t.xObjetivo
            if math.fabs(t.yObjetivo - t.y) > incrementoY:
                if t.yObjetivo > t.y:
                    t.y += incrementoY
                else:
                    t.y -= incrementoY
            else:
                t.y = t.yObjetivo
            # simula el movimiento del transelevador incrementando las posiciones x e y a cada temporización

            if t.x == t.xObjetivo and t.y == t.yObjetivo:
                # si llegó a la posición destino ...

                t.fase = FASE_EXTENDIENDO_EN_DESTINO
                etiquetaFase[i].setText("Fase: extendiendo")
                # pasa a una fase en la que extiende las palas

        elif t.fase == FASE_EXTENDIENDO_EN_DESTINO:
            # si está extendiendo las palas para dejar un palet ...

            if math.fabs(t.z - t.zObjetivo) > incrementoZ:
                if t.zObjetivo > t.z:
                    t.z += incrementoZ
                else:
                    t.z -= incrementoZ
            # simula el movimiento de las palas incrementando su posición a cada temporización

            else:  # si las palas están completamente extendidas ...

                t.z = t.zObjetivo
                t.fase = FASE_RETRAYENDO_EN_DESTINO
                etiquetaFase[i].setText("Fase: retrayendo")
                t.conPalet = False
                etiquetaConPalet[i].setText("Sin palet")
                # pasa a una fase de retracción de las palas sin palet

        elif t.fase == FASE_RETRAYENDO_EN_DESTINO:
            # si está retrayendo las palas después de dejar un palet ...

            if math.fabs(t.z) > incrementoZ:
                if t.z > 0:
                    t.z -= incrementoZ
                else:
                    t.z += incrementoZ
            # simula el movimiento de las palas aplicando un incremento

            else:  # si las palas están completamente retraídas ...

                t.z = 0
                t.fase = FASE_YENDO_A_REPOSO
                etiquetaFase[i].setText("Fase: a reposo")
                # pasa a una fase de movimiento del transelevador a su posición de reposo

        clienteOPC.escribeTag(dispositivo + ".Estado.Fase", t.fase)
        clienteOPC.escribeTag(dispositivo + ".Estado.ConPalet", t.conPalet)
        # guarda en el servidor OPC UA en qué fase está el transelevador y si tiene palet

        if t.operacion == OPERACION_NINGUNA:
            etiquetaEstanteriaOrigen[i].setText("Estantería")
            etiquetaBaldaOrigen[i].setText("Balda")
            etiquetaPosicionOrigen[i].setText("Posición")
            etiquetaDelanteOrigen[i].setText("Delante")
            etiquetaEstanteriaDestino[i].setText("Estantería")
            etiquetaBaldaDestino[i].setText("Balda")
            etiquetaPosicionDestino[i].setText("Posición")
            etiquetaDelanteDestino[i].setText("Delante")
            # textos a mostrar en etiquetas de la interfaz cuando el transelevador está en reposo

        elif t.operacion == OPERACION_INTRODUCIR:
            etiquetaEstanteriaOrigen[i].setText("Estantería")
            etiquetaBaldaOrigen[i].setText("Balda")
            etiquetaPosicionOrigen[i].setText("Posición")
            etiquetaDelanteOrigen[i].setText("Delante")
            etiquetaEstanteriaDestino[i].setText("Estantería = " + str(t.estanteriaDestino))
            etiquetaBaldaDestino[i].setText("Balda = " + str(t.baldaDestino))
            etiquetaPosicionDestino[i].setText("Posición = " + str(t.posicionDestino))
            etiquetaDelanteDestino[i].setText("Delante = " + str(t.delanteDestino))
            # textos en etiquetas cuando se está introduciendo un palet en el almacén

        elif t.operacion == OPERACION_EXTRAER:
            etiquetaEstanteriaOrigen[i].setText("Estantería = " + str(t.estanteriaOrigen))
            etiquetaBaldaOrigen[i].setText("Balda = " + str(t.baldaOrigen))
            etiquetaPosicionOrigen[i].setText("Posición = " + str(t.posicionOrigen))
            etiquetaDelanteOrigen[i].setText("Delante = " + str(t.delanteOrigen))
            etiquetaEstanteriaDestino[i].setText("Estantería")
            etiquetaBaldaDestino[i].setText("Balda")
            etiquetaPosicionDestino[i].setText("Posición")
            etiquetaDelanteDestino[i].setText("Delante")
            # textos en etiquetas cuando se está extrayendo un palet del almacén

        elif t.operacion == OPERACION_MOVER:
            etiquetaEstanteriaOrigen[i].setText("Estantería = " + str(t.estanteriaOrigen))
            etiquetaBaldaOrigen[i].setText("Balda = " + str(t.baldaOrigen))
            etiquetaPosicionOrigen[i].setText("Posición = " + str(t.posicionOrigen))
            etiquetaDelanteOrigen[i].setText("Delante = " + str(t.delanteOrigen))
            etiquetaEstanteriaDestino[i].setText("Estantería = " + str(t.estanteriaDestino))
            etiquetaBaldaDestino[i].setText("Balda = " + str(t.baldaDestino))
            etiquetaPosicionDestino[i].setText("Posición = " + str(t.posicionDestino))
            etiquetaDelanteDestino[i].setText("Delante = " + str(t.delanteDestino))
            # textos en etiquetas cuando se está moviendo un palet de posición en el almacén

        etiquetaX[i].setText('X = {0:.1f}'.format(t.x))
        etiquetaY[i].setText('Y = {0:.1f}'.format(t.y))
        etiquetaZ[i].setText('Z = {0:.1f}'.format(t.z))
        # muestra en etiquetas la posición x,y,z del transelevador en metros

        clienteOPC.escribeTag(dispositivo + ".Estado.X", t.x)
        clienteOPC.escribeTag(dispositivo + ".Estado.Y", t.y)
        clienteOPC.escribeTag(dispositivo + ".Estado.Z", t.z)
        # guarda en el servidor OPC UA la posición del transelevador


temporizador = QTimer()
temporizador.timeout.connect(temporizadorTick)
temporizador.start(100)
# crea un temporizador que provoca la ejecución de la función temporizadorTick() a cada
# décima de segundo

ventana.show()
sys.exit(aplicacion.exec())



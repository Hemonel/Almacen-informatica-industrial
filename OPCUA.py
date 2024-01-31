import opcua # Para la comunicación OPC UA
class OPC_UA:
 # Un objeto de esta clase facilita la conexión y comunicación con un servidor OPC UA
 BOOL = opcua.ua.VariantType.Boolean
 UINT8 = opcua.ua.VariantType.Byte
 INT8 = opcua.ua.VariantType.SByte
 UINT16 = opcua.ua.VariantType.UInt16
 INT16 = opcua.ua.VariantType.Int16
 UINT32 = opcua.ua.VariantType.UInt32
 INT32 = opcua.ua.VariantType.Int32
 UINT64 = opcua.ua.VariantType.UInt64
 INT64 = opcua.ua.VariantType.UInt64
 FLOAT = opcua.ua.VariantType.Float
 DOUBLE = opcua.ua.VariantType.Double
 STRING = opcua.ua.VariantType.String
 DATETIME = opcua.ua.VariantType.DateTime
 # Referencias estáticas para indicar un tipo de dato para cada tag
 def __init__(self, URLServidor):
  # Constructor. Inicia la conexión con el servidor OPC UA cuya URL se pasa por
  # parámetro.
  self.tags = {} # Crea el diccionario de tags, inicialmente vacío
  self.cliente = opcua.Client(URLServidor)
  self.cliente.connect() # Se conecta al servidor


 def registraTag(self, nombre, tipo):
   # Registra en el diccionario de tags un nuevo tag del servidor. En 'nombre' se
   # indica el nombre completo en una cadena (en Kepware Kepserver con el canal,
   # dispositivo, grupos y tag). En 'tipo' se indica tipo de dato: BOOL, UINT8, etc
   self.tags[nombre] = {
    "tag": self.cliente.get_node("ns=2;s=" + nombre),
    "tipo": tipo}
   # Crea una nueva entrada en el diccionario de tags, de forma que a partir del nombre
   # completo del tag del servidor, se obtiene a su vez otro diccionario con:
   # "tag": el objeto de la clase opcua.ua.Node correspondiente
   # "tipo": el tipo opcua.ua.VariantType correspondiente
 def leeTag(self, nombre):
   # Devuelve el resultado de leer el valor actual del tag del servidor que
   # corresponde al nombre indicado por parámetro
   tag = self.tags[nombre]["tag"]  # Obtiene el objeto de la clase Node
   resultado = tag.get_value()  # Realiza la lectura del valor
   return resultado  # devuelve el valor

 def escribeTag(self, nombre, valor):

   # Realiza la escritura de 'valor' en el tag identificado por 'nombre'
   dato = opcua.ua.DataValue(opcua.ua.Variant(valor, self.tags[nombre]["tipo"]))
   # Expresa el valor en un objeto de la clase opcua.ua.DataValue
   self.tags[nombre]["tag"].set_value(dato)

   # Realiza la escritura del valor en el servidor utilizando el objeto de la clase
   # Node disponible en el diccionario de tags
 def desconecta(self):  # Para que el cliente cierre la conexión con el servidor
   self.cliente.disconnect()
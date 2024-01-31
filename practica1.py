import xml.etree.ElementTree as ET
arbolXML = ET.parse('almacen1.xml') #carga el archivo almacen
raiz = arbolXML.getroot()

dic={} #productos y características
cant={} #cantidad de cada tipo de producto
for estanteria in raiz[2]: #crea un diccionario con cada producto y su cantidad
    for balda in estanteria:
        for palet in balda:
            if palet.attrib['idProducto'] in dic:
                dic[palet.attrib['idProducto']][0]+=int(palet.attrib['litros'])
                dic[palet.attrib['idProducto']][1] +=1
            if not palet.attrib['idProducto'] in dic:
                dic[palet.attrib['idProducto']]=[int(palet.attrib['litros']),1]
for p in raiz[1]: #añade a cada producto su tipo de producto
    for i in dic:
        if p.attrib['id'] == i:
            dic[i].append(p.attrib['idTipoProducto'])

litros=0
palets=0
for p in dic: #cálculo litros y palets totales y creo un diccionario con cada tipo de producto y sus características
    litros+=dic[p][0]
    palets+=dic[p][1]
    if dic[p][2] in cant:
        cant[dic[p][2]][0]+=dic[p][0]
        cant[dic[p][2]][1]+=dic[p][1]
    if not dic[p][2] in cant:
        cant[dic[p][2]]=[dic[p][0],dic[p][1]]


inventario = ET.Element('inventario') #crea la etiqueta principal
inventario.attrib['litros'] = str(litros) #añade como atributo los litros totales
inventario.attrib['numPalets'] = str(palets) #añade como atributo el número de palets totales

for i in cant: # crea cada etiqueta de tipo de producto y sus cantidades
    etiqueta = ET.SubElement(inventario,'tipoProducto')
    etiqueta.attrib['id'] = i
    etiqueta.attrib['litros'] = str(cant[i][0])
    etiqueta.attrib['numPalets'] = str(cant[i][1])
    for p in dic: #crea cada etiqueta por producto y sus cantidades
        if i==dic[p][2]:
            producto=ET.SubElement(etiqueta,'producto')
            producto.attrib['id'] = p
            producto.attrib['litros'] = str(dic[p][0])
            producto.attrib['numPalets'] = str(dic[p][1])

ET.ElementTree(inventario).write('inventario.xml', encoding='utf-8', method='xml') #guarda en el inventario.xml
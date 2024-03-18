# GESTIÓN DE ALMACEN ROBOTIZADO
Estás son las 3 prácticas realizadas para la asignatura de Informática Industrial de 3º de Ingeniería en Electrónica Industrial y Automática.

## Software
PyCharm Community Edition

## 1ª Práctica
Lectura de los datos de almacen1.xml, un archivo donde se indican las categorías de productos, los productos que puede haber en el almacen y los productos que hay en cada posición de la estantería.

El programa lee el amacen entero y suma las cantidades de cada producto.

Finalmente crea inventario.xml donde guarda las cantidades de cada producto.

## 2ª Práctica
En la segunda lee el archivo almacen1.xml, y crea una intefaz gráfica de QT desde la que se puede visualizar todo el inventario, buscar un producto o productos concretos mediante su ID, tipo de producto o nombre de producto.

## 3ª Práctica
En la tercera lee el archivo almacen1.xml y crea una intefaz similar a la anterior, pero esta vez puede solicitar que se metan, saquen o muevan productos.

Para simular estos procesos existe el programa simulador.py que emula los movimientos del robot de almacenaje.

Requiere de un servidor OPC UA, que es donde se cargan los datos del almacen.

#
#
#                   ------------------------------------------------------------------------------------
#                               PLANTILLA PARA ADAPTAR EL CONTROL A NUEVAS INTERFACES DE ENTRADA:
#                   ------------------------------------------------------------------------------------
#                   1. Importar la libreria que se comunica con el otro subsistema mediante sockets
#                   
##                   #   import Sockets_input as sk                 # ___librería para el envío
#
#                   2.1. Recibir las entradas dentro de un bucle infinito (While True:)
#
#                   2.2. Realizar la conversion de las entradas del sensor o dispositivo elegido a las 
#                   conocidas por control (definidas mas abajo en "ENVIOS PERMITIDOS POR CONTROL")
#
#
#                   2.3. Enviar los datos a traves de la funcion envio_data definida en la libreria
#                    Sockets_input de la siguiente manera:
#
#                   #   sk.envio_data(modo, direccion, velocidad)  # ___Para el envío constante dentro del bucle
#
#                   3. En la libreria Sockets_input, se puede modificar la linea time.sleep() de acuerdo a la          
#                   frecuencia de envío que se desee.
#
#                   ------------------------------------------------------------------------------------
#                               ENVIOS PERMITIDOS POR CONTROL:
#                   ------------------------------------------------------------------------------------
#                   Siendo v = velocidad valor comprendido entre -100.0 y 100.0
#                   d = direccion valores permitidos {1, 0, -1}
#                   modo {0, 1, 2, 3, 4, 5, 999}
#
#                   (0, d, v)               ____________________movimientos básicos (front, back, left, right)
#                   (1, -1, 0)  (1, 1, 0)   ____________________modo 1 giro 180 grados a ambos lados (-1 left, +1 right)   
#                   (2, 0, 0)               ____________________modo 2 realizar movimiento pregrabado
#                   (3, 0, 0)               ____________________modo 3 grabar movimiento
#                   (4, 0, 0)               ____________________modo 4 PARADA de emergencia   
#                   (5, 0, 0)               ____________________modo 5 finalizar grabación, reiniciar movimiento tras modo 4    
#                   (999, 0, 0)             ____________________modo 999 error en la entrada
#
#                   El modo 999 se usara para controlar entradas erroneas: mantiene el robot quieto

#                   
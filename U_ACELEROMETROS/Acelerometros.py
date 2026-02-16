# Violeta Toribio Rivera

# Codigo Movimientos básicos + modos especiales Acelerómetros 

# --------------------------------------------------------------------------------------------------------------------------------------------------- #
#   MODOS ESPECIALES
# --------------------------------------------------------------------------------------------------------------------------------------------------- #
#   MODOS:  MANOS:      
#   MODO 0: Manos ejecutan movimientos básicos: mano izquierda controla velocidad (up|down), mano derecha controla giro (L|R)
#   MODO 1: (L|R, up)       Giro 180 grados, posicion de las manos: izquierda gira, derecha arriba
#   MODO 2: (down, up)      EJECUTAR recorrido pregrabado, posicion de las manos: mano izquierda abajo, mano derecha arriba
#   MODO 3: (up, down)      INICIAR grabacion de movimiento, posicion de las manos: mano izquierda arriba, mano derecha abajo
#   MODO 4: (up, up)        Cancelar movimiento, posicion de las manos: ambas manos hacia arriba
#   MODO 5: (down, down)    TERMINAR la grabacion | volver al modo0 tras una cancelacion de movimiento (modo 4). Ambas manos hacia abajo
# ---------------------------------------------------------------------------------------------------------------------------------------------------- #


#Importación librerías

import RPi.GPIO as GPIO
from mpu6050 import mpu6050
import math
import time
import sys
#Importación fichero comunicación por sockets
import Sockets_input as sk

try:
    mpu = mpu6050(0x68)
    mpu2 = mpu6050(0x69)
except OSError:
    print("Error iniciacion mpu6050")
    sys.exit(1)
    
GPIO.setmode(GPIO.BOARD)
GPIO.setup(11, GPIO.IN)

#Función que devuelve los valores de las aceleraciones en los tres ejes
def leer_datos(accel_data):
    x = accel_data['x']
    y = accel_data['y']
    z = accel_data['z']
    return x, y, z

# Función que inicializa los movimientos máximos y mínimos del giro de muñecas de ambas manos

def leer_fichero():
    with open('setup_file.txt','r') as f:
        derecha_mdcha = float(f.readline())
        derecha_mizq = float(f.readline())
        izquierda_mdcha = float(f.readline())
        izquierda_mizq = float(f.readline())
        arriba_mdcha = float(f.readline())
        arriba_mizq = float(f.readline())
        cero_max_mdcha = float(f.readline())
        cero_min_mdcha = float(f.readline())
        cero_max_mizq = float(f.readline())
        cero_min_mizq = float(f.readline())
        abajo_mdcha = float(f.readline())
        abajo_mizq = float(f.readline())
        return derecha_mdcha, derecha_mizq, izquierda_mdcha, izquierda_mizq, arriba_mdcha, arriba_mizq, cero_max_mdcha, cero_min_mdcha, cero_max_mizq, cero_min_mizq,abajo_mdcha, abajo_mizq

# ------------------------------------------------------------------------------------------------------------------------------- #


derecha_mdcha, derecha_mizq, izquierda_mdcha, izquierda_mizq, arriba_mdcha, arriba_mizq, cero_max_mdcha, cero_min_mdcha, cero_max_mizq, cero_min_mizq,  abajo_mdcha, abajo_mizq = leer_fichero()
i=0
direccion = 0
velocidad = 0
modo = 0

error = False

    
while True:
    try:
#Leemos los datos de los acelerómetros
        x, y, z = leer_datos(mpu.get_accel_data())
        x2, y2, z2 = leer_datos(mpu2.get_accel_data())
        
#    #Control de errores de división por cero, si llega una entrada mal leida, llega en formato (x = 0.0, y = 0.0, z = 0.0)
        if (x == z and y == z) or (x2 == z2 and y2 == z2): error = True
    #Calculamos ángulos de rotación si no se ha leído mal la entrada
        
        if not error:
            x_rotation = math.degrees(math.atan(x/math.sqrt((y*y)+(z*z))))
            x_rotation_2 = math.degrees(math.atan(x2/math.sqrt((y2*y2)+(z2*z2))))
            y_rotation = math.degrees(math.atan(y/math.sqrt((x*x)+(z*z))))
            y_rotation_2 = math.degrees(math.atan(y2/math.sqrt((x2*x2)+(z2*z2))))
        #Analizamos los ángulos y calculamos direccion, velocidad y modo
         
         # SI LA MANO DERECHA ESTA ARRIBAS O ABAJO INDICA MODO ESPECIAL, SI NO, CONTROL NORMAL
            if y_rotation > cero_max_mdcha or y_rotation < cero_min_mdcha:

                if y_rotation > cero_max_mdcha:
                    if y_rotation_2 > cero_max_mizq:  #MODO 4 PARADA 
                        direccion = 0
                        velocidad = 0
                        modo = 4
                        ##print("L arriba, R arriba")
                    elif y_rotation_2 < cero_min_mizq:  #MODO 2 Movimiento pregrabado 
                        direccion = 0
                        velocidad = 0
                        modo = 2
                        ##print("L abajo, R arriba")
                    elif x_rotation_2 < derecha_mizq:#MODO 1 giro 180 a la derecha
                        direccion = 1
                        velocidad = 0
                        modo = 1
                        ##print("L dcha, R arriba")
                    elif x_rotation_2 > izquierda_mizq:#MODO 1 giro 180 a la izquierda
                        direccion = -1
                        velocidad = 0
                        modo = 1
                        ##print("L izq, R arriba")
                    else:#ERROR
                        direccion = 0
                        velocidad = 0
                        modo = 999
                else:
                    if y_rotation_2 > cero_max_mizq:  #MODO 3 INICIAR GRABACIÓN
                        direccion = 0
                        velocidad = 0
                        modo = 3
                        ##print("L arriba, R abajo")
                    elif y_rotation_2 < cero_min_mizq:  #MODO 5 PARAR GRABACION, REINICIAR MODO 0 DESPUES DE MODO4 PARADA
                        direccion = 0
                        velocidad = 0
                        modo = 5
                        ##print("L abajo, R abajo")
                    else:#ERROR
                        direccion = 0
                        velocidad = 0
                        modo = 999
            else:
                modo = 0                                            #MODO0 - Movimientos básicos
                if y_rotation_2 < cero_min_mizq:
                    ##print("L abajo")
                    rango = abajo_mizq - cero_min_mizq              # Movimiento hacia atrás
                    valor = y_rotation_2 - cero_min_mizq
                    velocidad = -valor / rango * 100
                    if(velocidad < -100):
                        velocidad = -100 
                elif y_rotation_2 > cero_max_mizq:
                    ##print("L arriba")
                    rango = abs(arriba_mizq) - cero_max_mizq        # Movimiento hacia delante
                    valor = y_rotation_2 - cero_max_mizq
                    velocidad = valor / rango * 100
                    if(velocidad > 100):
                        velocidad = 100 
                     
                else:
                    velocidad = 0
                
                if x_rotation < derecha_mdcha:
                    direccion = 1
                    ##print("R derecha")
                elif x_rotation > izquierda_mdcha:
                    direccion = -1
                    ##print("R izquierda")
                else: direccion = 0

        else: #Hay error (se ha leído mal la entrada)
            modo = 999
            velocidad = 0
            direccion = 0
            error = False
        sk.envio_data(modo, direccion, velocidad)
    #Si salta error en la mpu6050, se captura para finalizar la ejecución del código y que queden quietos los motores
    except Exception:
         print("Error entrada")
         sk.envio_data(0,0,0)

         #sys.exit(1)
# Enviamos resultado al fichero de comuniación por sockets


#                   ------------------------------------------------------------------------------------
#                               ENVIOS PERMITIDOS POR CONTROL:
#                   ------------------------------------------------------------------------------------
#                   Siendo v = velocidad valor comprendido entre -100.0 y 100.0
#                   d = direccion valores permitidos {1, 0, -1}
#                   modo {0, 1, 2, 3, 4, 5, 999}
#
#                   (0, d, v)               ____________________movimientos básicos
#                   (1, -1, 0)  (1, 1, 0)   ____________________modo 1 giro 180 grados a ambos lados    
#                   (2, 0, 0)               ____________________modo 2 realizar movimiento pregrabado
#                   (3, d, v)   (5, 0, 0)   ____________________modo 3 grabar movimiento, finalizar grabación
#                   (4, 0, 0)               ____________________modo 4 PARADA de emergencia   
#                   (999, 0, 0)             ____________________modo 999 error en la entrada
#
#                   Dependencias:       
#
#                   #   import Sockets_input as sk                  ___librería para el envío
#                   #   sk.envio_data(modo, direccion, velocidad)   ___Para el envío constante dentro del bucle
#



#Importamos librerías
import time
import math
from mpu6050 import mpu6050

mpu=mpu6050(0x68)
mpu2=mpu6050(0x69)

#Inicializamos las variables
x_setup_derecha=[]
x2_setup_derecha=[]
x_setup_izquierda=[]
x2_setup_izquierda=[]
y_setup_cero=[]
y2_setup_cero=[]
y_setup_porcentaje_alante=[]
y2_setup_porcentaje_alante=[]
y_setup_porcentaje_detras=[]
y2_setup_porcentaje_detras=[]

desviacion_x = 15
desviacion_y = 40

#Función que devuelve los valores de las aceleraciones en los tres ejes
def leer_datos(accel_data):
    x=accel_data['x']
    y=accel_data['y']
    z=accel_data['z']
    return x,y,z


#Función que guarda los datos en el fichero de inicialización
def guardar_datos(x_derecha, x2_derecha,x_izquierda,x2_izquierda,y_delante,y2_delante,y_cero_max,y_cero_min,y2_cero_max,y2_cero_min,y_detras,y2_detras):
    with open('setup_file.txt','w') as f:
        f.write(str(x_derecha))
        f.write('\n')
        f.write(str(x2_derecha))
        f.write('\n')
        f.write(str(x_izquierda))
        f.write('\n')
        f.write(str(x2_izquierda))
        f.write('\n')
        f.write(str(y_delante))
        f.write('\n')
        f.write(str(y2_delante))
        f.write('\n')
        f.write(str(y_cero_max))
        f.write('\n')
        f.write(str(y_cero_min))
        f.write('\n')
        f.write(str(y2_cero_max))
        f.write('\n')
        f.write(str(y2_cero_min))
        f.write('\n')
        f.write(str(y_detras))
        f.write('\n')
        f.write(str(y2_detras))
        

#Función que inicializa la variable derecha haciendo que la persona mantenga la posición 6 segundos
def setup_derecha():
    for i in range(6):
        time.sleep(1)
        x,y,z=leer_datos(mpu.get_accel_data())
        x2,y2,z2=leer_datos(mpu2.get_accel_data())
        x_rotation=math.degrees(math.atan(x/math.sqrt((y*y)+(z*z))))
        x2_rotation=math.degrees(math.atan(x2/math.sqrt((y2*y2)+(z2*z2))))
        
        x_setup_derecha.append(x_rotation)
        x2_setup_derecha.append(x2_rotation)
        print(i)
    x_derecha=x_setup_derecha[0]
    x2_derecha=x2_setup_derecha[0]
    for i in range(6):
        if(x_setup_derecha[i]>x_derecha):
            x_derecha=x_setup_derecha[i]
        if(x2_setup_derecha[i]>x2_derecha):
            x2_derecha=x2_setup_derecha[i]
    x_derecha=x_derecha+desviacion_x
    x2_derecha=x2_derecha+desviacion_x
    return x_derecha, x2_derecha


#Función que inicializa la variable izquierda haciendo que la persona mantenga la posición 6 segundos
def setup_izquierda():
    for i in range(6):
        time.sleep(1)
        x,y,z=leer_datos(mpu.get_accel_data())
        x2,y2,z2=leer_datos(mpu2.get_accel_data())
        x_rotation=math.degrees(math.atan(x/math.sqrt((y*y)+(z*z))))
        x2_rotation=math.degrees(math.atan(x2/math.sqrt((y2*y2)+(z2*z2))))
        
        x_setup_izquierda.append(x_rotation)
        x2_setup_izquierda.append(x2_rotation)
        print(i)
        
    x_izquierda=x_setup_izquierda[0]
    x2_izquierda=x2_setup_izquierda[0]
    for i in range(6):
        if(x_setup_izquierda[i]<x_izquierda):
            x_izquierda=x_setup_izquierda[i]
        if(x2_setup_izquierda[i]<x2_izquierda):
            x2_izquierda=x2_setup_izquierda[i]
    
    x_izquierda=x_izquierda-desviacion_x
    x2_izquierda=x2_izquierda-desviacion_x
    return x_izquierda, x2_izquierda


#Función que inicializa las variables cero_max cero_min haciendo que la persona mantenga la posición 6 segundos
def setup_cero():
    for i in range(6):
        time.sleep(1)
        x,y,z=leer_datos(mpu.get_accel_data())
        x2,y2,z2=leer_datos(mpu2.get_accel_data())
        y_rotation=math.degrees(math.atan(y/math.sqrt((x*x)+(z*z))))
        y2_rotation=math.degrees(math.atan(y2/math.sqrt((x2*x2)+(z2*z2))))
        y_setup_cero.append(y_rotation)
        y2_setup_cero.append(y2_rotation)
        print(i)
    y_cero_max=y_setup_cero[0]
    y2_cero_max=y2_setup_cero[0]
    y_cero_min=y_setup_cero[0]
    y2_cero_min=y2_setup_cero[0]
    for i in range(6):
        if(y_setup_cero[i]>y_cero_max):
            y_cero_max=y_setup_cero[i]
        if(y_setup_cero[i]<y_cero_min):
            y_cero_min=y_setup_cero[i]
        if(y2_setup_cero[i]>y2_cero_max):
            y2_cero_max=y2_setup_cero[i]
        if(y2_setup_cero[i]<y2_cero_min):
            y2_cero_min=y2_setup_cero[i]
            
    y_cero_max=y_cero_max+desviacion_y
    y2_cero_max=y2_cero_max+desviacion_y
    y_cero_min=y_cero_min-desviacion_y
    y2_cero_min=y2_cero_min-desviacion_y
    
    return y_cero_max,y_cero_min, y2_cero_max, y2_cero_min

    
#Función que inicializa la variable delante haciendo que la persona mantenga la posición 6 segundos
def setup_delante():
    for i in range(6):
        time.sleep(1)
        x,y,z=leer_datos(mpu.get_accel_data())
        x2,y2,z2=leer_datos(mpu2.get_accel_data())
        y_rotation=math.degrees(math.atan(y/math.sqrt((x*x)+(z*z))))
        y2_rotation=math.degrees(math.atan(y2/math.sqrt((x2*x2)+(z2*z2))))
        y_setup_porcentaje_alante.append(y_rotation)
        y2_setup_porcentaje_alante.append(y2_rotation)
        print(i)
        
    y_delante=y_setup_porcentaje_alante[0]
    y2_delante=y2_setup_porcentaje_alante[0]  
    for i in range(6):
        if(y_setup_porcentaje_alante[i]<y_delante):
            y_delante=y_setup_porcentaje_alante[i]
        if(y2_setup_porcentaje_alante[i]<y2_delante):
            y2_delante=y2_setup_porcentaje_alante[i]
    return y_delante, y2_delante
    
#Función que inicializa la detrás derecha haciendo que la persona mantenga la posición 6 segundos
def setup_detras():
    for i in range(6):
        time.sleep(1)
        x,y,z=leer_datos(mpu.get_accel_data())
        x2,y2,z2=leer_datos(mpu2.get_accel_data())
        y_rotation=math.degrees(math.atan(y/math.sqrt((x*x)+(z*z))))
        y2_rotation=math.degrees(math.atan(y2/math.sqrt((x2*x2)+(z2*z2))))
        y_setup_porcentaje_detras.append(y_rotation)
        y2_setup_porcentaje_detras.append(y2_rotation)
        print(i)
        
    y_detras=y_setup_porcentaje_detras[0]
    y2_detras=y2_setup_porcentaje_detras[0]
    for i in range(6):
        if(y_setup_porcentaje_detras[i]>y_detras):
            y_detras=y_setup_porcentaje_detras[i]
        if(y2_setup_porcentaje_detras[i]>y2_detras):
            y2_detras=y2_setup_porcentaje_detras[i]
    return y_detras, y2_detras

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

print("Por favor realice los movimientos que se le indiquen: ")
time.sleep(4)

# ------------------------------------------------------------------------------------------------------------------------------- #
print("Gira ambas muñecas hacia la derecha.")
time.sleep(2)
x_derecha_mdcha, x_derecha_mizq = setup_derecha()
time.sleep(3)
print("Movimiento registrado.")
# ------------------------------------------------------------------------------------------------------------------------------- #

# ------------------------------------------------------------------------------------------------------------------------------- #
print("Gira ambas muñecas hacia la izquierda.")
time.sleep(2)
x_izquierda_mdcha, x_izquierda_mizq = setup_izquierda()
time.sleep(3)
print("Movimiento registrado.")
# ------------------------------------------------------------------------------------------------------------------------------- #

# ------------------------------------------------------------------------------------------------------------------------------- #
print("Mantén ambas manos en posición neutral (Palmas paralelas al suelo)")
time.sleep(2)
y_cero_max_mdcha, y_cero_min_mdcha, y_cero_max_mizq, y_cero_min_mizq = setup_cero()
time.sleep(3)
print("Movimiento registrado.")

# ------------------------------------------------------------------------------------------------------------------------------- #

# ------------------------------------------------------------------------------------------------------------------------------- #
print("Gira las muñecas hacia arriba (Dedos inclinados hacia arriba)")
time.sleep(2)
y_delante_mdcha, y_delante_mizq = setup_delante()
time.sleep(3)
print("Movimiento registrado.")
# ------------------------------------------------------------------------------------------------------------------------------- #

# ------------------------------------------------------------------------------------------------------------------------------- #
print("Gira las muñecas hacia abajo (Dedos inclinados hacia abajo)")
time.sleep(2)
y_detras_mdcha, y_detras_mizq = setup_detras()
time.sleep(3)
print("Movimiento registrado.")
# ------------------------------------------------------------------------------------------------------------------------------- #

# ------------------------------------------------------------------------------------------------------------------------------- #
print("La inicialización se ha realizado correctamente")
guardar_datos(x_derecha_mdcha, x_derecha_mizq, x_izquierda_mdcha, x_izquierda_mizq, y_delante_mdcha, y_delante_mizq, y_cero_max_mdcha, y_cero_min_mdcha, y_cero_max_mizq, y_cero_min_mizq, y_detras_mdcha, y_detras_mizq)


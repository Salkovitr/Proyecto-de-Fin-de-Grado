
#*****************************************************************************************************************************************************
# Violeta Toribio Rivera
# Codigo Control ordenes robot
#*****************************************************************************************************************************************************
#                                                       Importación librerías
#*****************************************************************************************************************************************************
import Automata as au
import comunicacionGPIO as m
import time
#*****************************************************************************************************************************************************
#                                                   Inicialización variables
#*****************************************************************************************************************************************************

f_movimientos = 'Movimientos_Pregrabados.txt'
pautas = {'direccion':'','velocidad':'','modo':''}
ordenes = 0
fin_modo = True
direccion_giro = 0
i = 0    


a = au.Automata()                   # se inicia el automata de estados factibles

#*****************************************************************************************************************************************************
#                                                  Funcion que llama Sockets_Output en caso de desconexion
#*****************************************************************************************************************************************************

def stop():
    print("PARADA por desconexion")
    m.mandar_robot(0, 0)
    
#*****************************************************************************************************************************************************
#                                                   TRATAMIENTO DE FICHERO MOVIMIENTOS
#*****************************************************************************************************************************************************

def init_ordenes():
    global ordenes
    with open( f_movimientos, 'r') as f:
        lineas = f.readlines()
    ordenes = len(lineas)

def init_fichero():
    with open(f_movimientos, 'w') as f:
        pass
    init_ordenes()
     
def escribir_orden(direccion, velocidad):
    global ordenes
    with open(f_movimientos, 'a') as f:
        linea = f'{direccion},{velocidad}\n'
        f.write(linea) 
    ordenes += 1

def leer_orden():
    with open(f_movimientos, 'r') as f:
        f.seek(0)
        for _ in range(i):                              # descarta lineas
            f.readline()
                
        linea = f.readline()
                        
    direccion, velocidad = linea.strip().split(',')              # Dividir la línea por la coma para separar los números
    return float(direccion), float(velocidad)
  


init_fichero()                          

#*****************************************************************************************************************************************************
#                                                   TRATAMIENTO DE ESTADOS Y TRANSICIONES
#*****************************************************************************************************************************************************

def control(pautas):
    
    direccion = pautas['direccion']
    velocidad = pautas['velocidad']
    modo = pautas['modo']
  
    e_ant = a.obtener_estado()
    if modo == 999:                                                 # se trata como una entrada (0,0,0)
        modo = 0
    
    if (e_ant == 1 or e_ant == 2) and fin_modo:                     # Tratamiento de transiciones, llamada a automata
        existe_t, realiza_t = a.transitar('FIN')
    else: existe_t, realiza_t = a.transitar(int(modo))
    
    e_act = a.obtener_estado()
    
    if not existe_t:
        envio_data(e_act, direccion, velocidad)
    
    elif realiza_t:
        gestion_transiciones(e_act, e_ant, direccion)
    
    else: envio_data(0, 0, 0)                                       # Si exite transicion el usuario trata de hacer un cambio. Robot quieto.

        
        
def gestion_transiciones(e_act, e_ant, direccion):
    global direccion_giro                                   # Guarda dirección del giro del modo 1
    global i

    if e_act == 1:                                          # Si transita al estado 1 hay que guardar la dir de giro 
        direccion_giro = direccion   
        i = 0
    elif e_act == 2:
        init_ordenes()
        i = 0
    elif e_act == 3:                                        # Si transita al estado 3 hay que asegurar que el fichero quede vacío
        init_fichero()
    elif e_act == 4 and e_ant == 3:                         # Si transita al 4 estando en 1 o 2 reestablece i
        init_fichero()

        
    envio_data(e_act, 0, 0)

    
#*****************************************************************************************************************************************************
#                                                           TRATAMIENTO DE MODOS
#*****************************************************************************************************************************************************

def envio_data(modo, direccion, velocidad):   
    global fin_modo
    global i
    print("llega esto: ", modo, direccion, velocidad)
#-------------------------------------------------------    MODO 0      (movimientos básicos)    
    if modo == 0: 
        m.mandar_robot(direccion, velocidad)
#-------------------------------------------------------    MODO 1      (giro 180º)
    elif modo == 1:
        if i < 25:                          # Aproximacion de instrucciones para que el robot gire 180º 
            m.mandar_robot(direccion_giro, 0)        
            i += 1
            fin_modo = False
        else: 
            m.mandar_robot(0, 0)
            time.sleep(2)
            fin_modo = True
#-------------------------------------------------------    MODO 2      (Reproducir movimiento grabado en fichero)
    elif modo == 2:
        if i < ordenes:
            direccion, velocidad = leer_orden()
            m.mandar_robot(direccion, velocidad)
            i += 1
            fin_modo = False
        else: 
            print("FIN FICHERO")
            m.mandar_robot(0, 0)
            time.sleep(2)
            fin_modo = True
#-------------------------------------------------------    MODO 3      (Grabar movimiento en fichero)
    elif modo == 3:
        m.mandar_robot(direccion, velocidad)
        escribir_orden(direccion, velocidad)      
#-------------------------------------------------------    MODO 4      (Parada absoluta)
    elif modo == 4:
        m.mandar_robot(0, 0)


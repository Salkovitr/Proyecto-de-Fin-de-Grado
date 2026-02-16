
#*****************************************************************************************************************************************************
# Violeta Toribio Rivera
# Codigo Control comunicación por parte del robot
#*****************************************************************************************************************************************************
#                                                       Importación librerías
#*****************************************************************************************************************************************************

import time


pautas = {'direccion':'0','velocidad':'0','modo':'0'}

# Función que se llama desde la interfaz
def envio_data(modo, direccion, velocidad):  
    pautas['direccion'] = direccion
    pautas['velocidad'] = round( velocidad, 1)
    pautas['modo'] = modo
    print("-------------------------------------")
    print(pautas)
    print("-------------------------------------")


   
    time.sleep(0.05) 

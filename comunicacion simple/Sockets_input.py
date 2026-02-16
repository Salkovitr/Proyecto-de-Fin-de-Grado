# Violeta Toribio Rivera

#Comunicación simple por sockets, sin SSL 

#Importacion de librerias
import socket
import time

HOST = '192.168.176.102'            # Direccion del subsistema salidas
PORT = 50001                        # Puerto donde escucha el subsistema salidas

pautas={'direccion':'','porcentaje':'','modo':''}

# Creación del socket y conexión 
c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
c.connect((HOST,PORT))

def envio_data(modo, direccion, velocidad):  
    try:
        pautas['direccion'] = direccion
        pautas['velocidad'] = round( velocidad, 1)
        pautas['modo'] = modo
        data = bytes(str(pautas), 'utf8')
        c.send(data)
        
        #Se mandan los datos al otro subsistema
        #Se bloquea hasta recibir confirmación del otro subsistema
        data = c.recv(1024)
        if not data: print("ERROR. NO DATA FOUND")
        time.sleep(0.1)
        
        # Captura excepciones para finalizar la ejecución del programa
    except IOError:
        print("Error I/O")
        sys.exit(1)

    except KeyboardInterrupt:
        print("Detenido")
        sys.exit(1)
    
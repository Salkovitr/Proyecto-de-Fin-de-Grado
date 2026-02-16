
#*****************************************************************************************************************************************************
# Violeta Toribio Rivera
# Codigo Control comunicación por parte del robot
#*****************************************************************************************************************************************************
#                                                       Importación librerías
#*****************************************************************************************************************************************************
import socket
import ssl
import time
import sys

#*****************************************************************************************************************************************************
#                                                   Tratamiento de la conexión
#*****************************************************************************************************************************************************    
HOST = 'ROBHELPHUM'         #           Nombre del servidor
IP_HOST = 'localhost'       #           Direccion IP del servidor
PORT = 50001                #           Puerto al que enviar los datos

# Definición de la ubicación de los certificados SSL
CLIENT_CERT = 'certificados_u/user_cer.cer'
CLIENT_KEY = 'certificados_u/user_k.key'
SERVER_CERT = 'certificados_u/robhelphum_cer.cer'

# Creacion del contexto SSL
context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)       ## Creación del contexto SSL con propósito de autenticación del servidor
context.load_cert_chain(certfile=CLIENT_CERT, keyfile=CLIENT_KEY)   ## Carga del certificado y clave del cliente para autenticación mutua
context.load_verify_locations(cafile=SERVER_CERT)                   ## Carga del certificado del servidor para verificar su identidad


# Creacion del socket
s = socket.create_connection((IP_HOST, PORT))
# Creacion del socket seguro
c_sec = context.wrap_socket(s, server_hostname=HOST)

# Revision de certificados 
try:
    ssl.match_hostname(c_sec.getpeercert(), HOST)
    print("La conexión SSL es segura.")
except ssl.CertificateError as e:
    print(f"Error de certificado: {e}")
    sys.exit(1)

pautas = {'direccion':'0','velocidad':'0','modo':'0'}

# Función que se llama desde la interfaz
def envio_data(modo, direccion, velocidad):  
    try:   
        pautas['direccion'] = direccion
        pautas['velocidad'] = round( velocidad, 1)
        pautas['modo'] = modo
        print(pautas)
        data = bytes(str(pautas), 'utf8')

        c_sec.sendall(data)

        data = c_sec.recv(1024)
        if not data: print("ERROR. NO DATA FOUND")
        time.sleep(0.05) 

    # Tratamiento de excepciones         
    except IOError:
        print("Error I/O")
        sys.exit(1)

    except KeyboardInterrupt:
        print("Detenido")
        sys.exit(1)


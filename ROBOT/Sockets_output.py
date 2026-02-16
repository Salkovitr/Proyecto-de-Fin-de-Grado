
#*****************************************************************************************************************************************************
# Violeta Toribio Rivera
# Codigo Control comunicación por parte del robot
#*****************************************************************************************************************************************************
#                                                       Importación librerías
#*****************************************************************************************************************************************************
import Control_Robot as e
import socket
import ssl
import ast      
import hashlib
import sys

#*****************************************************************************************************************************************************
#                                                   Tratamiento de la conexión
#*****************************************************************************************************************************************************
HOST = ''          #           Direccion de escucha (cualquier red disponible)
PORT = 50001       #           Puerto por donde escucha para recibir los datos.

# Definición de la ubicación de los certificados SSL
SERVER_CERT = 'certificados_r/robhelphum_cer.cer'
SERVER_KEY = 'certificados_r/robhelphum_k.key'
USER_CERT = 'certificados_r/user_cer.cer'

# Huella digital (hash) permitida (del certificado del único usuario autorizado)
ALLOWED_FINGERPRINT = "705C1F39FD670F4E174D9A26DCE7038632525EE51CA6930D0DB192A5C076DC48"

# Creacion del socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(1)

# Creacion del contexto SSL
context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)       # Crea un contexto SSL con propósito de autenticación del cliente
context.verify_mode = ssl.CERT_REQUIRED                             # Obliga a que el cliente presente un certificado válido
context.load_cert_chain(certfile=SERVER_CERT, keyfile=SERVER_KEY)   # Carga el certificado y la clave privada del servidor para identificarse
context.load_verify_locations(cafile=USER_CERT)                     # Carga los certificados confiables para verificar al cliente (CA o certificado del cliente)

with context.wrap_socket(s, server_side=True) as s_sec:
    conn, addr = s_sec.accept()
    # Obtener certificado del cliente
    client_cert = conn.getpeercert(binary_form=True)
    with conn:
        try:                                # Intenta conexión
            if client_cert:
                # Calcular la huella digital SHA-256 del certificado recibido
                fingerprint = hashlib.sha256(client_cert).hexdigest().upper()
                print(f"Fingerprint recibido: {fingerprint}")
                if fingerprint != ALLOWED_FINGERPRINT:
                    print("Conexion rechazada: Certificado de cliente no autorizado.")
                    conn.close()
                else:
                    print("Conexion autorizada: Certificado valido.")
                    
                    while True:                     # Bucle infinito de recepción del dato 
                        
                        data = conn.recv(1024)
                        if not data:break
                        pautas = ast.literal_eval(data.decode('utf8'))
####--------------------------------------------------------------#####
                        e.control(pautas)                                           # Llamada a Control_Robot para tratamiento del dato
####--------------------------------------------------------------####
                        conn.send(bytes('True','utf-8'))                            # Señal de que esta listo para la recepción de otro dato
#
            else:
                print("No se recibió un certificado de cliente.")
                e.stop()
                conn.close()
                print('Disonnected by', addr)
            
# Tratamiento de excepciones en la comunicación     
          
        except KeyboardInterrupt:
            print("Detenido")
            e.stop()
            sys.exit(1)
        finally:
            e.stop()            ####__________Asegurarse de que el robot quede quieto
            conn.close()        ###___________Cerrar conexión socket
    
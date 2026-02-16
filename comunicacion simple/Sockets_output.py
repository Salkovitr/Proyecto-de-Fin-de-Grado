# Violeta Toribio Rivera

# Importación de librerias
import Control_Robot as e
import socket
import ast   
import sys  

HOST = ''          
PORT = 50001        #  Puerto donde se escucha la conexión

# Se crea el socket y se espera establecer comunicacion
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    cr.stop()
    s.bind((HOST, PORT))
    s.listen(1)
    conn, addr = s.accept()
    with conn:
        try:
            print('Connected by', addr)
            while True:
                # Se reciven datos y se manda a control
                data = conn.recv(1024)
                if not data:break
                pautas = ast.literal_eval(data.decode('utf8'))
####--------------------------------------------------------------#####
                e.control(pautas)
####--------------------------------------------------------------####
                # Se envía ok al subsistema entradas para recivir mas datos
                conn.send(bytes('True','utf-8'))
        finally:
            e.stop()            ####__________Asegurarse de que el robot quede quieto
            conn.close()        ###___________Cerrar conexión socket y finaliza ejecución del programa
            sys.exit(1)
    
    
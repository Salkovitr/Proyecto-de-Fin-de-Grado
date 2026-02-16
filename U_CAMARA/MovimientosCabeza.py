# Violeta Toribio Rivera
# Código de Alba Payo Fernández ligeramente modificado
# para la comunicación por sockets en el nuevo software


#Código solo Movimientos BASICOS Cabeza 

#Importación de librerías
import cv2
import mediapipe as mp
import numpy as np
from math import acos,degrees
# Importación del fichero de comunicación por sockets
import Sockets_input as sk

#Capturar la cámara
mp_face_detection = mp.solutions.face_detection

# Crear un objeto VideoCapture para conectarse a la transmisión de vídeo de AndroidCam
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: No se pudo abrir la cámara.")
    exit()

#Función que lee los puntos claves de la cara
def leer_coord():
	x1=int(detection.location_data.relative_keypoints[0].x*width)
	y1=int(detection.location_data.relative_keypoints[0].y*height)
	x2=int(detection.location_data.relative_keypoints[1].x*width)
	y2=int(detection.location_data.relative_keypoints[1].y*height)
	x3=int(detection.location_data.relative_keypoints[2].x*width)
	y3=int(detection.location_data.relative_keypoints[2].y*height)
	x4=int(detection.location_data.relative_keypoints[3].x*width)
	y4=int(detection.location_data.relative_keypoints[3].y*height)
	x5=int(detection.location_data.relative_keypoints[4].x*width)
	y5=int(detection.location_data.relative_keypoints[4].y*height)
	x6=int(detection.location_data.relative_keypoints[5].x*width)
	y6=int(detection.location_data.relative_keypoints[5].y*height)
	return x1,y1,x2,y2,x3,y3,x4,y4,x5,y5,x6,y6

#Establecemos la conexión con el otro subsistema

with mp_face_detection.FaceDetection(min_detection_confidence=0.75) as face_detection:
   
    while True: 

        ret, frame=cap.read()
        if ret ==False:break
        frame=cv2.flip(frame,1)
        height,width,_=frame.shape
        frame_rgb=cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
        results=face_detection.process(frame_rgb)
        if results.detections is not None:
            for detection in results.detections:
                x1,y1,x2,y2,x3,y3,x4,y4,x5,y5,x6,y6=leer_coord()
                #Calculamos ángulo de inclinación de los ojos
                p1=np.array([x1,y1])
                p2=np.array([x2,y2])
                p3=np.array([x2,y1])
                d_eyes=np.linalg.norm(p1-p2)
                l1=np.linalg.norm(p1-p3)
                angle=degrees(acos(l1/d_eyes))
                if y1<y2:angle=-angle
                cv2.line(frame,(x1,y1),(x2,y2),(0,255,0),2)
                cv2.line(frame,(x1,y1),(x2,y1),(211,0,148),2)
                cv2.line(frame,(x2,y2),(x2,y1),(0,128,255),2)
                cv2.circle(frame, (x1,y1),5,(0,255,0),-1)
                cv2.circle(frame, (x2,y2),5,(0,0,255),-1)
                cv2.circle(frame, (x3,y3),5,(255,0,0),-1)
                cv2.circle(frame, (x5,y5),5,(255,255,0),-1)
                cv2.circle(frame, (x6,y6),5,(255,255,255),-1)
                #Asignamos dirección y velocidad según ángulo de los ojos y los puntos de la cara
                if(angle>15):
                    direccion=0
                    velocidad=-50
                elif(angle<-15):
                    direccion=0
                    velocidad=50
                elif(x6<x3):
                    direccion=1
                    velocidad=50
                elif(x5>x3):
                    direccion=-1
                    velocidad=50
                else:
                    direccion=0
                    velocidad=0
        else:
            direccion=0
            velocidad=0
        
        # Se envía el resultado al fichero de comunicación por sockets (unicamente modo0)
        sk.envio_data(0, direccion, velocidad)
        print(velocidad, direccion)
        
        cv2.imshow("Frame",frame)
        k=cv2.waitKey(1) & 0xFF
        if k==27:break
        
cap.release()
cv2.destroyAllWindows()
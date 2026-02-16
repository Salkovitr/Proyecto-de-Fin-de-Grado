#*****************************************************************************************************************************************************
# Violeta Toribio Rivera
# Codigo Comunicación con los motores mediante GPIO
#*****************************************************************************************************************************************************
#                                                       Importación librerías
#*****************************************************************************************************************************************************
import RPi.GPIO as GPIO
from math import fabs as abs
#*****************************************************************************************************************************************************
#                                                       GESTION GPIO DE LOS MOTORES
#*****************************************************************************************************************************************************
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Variables de los motores del robot
enaA = 18
in1 = 23
in2 = 24

enaB = 19
in3 = 5
in4 = 6

#*****************************************************************************************************************************************************
#                                                               CLASE MOTOR
#*****************************************************************************************************************************************************

class Motor():
	#Función inicialización
   
	def __init__(self):
		self.EnaA = enaA
		self.In1 = in1
		self.In2 = in2
		self.EnaB = enaB
		self.In3 = in3
		self.In4 = in4
		
		GPIO.setup(self.EnaA, GPIO.OUT)
		GPIO.setup(self.In1, GPIO.OUT)
		GPIO.setup(self.In2, GPIO.OUT)

		GPIO.setup(self.EnaB, GPIO.OUT)
		GPIO.setup(self.In3, GPIO.OUT)
		GPIO.setup(self.In4, GPIO.OUT)


		self.pwmMotorA = GPIO.PWM(self.EnaA, 1000)
		self.pwmMotorB = GPIO.PWM(self.EnaB, 1000)

		self.pwmMotorA.start(0)
		self.pwmMotorB.start(0)
		
	#Función movimiento recto hacia delante
	def moveF(self, x):
		GPIO.output(self.In1, GPIO.HIGH)
		GPIO.output(self.In2, GPIO.LOW)
		GPIO.output(self.In3, GPIO.LOW)
		GPIO.output(self.In4, GPIO.HIGH)
		self.pwmMotorA.ChangeDutyCycle(x)
		self.pwmMotorB.ChangeDutyCycle(x)

	#Función movimiento recto hacia detrás
	def moveB(self, x):
		GPIO.output(self.In1, GPIO.LOW)
		GPIO.output(self.In2, GPIO.HIGH)
		GPIO.output(self.In3, GPIO.HIGH)
		GPIO.output(self.In4, GPIO.LOW)
		self.pwmMotorA.ChangeDutyCycle(x)
		self.pwmMotorB.ChangeDutyCycle(x)
	
	#Función movimiento giro a la izquierda hacia delante
	def moveL(self, x):
		GPIO.output(self.In1, GPIO.HIGH)
		GPIO.output(self.In2, GPIO.LOW)
		GPIO.output(self.In3, GPIO.LOW)
		GPIO.output(self.In4, GPIO.LOW)
		self.pwmMotorA.ChangeDutyCycle(x)
		self.pwmMotorB.ChangeDutyCycle(0)

	#Función movimiento giro a la izquierda hacia detrás
	def moveLB(self, x):
		GPIO.output(self.In1, GPIO.LOW)
		GPIO.output(self.In2, GPIO.LOW)
		GPIO.output(self.In3, GPIO.HIGH)
		GPIO.output(self.In4, GPIO.LOW)
		self.pwmMotorA.ChangeDutyCycle(0)
		self.pwmMotorB.ChangeDutyCycle(x)

	#Función movimiento giro a la derecha hacia delante	
	def moveR(self, x):
		GPIO.output(self.In1, GPIO.LOW)
		GPIO.output(self.In2, GPIO.LOW)
		GPIO.output(self.In3, GPIO.LOW)
		GPIO.output(self.In4, GPIO.HIGH)
		self.pwmMotorA.ChangeDutyCycle(0)
		self.pwmMotorB.ChangeDutyCycle(x)

	#Función movimiento giro a la derecha hacia detrás
	def moveRB(self, x):
		GPIO.output(self.In1, GPIO.LOW)
		GPIO.output(self.In2, GPIO.HIGH)
		GPIO.output(self.In3, GPIO.LOW)
		GPIO.output(self.In4, GPIO.LOW)
		self.pwmMotorA.ChangeDutyCycle(x)
		self.pwmMotorB.ChangeDutyCycle(0)

	#Función no movimiento
	def stop(self):
		GPIO.output(self.In1, GPIO.LOW)
		GPIO.output(self.In2, GPIO.LOW)
		GPIO.output(self.In3, GPIO.LOW)
		GPIO.output(self.In4, GPIO.LOW)
		self.pwmMotorA.ChangeDutyCycle(0)
        
    #Funciones giro 180 grados: 
	def giro_180_i(self):
		      # SENTIDO ANTIHORARIO
		GPIO.output(self.In1, GPIO.HIGH)
		GPIO.output(self.In2, GPIO.LOW)
		GPIO.output(self.In3, GPIO.HIGH)
		GPIO.output(self.In4, GPIO.LOW)
		self.pwmMotorA.ChangeDutyCycle(50)
		self.pwmMotorB.ChangeDutyCycle(50)
        
	def giro_180_d(self):
		GPIO.output(self.In1, GPIO.LOW)
		GPIO.output(self.In2, GPIO.HIGH)
		GPIO.output(self.In3, GPIO.LOW)
		GPIO.output(self.In4, GPIO.HIGH)
		self.pwmMotorA.ChangeDutyCycle(50)
		self.pwmMotorB.ChangeDutyCycle(50)
            
            
motor1 = Motor()


#Función que según la dirección y velocidad llama a las de movimiento

def mandar_robot(direccion, velocidad):

	if velocidad == 0:
		if direccion == 1:                              #Giro 180 a la derecha
			motor1.giro_180_d()
		elif direccion == -1:                           #Giro 180 a la izquierda
			motor1.giro_180_i()
		else:
			motor1.stop()								# Estado sin movimiento
	else:
		if direccion == 0 and velocidad > 0: 			# Movimiento hacia delante
			motor1.moveF(velocidad)
		elif direccion == 0 and velocidad < 0: 			# Movimiento hacia detras
			motor1.moveB(abs(velocidad))
		elif direccion == 1 and velocidad > 0: 			# Giro hacia delante-derecha
			motor1.moveR(velocidad)
		elif direccion == 1 and velocidad < 0:			# Giro hacia detras-derecha
			motor1.moveRB(abs(velocidad))
		elif direccion == -1 and velocidad > 0:			# Giro hacia delante-izquierda
			motor1.moveL(velocidad)
		else: 											# Giro hacia detras-izquierda
			motor1.moveLB(abs(velocidad))
            

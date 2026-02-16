#*****************************************************************************************************************************************************
# Violeta Toribio Rivera
# Codigo Automata de estados
#*****************************************************************************************************************************************************
#                                                       Importación librerías
#*****************************************************************************************************************************************************
from enum import Enum

#*****************************************************************************************************************************************************
#                                                        ESTADOS
#*****************************************************************************************************************************************************
 
class Estado(Enum):
    ESTADO0 = 0
    ESTADO1 = 1
    ESTADO2 = 2
    ESTADO3 = 3
    ESTADO4 = 4
#*****************************************************************************************************************************************************
#                                                   CLASE AUTOMATA
#*****************************************************************************************************************************************************    
# Controla las transiciones de los distintos estados con su funcion transitar y devuelve si existe transicion y si finalmente se realiza la transición.
# Tiene otras funciones como indicar estado actual (obtener_estado) y para el control del numero de entradas iguales (cuenta_entradas y tiempo_reset) 
    
class Automata:
    def __init__(self):
        self.estado_actual = Estado.ESTADO0
        self.lista_modos = [0, 1, 2, 3, 4, 5]
        self.pausa = 35                                          # Constante para el cambio de estado (numero de ordenes iguales para el cambio de estado)
        self.contador = {modo: 0 for modo in self.lista_modos}  # Contador de número de entradas iguales para cada modo en la lista
        self.transiciones = {
            Estado.ESTADO0: {   1: (False , Estado.ESTADO1),
                                2: (False, Estado.ESTADO2),
                                3: (False, Estado.ESTADO3), 
                                4: (False, Estado.ESTADO4)},                #       True si transita enseguida
#                                                                           #       False si debe cumplir un numero de entradas
            Estado.ESTADO1: {   'FIN': (True, Estado.ESTADO0),
                                4: (False, Estado.ESTADO4)},
                    
            Estado.ESTADO2: {   'FIN': (True, Estado.ESTADO0),
                                4: (False, Estado.ESTADO4)},
        
            Estado.ESTADO3: {   4: (False, Estado.ESTADO4),
                                5: (False, Estado.ESTADO0)},
                                
            Estado.ESTADO4: {   5: (False, Estado.ESTADO0)}
            }
            
    def transitar(self, modo):                                  ## Si es una transicion factible y cumple la condicion --> transita y guarda un nuevo estado
        if modo in self.transiciones[self.estado_actual]:
            cond, nuevo_estado = self.transiciones[self.estado_actual][modo]
            if not cond:                                                # Si es False, se evalua el tiempo de espera
                cond = self.cuenta_entradas(modo)            
            if cond:                                            # Si cumple la condicion, realiza transicion, actualiza estado actual y resetea contadores
                self.estado_actual = nuevo_estado    
                self.tiempo_reset()
                return True, True                               # Transita, por lo tanto, existe transicion
            else: return True, False                            # existe transicion (true), pero no transita (false)
        else: return False, False                               # No existe transicion ni tampoco transita
        
    def obtener_estado(self):                                   # Devuelve el estado actual, el último guardado
        return self.estado_actual.value
        
    def cuenta_entradas(self, modo):                            # Contador de numero de entradas iguales
        self.contador[modo] += 1
        return self.contador[modo] >= self.pausa 
           
    def tiempo_reset(self):                                     # Resetea contador tras una transicion
        for i in self.contador:
            self.contador[i] = 0
            
        


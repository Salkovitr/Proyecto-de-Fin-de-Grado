
import Sockets_input_texto as sk
import keyboard

num = 0
modo = 0
direccion = 0


def on_key_event(num, key):
    # Esta función se llama cuando se presiona una tecla
    
    for _ in range(num):

        if key == 'a':
            print("Mano derecha: giro izquierda")
            print("Mano izquierda: abajo")
            sk.envio_data(0,-1,-25)
        elif key == 's':
            print("Mano derecha: neutra")
            print("Mano izquierda: abajo")
            sk.envio_data(0,0,-30)
        elif key == 'd':
            print("Mano derecha: neutra")
            print("Mano izquierda: neutra")
            sk.envio_data(0,0,0)
        elif key == 'q':
            print("Mano derecha: gira izquierda")
            print("Mano izquierda: arriba")
            sk.envio_data(0,-1,46)
        if key == 'w':
            print("Mano derecha: neutra")
            print("Mano izquierda: arriba")
            sk.envio_data(0,0,65)
        elif key == 'e':
            print("Mano derecha: giro derecha")
            print("Mano izquierda: arriba")
            sk.envio_data(0,1,90)
        elif key == 'o':
            print("Mano derecha: arriba")
            print("Mano izquierda: gira izquierda")
            sk.envio_data(1,-1,0)
        elif key == 'p':
            print("Mano derecha: arriba")
            print("Mano izquierda: gira derecha")
            sk.envio_data(1,1,0)
        elif key == 'z':
            print("Mano derecha: arriba")
            print("Mano izquierda: abajo")
            sk.envio_data(2,0,0)
        elif key == 'x':
            print("Mano derecha: abajo")
            print("Mano izquierda: arriba")
            sk.envio_data(3,0,0)
        elif key == 'c':
            print("Mano derecha: arriba")
            print("Mano izquierda: arriba")
            sk.envio_data(4,0,0)
        elif key == 'v':
            print("Mano derecha: abajo")
            print("Mano izquierda: abajo")
            sk.envio_data(5,0,0)
        elif key == 'b':
            print("Mano derecha: mal")
            print("Mano izquierda: mal")
            sk.envio_data(999,0,0)
        elif key == 'esc':
            print("Proceso interrumpido por el usuario.")
            keyboard.unhook_all()  # Desregistrar todos los eventos de teclado
            exit()

while True:

    num = int(input("num: ").strip())

    letra = input("modo: ").strip()
    on_key_event(num, letra)
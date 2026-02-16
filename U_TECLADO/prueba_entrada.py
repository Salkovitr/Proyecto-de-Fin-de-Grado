




import Sockets_input as sk
import keyboard

num = 0
modo = 0
direccion = 0


def on_key_event(num, key):
    # Esta función se llama cuando se presiona una tecla
    
    for _ in range(num):


        if key == 'a':
            sk.envio_data(0,-1,-25)
        elif key == 's':
            sk.envio_data(0,0,-30)
        elif key == 'd':
            sk.envio_data(0,0,0)
        elif key == 'q':
            sk.envio_data(0,-1,46)
        if key == 'w':
            sk.envio_data(0,0,65)
        elif key == 'e':
            sk.envio_data(0,1,90)
        elif key == 'o':
            sk.envio_data(1,-1,0)
        elif key == 'p':
            sk.envio_data(1,1,0)
        elif key == 'z':
            sk.envio_data(2,0,0)
        elif key == 'x':
            sk.envio_data(3,0,0)
        elif key == 'c':
            sk.envio_data(4,0,0)
        elif key == 'v':
            sk.envio_data(5,0,0)
        elif key == 'b':
            sk.envio_data(999,0,0)
        elif key == 'esc':
            print("Proceso interrumpido por el usuario.")
            keyboard.unhook_all()  # Desregistrar todos los eventos de teclado
            exit()

while True:

    num = int(input("num: ").strip())

    letra = input("modo: ").strip()
    on_key_event(num, letra)
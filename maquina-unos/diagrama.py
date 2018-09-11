import tkinter as tk
import time
from tkinter import font as tkfont
from turing import MaquinaTuring

# Tabla de transiciones que modela el automata
transiciones = {
            ("q0", "1"): ("q1", "X", "R"),
            ("q0", "Y"): ("q3", "1", "R"),
            ("q1", "1"): ("q1", "1", "R"),
            ("q1", "Y"): ("q1", "Y", "R"),
            ("q1", "B"): ("q2", "Y", "L"),
            ("q2", "1"): ("q2", "1", "L"),
            ("q2", "X"): ("q0", "1", "R"),
            ("q2", "Y"): ("q2", "Y", "L"),
            ("q3", "Y"): ("q3", "1", "R"),
            }

entrada = input("Ingrese la cadena de unos: ")
maquina = MaquinaTuring("q0", "q3", entrada, transiciones)

# Configuracion de la ventana
gui = tk.Tk()
gui.geometry("600x400+100+100")
gui.title("Maquina de Turing")
c = tk.Canvas(gui, width=600, height=400)
c.pack()
bold_font = tkfont.Font(family="Arial", size=24)

# Principales componentes que se animan
control = c.create_rectangle(150, 100, 200, 150, fill="lightblue")
flecha = c.create_line(175, 150, 175, 175, arrow=tk.LAST, width=3)
texto = c.create_text(165, 200, text=''.join(maquina.cinta), font=bold_font,
                      anchor=tk.W)
estado = c.create_text(160, 125, text=maquina.estado_actual, font=bold_font,
                       anchor=tk.W)

archivo = open("salida.txt", "w+")
# Mientras no llegues a un estado final continua
while not maquina.es_final():
    print('Cadena: {}'.format(''.join(maquina.cinta)))
    print('Estado actual: {}, apuntador: {}'.format(maquina.estado_actual,
          maquina.apuntador+1))

    archivo.write('Cadena: {}\n'.format(''.join(maquina.cinta)))
    archivo.write('Estado actual: {}, apuntador: {}\n'
                  .format(maquina.estado_actual, maquina.apuntador+1))
    if not maquina.consumir():
        print('*' * 20)
        archivo.write('*' * 20)
        archivo.write('\n')
        break
    print('Siguiente estado: {}'.format(maquina.estado_actual))
    print('*'*20)

    archivo.write('Siguiente estado: {}\n'.format(maquina.estado_actual))
    archivo.write('*' * 20)
    archivo.write('\n')

    gui.update()
    time.sleep(1)
    c.itemconfigure(texto, text=''.join(maquina.cinta), anchor=tk.W)
    c.itemconfigure(estado, text=maquina.estado_actual)
    if maquina.direccion == 'R':
        c.move(control, 19, 0)
        c.move(flecha, 19, 0)
        c.move(estado, 19, 0)
    else:
        c.move(control, -19, 0)
        c.move(estado, -19, 0)
        c.move(flecha, -19, 0)

print('Cadena final: {}'.format(''.join(maquina.cinta)))
archivo.write('Cadena final: {}\n'.format(''.join(maquina.cinta)))
archivo.close()
gui.mainloop()

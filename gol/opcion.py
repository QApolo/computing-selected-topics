from tkinter import *
import numpy as np
import time

master = Tk()

tam = 500
tam_cuadro = 2

ceros = "red"
unos = "blue"
w = Canvas(master, width=1000, height=800)
w.pack()
a = np.zeros(shape=(tam, tam), dtype=int)
celulas = np.random.randint(2, size=(tam, tam))
for i in range(tam):
    for j in range(tam):
        if celulas[i][j] == 0:
            a[i][j] = w.create_rectangle(0 + (i*tam_cuadro), 0 + (j*tam_cuadro), tam_cuadro + (i*tam_cuadro), tam_cuadro + (j*tam_cuadro), fill=ceros, width=0)
        else:
            a[i][j] = w.create_rectangle(0 + (i*tam_cuadro), 0 + (j*tam_cuadro), tam_cuadro + (i*tam_cuadro), tam_cuadro + (j*tam_cuadro), fill=unos, width=0)

w.update_idletasks()

def helloCallBack():
   print("HOLA")

button1 = Button(master, text = "Quit", command = helloCallBack, anchor = E)
button1_window = w.create_window(10, 10, anchor=NW, window=button1)

for k in range(10):
    print("iteracion")
    nueva_poblacion = celulas.copy()
    for i in range(tam):
        print(i)
        for j in range(tam):
            vecinos = (celulas[i - 1, j - 1] + celulas[i - 1, j] + celulas[i - 1, (j + 1) % tam]
                       + celulas[i, (j + 1) % tam] + celulas[(i + 1) % tam, (j + 1) % tam]
                       + celulas[(i + 1) % tam, j] + celulas[(i + 1) % tam, j - 1] + celulas[i, j - 1])

            if celulas[i, j] == 1:
                if vecinos < 2 or vecinos > 3:
                    nueva_poblacion[i, j] = 0
                    w.itemconfig(a[i][j], fill=ceros)
            else:
                if vecinos >= 3 and vecinos <= 3:
                    nueva_poblacion[i, j] = 1
                    w.itemconfig(a[i][j], fill=unos)

    celulas[:] = nueva_poblacion[:]
    w.update_idletasks()
    w.update()
    time.sleep(1)

mainloop()
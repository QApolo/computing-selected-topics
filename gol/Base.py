from tkinter import Tk, Canvas, Frame, Button, Scrollbar
from tkinter import BOTH, W, NW, SUNKEN, TOP, X, FLAT, LEFT, NE, E, Y, HORIZONTAL, VERTICAL, BOTTOM, RIGHT
import numpy as np
import time

class Example(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.parent = parent
        self.pausa = True
        self.tam = 1000
        self.tam_cuadro = 2
        self.ceros = "red"
        self.unos = "blue"
        self.a = np.zeros(shape=(self.tam, self.tam), dtype=int)
        self.celulas = np.random.randint(2, size=(self.tam, self.tam))
        self.canvas = None
        self.initUI()
        self.update()
        self.animacion()

    def initUI(self):
        self.parent.title("Layout Test")
        self.config(bg = '#F0F0F0')
        self.pack(fill = BOTH, expand = 1)
        #create canvas
        self.canvas1 = Canvas(self, relief = 'raised', width = self.tam, height = self.tam)

        self.canvas1.pack(side = LEFT)
        for i in range(self.tam):
            for j in range(self.tam):
                if self.celulas[i][j] == 0:
                    self.a[i][j] = self.canvas1.create_rectangle(0 + (i * self.tam_cuadro), 0 + (j * self.tam_cuadro),
                                                       self.tam_cuadro + (i * self.tam_cuadro), self.tam_cuadro + (j * self.tam_cuadro),
                                                 fill=self.ceros, width=0)
                else:
                    self.a[i][j] = self.canvas1.create_rectangle(0 + (i * self.tam_cuadro), 0 + (j * self.tam_cuadro),
                                                       self.tam_cuadro + (i * self.tam_cuadro), self.tam_cuadro + (j * self.tam_cuadro),
                                                 fill=self.unos, width=0)
        #add quit button
        button1 = Button(self, text="Pausa/Reanudar", command=self.empezar_dentener)
        button1.configure(width=10, activebackground="#33B5E5")
        #button1_window = canvas1.create_window(610, 10, anchor=NE, window=button1)
        button1.pack(side = TOP)

    def empezar_dentener(self):
        print("empezar_detener")
        self.pausa = not self.pausa

    def animacion(self):
        print("ANIMACION")
        if not self.pausa:
            nueva_poblacion = self.celulas.copy()
            for i in range(self.tam):
                print(i)
                for j in range(self.tam):
                    vecinos = (self.celulas[i - 1, j - 1] + self.celulas[i - 1, j] + self.celulas[i - 1, (j + 1) % self.tam]
                               + self.celulas[i, (j + 1) % self.tam] + self.celulas[(i + 1) % self.tam, (j + 1) % self.tam]
                               + self.celulas[(i + 1) % self.tam, j] + self.celulas[(i + 1) % self.tam, j - 1] + self.celulas[i, j - 1])
                    if self.celulas[i, j] == 1:
                        if vecinos < 2 or vecinos > 3:
                            nueva_poblacion[i, j] = 0
                            self.canvas1.itemconfig(self.a[i][j], fill=self.ceros)
                    else:
                        if vecinos >= 3 and vecinos <= 3:
                            nueva_poblacion[i, j] = 1
                            self.canvas1.itemconfig(self.a[i][j], fill=self.unos)

            self.celulas[:] = nueva_poblacion[:]
            self.update_idletasks()
            print("Termino")
        self.after(1000, self.animacion)

def main():
    root = Tk()
    root.geometry('800x600+10+50')
    app = Example(root)
    app.mainloop()

main()
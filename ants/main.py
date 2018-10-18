from tkinter import Tk, Frame, Canvas, Button, Label, Entry, Scale
import tkinter as tk
from tkcolorpicker import askcolor
import numpy as np
import random as pyrandom
from hormiga import Hormiga, colores_dict


class Ventana(Frame):
    def __init__(self, parent):
        # Elemetnso de la interfaz
        Frame.__init__(self, parent)
        self.parent = parent
        self.canvas = None
        self.input_tam = None
        self.barra = None
        self.default_color = "white"

        # Elementos de control
        self.cuadros = None
        self.matriz = None
        self.tam = 500
        self.tam_cuadro = 2
        self.hormigas = list()
        self.pausa = True
        self.distribucion = .05

    def init_ui(self):
        self.parent.title("Hormiga de Lagnton")
        self.pack(fill=tk.BOTH, expand=1)

        self.canvas = Canvas(self, relief='raised', width=1000, height=1000)
        self.canvas.pack(side=tk.LEFT)

        Label(self, text="Tamaño:", font=(20,)).pack(side=tk.TOP)
        self.input_tam = Entry(self, fg="black", bg="white")
        self.input_tam.insert(10, "100")
        self.input_tam.pack(side=tk.TOP)

        Label(self, text="Porcentaje de hormigas", font=(20,)).pack(side=tk.TOP)
        self.barra = Scale(self, from_=0, to=100, orient=tk.HORIZONTAL, tickinterval=50)
        self.barra.set(5)
        self.barra.pack(side=tk.TOP)

        self.btn_color = Button(self, text="Color de la hormiga", command=self.get_color, bg=self.default_color)
        self.btn_color.pack(side=tk.TOP)

        btn_iniciar = Button(self, text="Iniciar/Reiniciar", command=self.iniciar, font=(20,))
        btn_iniciar.pack(side=tk.TOP)

        btn_pausa = Button(self, text="Reanudar/Pausa", command=self.empezar_detener, font=(20,))
        btn_pausa.pack(side=tk.TOP)

        Label(self, text="Relación de colores y \n posicion de las hormiga:", font=(20,)).pack(side=tk.TOP)
        Label(self, text="Abajo", bg="blue", font=(20,)).pack(side=tk.TOP)
        Label(self, text="Arriba", bg="red", font=(20,)).pack(side=tk.TOP)
        Label(self, text="Izquierda", bg="green", font=(20,)).pack(side=tk.TOP)
        Label(self, text="Derecha", bg="yellow", fg="black", font=(20,)).pack(side=tk.TOP)

    def iniciar(self):
        print("iniciar")
        self.hormigas[:] = []
        self.canvas.delete('all')
        self.update_idletasks()

        self.tam = int(self.input_tam.get())
        self.tam_cuadro = 0
        while self.tam_cuadro * self.tam < 1000:
            self.tam_cuadro += 1
        if self.tam_cuadro * self.tam > 1000:
            self.tam_cuadro -= 1

        self.distribucion = self.barra.get() / 100

        self.pausa = True
        self.cuadros = np.zeros(shape=(self.tam, self.tam), dtype=int)
        self.matriz = np.random.choice([1, 0], size=(self.tam, self.tam), p=[self.distribucion, 1-self.distribucion])
        self.redibujar()

    def get_color(self):
        color = askcolor()
        if not color[1] == None:
            self.default_color = color[1]
            self.btn_color.configure(bg=self.default_color)


    def empezar_detener(self):
        print("empezar_detener")
        self.pausa = not self.pausa
        self.animacion()

    def animacion(self):
        if not self.pausa:
            for hormiga in self.hormigas:
                if self.matriz[hormiga.y, hormiga.x] == 0:
                    self.matriz[hormiga.y, hormiga.x] = 1
                    self.canvas.itemconfig(self.cuadros[hormiga.y, hormiga.x], fill=hormiga.color)
                    hormiga.mover(0)
                else:
                    self.matriz[hormiga.y, hormiga.x] = 0
                    self.canvas.itemconfig(self.cuadros[hormiga.y, hormiga.x], fill="black")
                    hormiga.mover(1)

                self.canvas.itemconfig(self.cuadros[hormiga.y, hormiga.x], fill=colores_dict[hormiga.orientacion])

            self.update_idletasks()
            self.after(5, self.animacion)

    def pulsar_cuadrito(self, event):
        print("pulsar_cuadrito")
        item = self.canvas.find_closest(event.x, event.y)[0]
        y, x = np.where(self.cuadros == item)
        crear = True
        for hormiga in self.hormigas:
            if hormiga.x == x and hormiga.y == y:
                hormiga.cambiar()
                crear = False
                self.canvas.itemconfig(item, fill=colores_dict[hormiga.orientacion])
                break

        if crear:
            hormiga = Hormiga(x[0], y[0], self.tam)
            hormiga.color = self.default_color
            self.hormigas.append(hormiga)
            self.canvas.itemconfig(item, fill=colores_dict[hormiga.orientacion])

    def redibujar(self):
        print("redibujar")
        for i in range(self.tam):
            for j in range(self.tam):
                if self.matriz[i, j] == 1:
                    self.matriz[i, j] = 0
                    hormiga = Hormiga(j, i, self.tam)
                    hormiga.orientacion = np.random.choice(['N', 'S', 'E', 'O'])
                    hormiga.color = "#%06x" % pyrandom.randint(0, 0xFFFFFF)
                    self.cuadros[i, j] = self.canvas.create_rectangle(0 + (j * self.tam_cuadro),
                                                                      0 + (i * self.tam_cuadro),
                                                                      self.tam_cuadro + (j * self.tam_cuadro),
                                                                      self.tam_cuadro + (i * self.tam_cuadro),
                                                                      fill=colores_dict[hormiga.orientacion],
                                                                      width=0, tag="btncuadrito")
                    self.hormigas.append(hormiga)
                else:
                    self.cuadros[i, j] = self.canvas.create_rectangle(0 + (j * self.tam_cuadro),
                                                                      0 + (i * self.tam_cuadro),
                                                                      self.tam_cuadro + (j * self.tam_cuadro),
                                                                      self.tam_cuadro + (i * self.tam_cuadro),
                                                                      fill="black", width=0, tag="btncuadrito")
        self.canvas.tag_bind("btncuadrito", "<Button-1>", self.pulsar_cuadrito)
        self.update_idletasks()


def main():
    root = Tk()
    root.geometry("1360x750+0+0")
    app = Ventana(root)
    app.init_ui()
    app.mainloop()


main()

from tkinter import Tk, Frame, Canvas, Button, Label, Entry, Scale, Scrollbar, Radiobutton, IntVar
import tkinter as tk
import numpy as np
from hormiga import Soldado, Hormiga, Reina, colores_dict


class Ventana(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.parent = parent
        self.canvas = None
        self.input_tam = None
        self.barra = None

        # Elementos de control
        self.cuadros = None
        self.matriz = None
        self.tam = 100
        self.tam_cuadro = 10
        self.hormigas = list()
        self.pausa = True
        self.distribucion = .05
        self.mi_var = IntVar()
        self.mi_var.set(1)
        self.radio1 = None
        self.radio2 = None
        self.radio3 = None
        self.tiempo = 0
        self.contador = [0, 0, 0]

    def init_ui(self):
        self.parent.title("Hormiga de Lagnton")
        self.pack(fill=tk.BOTH, expand=1)

        self.canvas = Canvas(self, relief='raised', width=1000, height=1000)
        scroll = Scrollbar(self, orient=tk.VERTICAL)
        scroll.pack(side=tk.RIGHT, fill=tk.Y)
        scroll.config(command=self.canvas.yview)

        self.canvas.config(yscrollcommand=scroll.set)
        self.canvas.pack(side=tk.LEFT)

        Label(self, text="Tamaño:", font=(20,)).pack(side=tk.TOP)
        self.input_tam = Entry(self, fg="black", bg="white")
        self.input_tam.insert(10, "100")
        self.input_tam.pack(side=tk.TOP)

        Label(self, text="Porcentaje de hormigas", font=(20,)).pack(side=tk.TOP)
        self.barra = Scale(self, from_=0, to=100, orient=tk.HORIZONTAL, tickinterval=50)
        self.barra.set(5)
        self.barra.pack(side=tk.TOP)

        Label(self, text="Tipo de hormiga:", font=(20,)).pack(side=tk.TOP)
        self.radio1 = Radiobutton(self, text="Obrera", variable=self.mi_var, value=1, command=self.seleccion,
                                  indicatoron=False, selectcolor="white", font=(20,), fg="black")
        self.radio2 = Radiobutton(self, text="Soldado", variable=self.mi_var, value=2, command=self.seleccion,
                                  indicatoron=False, selectcolor="orange", font=(20,), fg="black")
        self.radio3 = Radiobutton(self, text="Reina", variable=self.mi_var, value=3, command=self.seleccion,
                                  indicatoron=False, selectcolor="purple", font=(20,), fg="black")
        self.radio1.pack(side=tk.TOP)
        self.radio2.pack(side=tk.TOP)
        self.radio3.pack(side=tk.TOP)
        self.radio1.select()
        self.radio2.deselect()
        self.radio3.deselect()

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
        self.contador[:] = [0, 0, 0]
        self.tiempo = 0
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

    def seleccion(self):
        print(str(self.mi_var.get()))

    def redibujar(self):
        print("redibujar")
        for i in range(self.tam):
            for j in range(self.tam):
                if self.matriz[i, j] == 1:
                    self.matriz[i, j] = 0
                    tipo = np.random.choice([1, 2, 3], p=[.9, .09, .01])
                    if tipo == 1:
                        hormiga = Hormiga(j, i, self.tam)
                        self.contador[0] += 1
                    elif tipo == 2:
                        hormiga = Soldado(i, j, self.tam)
                        self.contador[1] += 1
                    else:
                        hormiga = Reina(i, j, self.tam)
                        self.contador[2] += 1
                    hormiga.orientacion = np.random.choice(['N', 'S', 'E', 'O'])
                    self.cuadros[i, j] = self.canvas.create_rectangle(0 + (j * self.tam_cuadro),
                                                                      0 + (i * self.tam_cuadro),
                                                                      self.tam_cuadro + (j * self.tam_cuadro),
                                                                      self.tam_cuadro + (i * self.tam_cuadro),
                                                                      fill=hormiga.color,
                                                                      width=0, tag="btncuadrito")
                    self.hormigas.append(hormiga)
                else:
                    self.cuadros[i, j] = self.canvas.create_rectangle(0 + (j * self.tam_cuadro),
                                                                      0 + (i * self.tam_cuadro),
                                                                      self.tam_cuadro + (j * self.tam_cuadro),
                                                                      self.tam_cuadro + (i * self.tam_cuadro),
                                                                      fill="black", width=0, tag="btncuadrito")
        self.canvas.tag_bind("btncuadrito", "<Button-1>", self.pulsar_cuadrito)
        self.canvas.tag_bind("btncuadrito", "<Button-2>", self.borrar_cuadrito)
        self.update_idletasks()
        print(self.contador)

    def borrar_cuadrito(self, event):
        print("borrar_cuadrito")

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
            if self.mi_var.get() == 1:
                hormiga = Hormiga(x[0], y[0], self.tam)
            elif self.mi_var.get() == 2:
                hormiga = Soldado(x[0], y[0], self.tam)
            else:
                hormiga = Reina(x[0], y[0], self.tam)
            self.hormigas.append(hormiga)
            self.canvas.itemconfig(item, fill=colores_dict[hormiga.orientacion])

    def animacion(self):
        pass

    def empezar_detener(self):
        print("empezar_detener")
        self.pausa = not self.pausa
        self.animacion()


def main():
    root = Tk()
    root.geometry("1360x750+0+0")
    app = Ventana(root)
    app.init_ui()
    app.mainloop()


main()

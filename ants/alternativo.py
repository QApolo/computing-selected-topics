from tkinter import Tk, Frame, Canvas, Button, Label, Entry, Scale, Scrollbar, Radiobutton, IntVar
import tkinter as tk
import numpy as np
from hormiga import Soldado, Hormiga, Reina, colores_dict, tipos_dict
import datetime
import time


class Ventana(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.parent = parent
        self.canvas = None
        self.input_tam = None
        self.barra = None
        self.barra_normal = None
        self.barra_soldado = None
        self.barra_reina = None

        self.tiempo_vida = 50
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
        self.nom_archivo = "{}.csv".format(self.obtener_hora())
        self.archivo = None
        self.probabilidades = [.9, .08, .02]

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

        Label(self, text="Probabilidad de horigas normales:", font=(20,)).pack(side=tk.TOP)
        self.barra_normal = Scale(self, from_=0, to=100, orient=tk.HORIZONTAL, tickinterval=50)
        self.barra_normal.set(90)
        self.barra_normal.pack(side=tk.TOP)

        Label(self, text="Probabilidad de horigas soldado:", font=(20,)).pack(side=tk.TOP)
        self.barra_soldado = Scale(self, from_=0, to=100, orient=tk.HORIZONTAL, tickinterval=50)
        self.barra_soldado.set(8)
        self.barra_soldado.pack(side=tk.TOP)

        Label(self, text="Probabilidad de horigas reina:", font=(20,)).pack(side=tk.TOP)
        self.barra_reina = Scale(self, from_=0, to=100, orient=tk.HORIZONTAL, tickinterval=50)
        self.barra_reina.set(2)
        self.barra_reina.pack(side=tk.TOP)

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
        self.nom_archivo = "{}.csv".format(self.obtener_hora())
        self.archivo = open(self.nom_archivo, "w")
        self.archivo.close()
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

    def crear_hormiga(self, j, i):
        tipo = np.random.choice([1, 2, 3], p=self.probabilidades)
        if tipo == 1:
            hormiga = Hormiga(j, i, self.tam)
            self.contador[0] += 1
        elif tipo == 2:
            hormiga = Soldado(j, i, self.tam)
            self.contador[1] += 1
        else:
            hormiga = Reina(j, i, self.tam)
            self.contador[2] += 1
        hormiga.orientacion = np.random.choice(['N', 'S', 'E', 'O'])
        return hormiga

    @staticmethod
    def obtener_hora():
        return datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d_%H:%M:%S')

    def redibujar(self):
        print("redibujar")
        for i in range(self.tam):
            for j in range(self.tam):
                if self.matriz[i, j] == 1:
                    self.matriz[i, j] = 0
                    hormiga = self.crear_hormiga(j, i)
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
        self.canvas.tag_bind("btncuadrito", "<Button-3>", self.borrar_cuadrito)
        self.update_idletasks()
        print(self.contador)

    def borrar_cuadrito(self, event):
        print("borrar_cuadrito")
        item = self.canvas.find_closest(event.x, event.y)[0]
        y, x = np.where(self.cuadros == item)
        contador = 0
        for hormiga in self.hormigas:
            if hormiga.x == x and hormiga.y == y:
                self.contador[hormiga.tipo-1] -= 1
                if self.matriz[hormiga.y, hormiga.x] == 1:
                    self.canvas.itemconfig(item, fill="white")
                else:
                    self.canvas.itemconfig(item, fill="black")
                break
            contador += 1
        if contador < len(self.hormigas):
            self.hormigas.pop(contador)

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
                self.contador[0] += 1
            elif self.mi_var.get() == 2:
                hormiga = Soldado(x[0], y[0], self.tam)
                self.contador[1] += 1
            else:
                hormiga = Reina(x[0], y[0], self.tam)
                self.contador[2] += 1
            self.hormigas.append(hormiga)
            self.canvas.itemconfig(item, fill=colores_dict[hormiga.orientacion])

    def animacion(self):
        if not self.pausa:
            archivo = open(self.nom_archivo, "a")
            archivo.write("{},{},{},{}\n".format(self.tiempo, self.contador[0], self.contador[1], self.contador[2]))
            archivo.close()
            reinas = list()
            soldados = list()
            cont = 0
            for hormiga in self.hormigas:
                if hormiga.tipo == tipos_dict["reina"]:
                    reinas.append(cont)
                elif hormiga.tipo == tipos_dict["soldado"]:
                    soldados.append(cont)
                cont += 1
            for i in reinas:
                for j in soldados:
                    if self.hormigas[i].x == self.hormigas[j].x and self.hormigas[i].y == self.hormigas[j].y:
                            self.hormigas.append(self.crear_hormiga(self.hormigas[i].x, self.hormigas[i].y))

            conjunto = set()
            for hormiga in self.hormigas:
                if hormiga.vida == self.tiempo_vida:
                    self.contador[hormiga.tipo-1] -= 1
                    self.hormigas.remove(hormiga)
                    continue
                if self.matriz[hormiga.y, hormiga.x] == 0:
                    if (hormiga.y, hormiga.x) not in conjunto:
                        self.matriz[hormiga.y, hormiga.x] = 1
                        conjunto.add((hormiga.y, hormiga.x))
                    self.canvas.itemconfig(self.cuadros[hormiga.y, hormiga.x], fill=hormiga.color)
                    hormiga.mover(0)
                else:
                    if (hormiga.y, hormiga.x) not in conjunto:
                        self.matriz[hormiga.y, hormiga.x] = 0
                        conjunto.add((hormiga.y, hormiga.x))
                    self.canvas.itemconfig(self.cuadros[hormiga.y, hormiga.x], fill="black")
                    hormiga.mover(1)
                self.canvas.itemconfig(self.cuadros[hormiga.y, hormiga.x], fill=colores_dict[hormiga.orientacion])

            self.update_idletasks()
            self.after(100, self.animacion)
            self.tiempo += 1

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

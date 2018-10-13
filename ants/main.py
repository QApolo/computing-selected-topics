from tkinter import Tk, Frame, Canvas, Button
import tkinter as tk
import numpy as np

colores_dict = {
    "N": "red",
    "S": "blue",
    "E": "yellow",
    "O": "green",
}


class Hormiga:
    def __init__(self, x=0, y=0, limite=0):
        """Direcciones:
        N -> Norte
        S -> Sur
        E -> Este
        O -> Oeste """
        self.x = x
        self.y = y
        self.limite = limite
        self.orientacion = 'S'

    def mover(self, direccion):
        if direccion == 0:
            if self.orientacion == 'S':
                self.orientacion = 'O'
            elif self.orientacion == 'O':
                self.orientacion = 'N'
            elif self.orientacion == 'N':
                self.orientacion = 'E'
            else:
                self.orientacion = 'S'
        else:
            if self.orientacion == 'S':
                self.orientacion = 'E'
            elif self.orientacion == 'E':
                self.orientacion = 'N'
            elif self.orientacion == 'N':
                self.orientacion = 'O'
            else:
                self.orientacion = 'S'

        if self.orientacion == 'S':
            self.y += 1
        elif self.orientacion == 'E':
            self.x += 1
        elif self.orientacion == 'N':
            self.y -= 1
        else:
            self.x -= 1

        self.y = self.checar_limite(self.y)
        self.x = self.checar_limite(self.x)

    def checar_limite(self, coord):
        if coord < 0:
            return self.limite - 1
        if coord == self.limite:
            return 0
        return coord


class Ventana(Frame):
    def __init__(self, parent):
        # Elemetnso de la interfaz
        Frame.__init__(self, parent)
        self.parent = parent
        self.canvas = None

        # Elementos de control
        self.cuadros = None
        self.matriz = None
        self.tam = 100
        self.tam_cuadro = 10
        self.hormigas = list()
        self.hormigas.append(Hormiga(50, 50, self.tam))
        self.pausa = True

    def init_ui(self):
        self.parent.title("Hormiga de Lagnton")
        self.pack(fill=tk.BOTH, expand=1)

        self.canvas = Canvas(self, relief='raised', width=1000, height=1000)
        self.canvas.pack(side=tk.LEFT)

        btn_iniciar = Button(self, text="Iniciar/Reiniciar", command=self.iniciar)
        btn_iniciar.pack(side=tk.TOP)

        btn_pausa = Button(self, text="Pausa/Reanudar", command=self.empezar_detener)
        btn_pausa.pack(side=tk.TOP)

    def empezar_detener(self):
        print("empezar_detener")
        self.pausa = not self.pausa
        self.animacion()

    def animacion(self):
        if not self.pausa:
            cambios = list()
            for hormiga in self.hormigas:
                if self.matriz[hormiga.y, hormiga.x] == 0:
                    self.matriz[hormiga.y, hormiga.x] = 1
                    self.canvas.itemconfig(self.cuadros[hormiga.y, hormiga.x], fill="white")
                    hormiga.mover(0)
                else:
                    self.matriz[hormiga.y, hormiga.x] = 0
                    self.canvas.itemconfig(self.cuadros[hormiga.y, hormiga.x], fill="black")
                    hormiga.mover(1)
                self.canvas.itemconfig(self.cuadros[hormiga.y, hormiga.x], fill=colores_dict[hormiga.orientacion])
            self.update_idletasks()

            self.after(1000, self.animacion)

    def pulsar_cuadrito(self, event):
        item = self.canvas.find_closest(event.x, event.y)[0]
        x, y = np.where(self.cuadros == item)

        #Checar si existe una hormiga en esa cordenada
        # Si existe, cambiar su horientacion (color)
        # Si no existe:
            # Crear la hormiga en esa posicion y agregar a la lista

        # if self.canvas.itemcget(item, "fill") == self.unos:
        #     self.canvas.itemconfig(item, fill=self.ceros)
        #     self.celulas[x[0]][y[0]] = 0
        # else:
        #     self.canvas.itemconfig(item, fill=self.unos)
        #     self.celulas[x[0]][y[0]] = 1

    def iniciar(self):
        print("iniciar")
        self.canvas.delete('all')
        self.update_idletasks()

        self.pausa = True
        self.cuadros = np.zeros(shape=(self.tam, self.tam), dtype=int)
        self.matriz = np.zeros(shape=(self.tam, self.tam), dtype=int)
        self.redibujar()
        self.canvas.itemconfig(self.cuadros[self.hormigas[0].x, self.hormigas[0].y], fill=colores_dict[self.hormigas[0].orientacion])

    def redibujar(self):
        for i in range(self.tam):
            for j in range(self.tam):
                self.cuadros[i, j] = self.canvas.create_rectangle(0 + (j * self.tam_cuadro),
                                                                        0 + (i * self.tam_cuadro),
                                                                        self.tam_cuadro + (j * self.tam_cuadro),
                                                                        self.tam_cuadro + (i * self.tam_cuadro),
                                                                        fill="black", width=0, tag="btncuadrito")

def main():
    root = Tk()
    root.geometry("1360x750+0+0")
    app = Ventana(root)
    app.init_ui()
    app.mainloop()

main()
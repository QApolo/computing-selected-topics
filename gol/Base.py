from tkinter import Tk, Canvas, Frame, Button, Entry, Label
from tkinter import BOTH, W, NW, SUNKEN, TOP, X, FLAT, LEFT, NE, E, Y, HORIZONTAL, VERTICAL, BOTTOM, RIGHT
import numpy as np
from tkcolorpicker import askcolor

class Example(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.parent = parent
        self.pausa = True
        self.tam = 50
        self.tam_cuadro = 2
        self.ceros = "white"
        self.unos = "black"
        self.regla = [2, 3, 3, 3]
        self.e1 = None
        self.contador = 0
        self.colorBtn1 = None
        self.colorBtn2 = None
        self.a = np.zeros(shape=(self.tam, self.tam), dtype=int)
        self.celulas = np.random.randint(2, size=(self.tam, self.tam), dtype=int)
        self.historia_x = list()
        self.historia_y = list()
        # Historial de unos
        archivo = open("grafica.txt", "w")
        archivo.close()
        self.canvas = None
        self.tiempo = 0
        self.initUI()
        self.update()
        self.cargar()
        # self.animacion()


    def contar_unos(self):
        for i in range(self.tam):
            for j in range(self.tam):
                if self.celulas[i, j] == 1:
                    self.contador += 1


    def re_dibujar(self):
        print("REDIBUJAR")
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
                    self.contador += 1

    def initUI(self):
        self.parent.title("Layout Test")
        self.config(bg = '#F0F0F0')
        self.pack(fill = BOTH, expand = 1)
        #create canvas
        self.canvas1 = Canvas(self, relief = 'raised', width = self.tam, height = self.tam)
        self.re_dibujar()
        self.canvas1.pack(side = LEFT)

        Label(self, text="Regla:").pack(side=TOP)
        self.e1 = Entry(self, fg="black")
        self.e1.insert(10, "2,3,3,3")
        self.e1.pack(side=TOP)
        #add quit button
        button1 = Button(self, text="Pausa/Reanudar", command=self.empezar_dentener, )
        button1.configure(width=10, activebackground="#33B5E5")
        #button1_window = canvas1.create_window(610, 10, anchor=NE, window=button1)
        button1.pack(side = TOP)

        self.colorBtn1 = Button(self, text="Selecciona el color de unos", command=self.getColorUnos, bg=self.unos)
        self.colorBtn1.pack(side = TOP)

        self.colorBtn2 = Button(self, text="Selecciona el color de ceros", command=self.getColorCeros, bg=self.ceros)
        self.colorBtn2.pack(side=TOP)


    def actualizar_color_matriz(self):
        for i in range(self.tam):
            for j in range(self.tam):
                if self.celulas[i][j] == 0:
                    self.canvas1.itemconfig(self.a[i][j], fill=self.ceros)
                else:
                    self.canvas1.itemconfig(self.a[i][j], fill=self.unos)

        self.update_idletasks()

    def getColorUnos(self):
        color = askcolor()
        if not color[1] == None:
            self.unos = color[1]
            self.colorBtn1.configure(bg=self.unos)
            self.actualizar_color_matriz()


    def getColorCeros(self):
        color = askcolor()
        if not color[1] == None:
            self.ceros = color[1]
            self.colorBtn2.configure(bg=self.ceros)
            self.actualizar_color_matriz()

    def guardar(self):
        # np.savetxt("matriz.txt", self.celulas, fmt="%d")
        archivo = open("matriz.txt", 'a')
        archivo.write("tiempo={}\n".format(self.tiempo))
        for i in range(self.tam):
            for j in range(self.tam):
                archivo.write("{} ".format(self.celulas[i, j]))
            archivo.write("\n")

        archivo.write("\n")
        archivo.close()


    def cargar(self):
        self.celulas = np.loadtxt("prueba.txt", dtype=int)
        self.canvas1.delete('all')
        self.tam = self.celulas.shape[0]
        #self.celulas = np.random.randint(2, size=(self.tam, self.tam), dtype=int)
        self.a = np.zeros(shape=(self.tam, self.tam), dtype=int)
        print(self.celulas)
        print(self.tam)
        self.canvas1.configure(width=self.tam, height=self.tam)
        # self.contar_unos()
        self.re_dibujar()
        self.update_idletasks()
        self.update()

    def reiniciar(self):
        pass

    def empezar_dentener(self):
        print("empezar_detener")
        texto = self.e1.get().split(",")
        self.regla[0] = int(texto[0])
        self.regla[1] = int(texto[1])
        self.regla[2] = int(texto[2])
        self.regla[3] = int(texto[3])

        print(texto)
        self.pausa = not self.pausa

    def animacion(self):
        print("ANIMACION")
        if not self.pausa:
            self.historia_y.append(self.contador)
            self.historia_x.append(self.tiempo)
            archivo = open("grafica.txt", "a")
            archivo.write("{},{}\n".format(self.tiempo, self.contador))
            archivo.close()
            nueva_poblacion = self.celulas.copy()
            for i in range(self.tam):
                print(i)
                for j in range(self.tam):
                    vecinos = (self.celulas[i - 1, j - 1] + self.celulas[i - 1, j] + self.celulas[i - 1, (j + 1) % self.tam]
                               + self.celulas[i, (j + 1) % self.tam] + self.celulas[(i + 1) % self.tam, (j + 1) % self.tam]
                               + self.celulas[(i + 1) % self.tam, j] + self.celulas[(i + 1) % self.tam, j - 1] + self.celulas[i, j - 1])
                    if self.celulas[i, j] == 1:
                        if vecinos < self.regla[0] or vecinos > self.regla[1]:
                            nueva_poblacion[i, j] = 0
                            self.canvas1.itemconfig(self.a[i][j], fill=self.ceros)
                            self.contador -= 1
                    else:
                        if vecinos >= self.regla[2] and vecinos <= self.regla[3]:
                            nueva_poblacion[i, j] = 1
                            self.canvas1.itemconfig(self.a[i][j], fill=self.unos)
                            self.contador += 1

            self.celulas[:] = nueva_poblacion[:]
            self.update_idletasks()
            print("Termino")
            self.tiempo += 1
        self.after(1000, self.animacion)

def main():
    root = Tk()
    root.geometry('1000x600+0+0')
    app = Example(root)
    app.mainloop()

main()
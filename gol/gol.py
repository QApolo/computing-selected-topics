from tkinter import Tk, Canvas, Frame, Button, Entry, Label, Scale, filedialog
from tkinter import BOTH, TOP, LEFT, HORIZONTAL
import numpy as np
from tkcolorpicker import askcolor
import datetime
import time


class Ventana(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.parent = parent
        # Elementos interfaz
        self.ceros = "white"
        self.unos = "black"
        self.regla = [2, 3, 3, 3]
        self.e1 = None
        self.e2 = None
        self.contador = 0
        self.colorBtn1 = None
        self.colorBtn2 = None
        self.barra = None
        self.canvas = None
        # variables del juego de la vida
        self.pausa = True
        self.tam = 100
        self.tam_cuadro = 10
        self.distribucion = .5
        self.cuadritos = np.zeros(shape=(self.tam, self.tam), dtype=int)
        self.celulas = np.random.randint(2, size=(self.tam, self.tam), dtype=int)
        self.tiempo = 0
        # Historial de unos
        self.nom_archivo = None

    def iniciar(self):
        self.nom_archivo = "{}.csv".format(self.obtener_hora())
        archivo = open(self.nom_archivo, "w")
        archivo.close()
        self.canvas.delete('all')
        self.update_idletasks()
        self.pausa = True
        self.contador = 0
        self.tiempo = 0
        self.tam = int(self.e2.get())
        self.tam_cuadro = 0
        while self.tam_cuadro*self.tam < 1000:
            self.tam_cuadro += 1
        if self.tam_cuadro*self.tam > 1000:
            self.tam_cuadro -= 1
        self.distribucion = self.barra.get()/100
        self.celulas = np.random.choice([1, 0], size=(self.tam, self.tam), p=[self.distribucion, 1-self.distribucion])
        self.cuadritos = np.zeros(shape=(self.tam, self.tam), dtype=int)
        texto = self.e1.get().split(",")
        self.regla[0] = int(texto[0])
        self.regla[1] = int(texto[1])
        self.regla[2] = int(texto[2])
        self.regla[3] = int(texto[3])
        self.contar_unos()
        print(self.contador)
        self.re_dibujar()

    def contar_unos(self):
        for i in range(self.tam):
            for j in range(self.tam):
                if self.celulas[i, j] == 1:
                    self.contador += 1

        print("contador_unos : {}".format(self.contador))

    def pulsar_cuadrito(self, event):
        item = self.canvas.find_closest(event.x, event.y)[0]
        x, y = np.where(self.cuadritos == item)
        if self.canvas.itemcget(item, "fill") == self.unos:
            self.canvas.itemconfig(item, fill=self.ceros)
            self.celulas[x[0]][y[0]] = 0
            self.contador -= 1
        else:
            self.canvas.itemconfig(item, fill=self.unos)
            self.celulas[x[0]][y[0]] = 1
            self.contador += 1

    def re_dibujar(self):
        print("REDIBUJAR")
        for i in range(self.tam):
            for j in range(self.tam):
                if self.celulas[i, j] == 0:
                    self.cuadritos[i, j] = self.canvas.create_rectangle(0 + (j * self.tam_cuadro),
                                                                        0 + (i * self.tam_cuadro),
                                                                        self.tam_cuadro + (j * self.tam_cuadro),
                                                                        self.tam_cuadro + (i * self.tam_cuadro),
                                                                        fill=self.ceros, width=0, tag="btncuadrito")
                else:
                    self.cuadritos[i, j] = self.canvas.create_rectangle(0 + (j * self.tam_cuadro),
                                                                        0 + (i * self.tam_cuadro),
                                                                        self.tam_cuadro + (j * self.tam_cuadro),
                                                                        self.tam_cuadro + (i * self.tam_cuadro),
                                                                        fill=self.unos, width=0, tag="btncuadrito")

        self.canvas.tag_bind("btncuadrito", "<Button-1>", self.pulsar_cuadrito)
        self.update_idletasks()

    def init_ui(self):
        self.parent.title("Juego de la vida")
        self.pack(fill=BOTH, expand=1)

        self.canvas = Canvas(self, relief='raised', width=1000, height=1000)
        self.canvas.pack(side=LEFT)

        Label(self, text="Regla:").pack(side=TOP)
        self.e1 = Entry(self, fg="black", bg="white")
        self.e1.insert(10, "2,3,3,3")
        self.e1.pack(side=TOP)

        Label(self, text="Tamaño:").pack(side=TOP)
        self.e2 = Entry(self, fg="black", bg="white")
        self.e2.insert(10, "100")
        self.e2.pack(side=TOP)

        Label(self, text="Porcentaje de unos").pack(side=TOP)
        self.barra = Scale(self, from_=0, to=100, orient=HORIZONTAL, tickinterval=50)
        self.barra.set(50)
        self.barra.pack(side=TOP)

        btn_iniciar = Button(self, text="Iniciar/Reiniciar", command=self.iniciar)
        btn_iniciar.pack(side=TOP)

        button1 = Button(self, text="Pausa/Reanudar", command=self.empezar_dentener)
        button1.pack(side=TOP)

        self.colorBtn1 = Button(self, text="Selecciona el color de unos", command=self.get_color_unos, bg=self.unos)
        self.colorBtn1.pack(side=TOP)

        self.colorBtn2 = Button(self, text="Selecciona el color de ceros", command=self.get_color_ceros, bg=self.ceros)
        self.colorBtn2.pack(side=TOP)

        btn_save = Button(self, text="Guardar", command=self.guardar)
        btn_save.pack(side=TOP)
        btn_cargar = Button(self, text="Cargar Matriz", command=self.cargar)
        btn_cargar.pack(side=TOP)

    def abrir_archivo(self):
        print("abrir archivo")
        ga = filedialog.askopenfilename(title="Selecciona un archivo",
                                        filetypes=(("CSV", "*.csv"), ("Archivo de texto", "*.txt"),
                                                   ("Todos los archivos", "*.*")))
        return ga

    def actualizar_color_matriz(self):
        for i in range(self.tam):
            for j in range(self.tam):
                if self.celulas[i][j] == 0:
                    self.canvas.itemconfig(self.cuadritos[i][j], fill=self.ceros)
                else:
                    self.canvas.itemconfig(self.cuadritos[i][j], fill=self.unos)

        self.update_idletasks()

    def get_color_unos(self):
        color = askcolor()
        if not color[1] is None:
            self.unos = color[1]
            self.colorBtn1.configure(bg=self.unos)
            self.actualizar_color_matriz()

    def get_color_ceros(self):
        color = askcolor()
        if not color[1] is None:
            self.ceros = color[1]
            self.colorBtn2.configure(bg=self.ceros)
            self.actualizar_color_matriz()

    def guardar(self):
        temp_nom = "respaldo-{}.csv".format(self.obtener_hora())
        archivo = open(temp_nom, 'a')
        for i in range(self.tam):
            for j in range(self.tam):
                archivo.write("{} ".format(self.celulas[i, j]))
            archivo.write("\n")

        archivo.write("\n")
        archivo.close()

    def cargar(self):
        print("Cargar archivo")
        temp_archivo = self.abrir_archivo()
        self.celulas = np.loadtxt(temp_archivo, dtype=int)
        self.canvas.delete('all')
        self.nom_archivo = "{}.csv".format(self.obtener_hora())
        archivo = open(self.nom_archivo, "w")
        archivo.close()
        texto = self.e1.get().split(",")
        self.regla[0] = int(texto[0])
        self.regla[1] = int(texto[1])
        self.regla[2] = int(texto[2])
        self.regla[3] = int(texto[3])
        self.tam = self.celulas.shape[0]
        self.cuadritos = np.zeros(shape=(self.tam, self.tam), dtype=int)
        self.tam_cuadro = 0
        self.contador = 0
        while self.tam_cuadro * self.tam < 1000:
            self.tam_cuadro += 1
        if self.tam_cuadro * self.tam > 1000:
            self.tam_cuadro -= 1
        self.contar_unos()
        self.re_dibujar()

    def empezar_dentener(self):
        print("empezar_detener")
        self.pausa = not self.pausa
        self.animacion()

    def animacion(self):
        if not self.pausa:
            archivo = open(self.nom_archivo, "a")
            archivo.write("{},{}\n".format(self.tiempo, self.contador))
            archivo.close()
            nueva_poblacion = self.celulas.copy()
            for i in range(self.tam):
                for j in range(self.tam):
                    vecinos = self.revisar_vecinos(i, j)
                    if self.celulas[i, j] == 1:
                        if vecinos < self.regla[0] or vecinos > self.regla[1]:
                            nueva_poblacion[i, j] = 0
                            self.canvas.itemconfig(self.cuadritos[i][j], fill=self.ceros)
                            self.contador -= 1
                    else:
                        if self.regla[2] <= vecinos <= self.regla[3]:
                            nueva_poblacion[i, j] = 1
                            self.canvas.itemconfig(self.cuadritos[i][j], fill=self.unos)
                            self.contador += 1

            self.celulas[:] = nueva_poblacion[:]
            self.update_idletasks()
            print("Termino el t={}".format(self.tiempo))
            self.tiempo += 1
            self.after(50, self.animacion)

    def revisar_vecinos(self, i, j):
        vecinos = self.celulas[i - 1, j - 1]
        vecinos += self.celulas[i - 1, j]
        vecinos += self.celulas[i - 1, (j + 1) % self.tam]
        vecinos += self.celulas[i, (j + 1) % self.tam]
        vecinos += self.celulas[(i + 1) % self.tam, (j + 1) % self.tam]
        vecinos += self.celulas[(i + 1) % self.tam, j]
        vecinos += self.celulas[(i + 1) % self.tam, j - 1]
        vecinos += self.celulas[i, j - 1]
        return vecinos

    @staticmethod
    def obtener_hora():
        return datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d_%H:%M:%S')


# 2 2 7 7
def main():
    root = Tk()
    root.geometry('1360x750+0+0')
    app = Ventana(root)
    app.init_ui()
    app.mainloop()


main()

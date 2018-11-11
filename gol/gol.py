from tkinter import Tk, Canvas, Frame, Button, Entry, Label, Scale, filedialog
from tkinter import BOTH, TOP, LEFT, HORIZONTAL, Y, RIGHT, VERTICAL, PhotoImage
from tkinter import Scrollbar
import numpy as np
from tkcolorpicker import askcolor
import datetime
import time


dict_tipos = {
    "nada": 0,
    "cubo": 1,
    "glider": 2,
    "glider2": 3,
    "glider3": 4,
    "oscilador": 5,
}


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
        self.cubo_image = None
        self.glider = None
        self.glider2 = None
        self.glider3 = None
        self.oscilador = None
        # variables del juego de la vida
        self.pausa = True
        self.tam = 100
        self.tam_cuadro = 10
        self.distribucion = .5
        self.cuadritos = np.zeros(shape=(self.tam, self.tam), dtype=int)
        self.celulas = np.random.randint(2, size=(self.tam, self.tam), dtype=int)
        self.tiempo = 0
        self.tipo_insertar = dict_tipos["nada"]
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
        self.celulas = np.random.choice([1, 0], size=(self.tam, self.tam), 
                                        p=[self.distribucion, 1-self.distribucion])
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
        i, j = np.where(self.cuadritos == item)
        print("{}, {}".format(i[0], j[0]))
        if self.tipo_insertar == dict_tipos["nada"]:
            if self.canvas.itemcget(item, "fill") == self.unos:
                self.canvas.itemconfig(item, fill=self.ceros)
                self.celulas[i[0]][j[0]] = 0
                self.contador -= 1
            else:
                self.canvas.itemconfig(item, fill=self.unos)
                self.celulas[i[0]][j[0]] = 1
                self.contador += 1
        elif self.tipo_insertar == dict_tipos["cubo"]:
            print("cubo")
            self.insertar_cubo(i[0], j[0])
        elif self.tipo_insertar == dict_tipos["glider"]:
            print("glider")
            self.insertar_glider(i[0], j[0])
        elif self.tipo_insertar == dict_tipos["glider2"]:
            print("glider2")
            self.insertar_glider_dos(i[0], j[0])
        elif self.tipo_insertar == dict_tipos["glider3"]:
            print("glider3")
            self.insertar_glider_tres(i[0], j[0])
        elif self.tipo_insertar == dict_tipos["oscilador"]:
            print("oscilador")
            self.insertar_oscilador(i[0], j[0])

        self.tipo_insertar = dict_tipos["nada"]

    def insertar_cubo(self, x1, y1):
        x2 = x1 + 1
        y2 = y1 + 1
        item1 = self.cuadritos[x1, y1]
        item2 = self.cuadritos[x1, y2]
        item3 = self.cuadritos[x2, y1]
        item4 = self.cuadritos[x2, y2]

        if self.celulas[x1, y1] == 0:
            self.celulas[x1, y1] = 1
            self.contador += 1
            self.canvas.itemconfig(item1, fill=self.unos)
        if self.celulas[x1, y2] == 0:
            self.celulas[x1, y2] = 1
            self.contador += 1
            self.canvas.itemconfig(item2, fill=self.unos)
        if self.celulas[x2, y1] == 0:
            self.celulas[x2, y1] = 1
            self.contador += 1
            self.canvas.itemconfig(item3, fill=self.unos)
        if self.celulas[x2, y2] == 0:
            self.celulas[x2, y2] = 1
            self.contador += 1
            self.canvas.itemconfig(item4, fill=self.unos)

    def insertar_oscilador(self, i1, j1):
        i0 = i1 - 1
        i2 = i1 + 1
        item0 = self.cuadritos[i0, j1]
        item1 = self.cuadritos[i1, j1]
        item2 = self.cuadritos[i2, j1]

        if self.celulas[i0, j1] == 0:
            self.celulas[i0, j1] = 1
            self.contador += 1
            self.canvas.itemconfig(item0, fill=self.unos)

        if self.celulas[i1, j1] == 0:
            self.celulas[i1, j1] = 1
            self.contador += 1
            self.canvas.itemconfig(item1, fill=self.unos)

        if self.celulas[i2, j1] == 0:
            self.celulas[i2, j1] = 1
            self.contador += 1
            self.canvas.itemconfig(item2, fill=self.unos)

    def insertar_glider(self, i1, j1):
        j2 = j1 + 1
        i2 = i1 + 1
        i3 = i2 + 1
        i4 = i3 + 1

        item1 = self.cuadritos[i1, j1]
        item2 = self.cuadritos[i1, j2]
        item3 = self.cuadritos[i2, j1]
        item4 = self.cuadritos[i2, j2]
        item5 = self.cuadritos[i3, j1]
        item6 = self.cuadritos[i3, j2]
        item7 = self.cuadritos[i4, j1]
        item8 = self.cuadritos[i4, j2]

        if self.celulas[i1, j1] == 0:
            self.celulas[i1, j1] = 1
            self.contador += 1
            self.canvas.itemconfig(item1, fill=self.unos)
        if self.celulas[i1, j2] == 1:
            self.celulas[i1, j2] = 0
            self.contador -= 1
            self.canvas.itemconfig(item2, fill=self.ceros)

        if self.celulas[i2, j1] == 1:
            self.celulas[i2, j1] = 0
            self.contador -= 1
            self.canvas.itemconfig(item3, fill=self.ceros)
        if self.celulas[i2, j2] == 0:
            self.celulas[i2, j2] = 1
            self.contador += 1
            self.canvas.itemconfig(item4, fill=self.unos)

        if self.celulas[i3, j1] == 1:
            self.celulas[i3, j1] = 0
            self.contador -= 1
            self.canvas.itemconfig(item5, fill=self.ceros)
        if self.celulas[i3, j2] == 0:
            self.celulas[i3, j2] = 1
            self.contador += 1
            self.canvas.itemconfig(item6, fill=self.unos)

        if self.celulas[i4, j1] == 0:
            self.celulas[i4, j1] = 1
            self.contador += 1
            self.canvas.itemconfig(item7, fill=self.unos)
        if self.celulas[i1, j2] == 1:
            self.celulas[i1, j2] = 0
            self.contador -= 1
            self.canvas.itemconfig(item8, fill=self.ceros)

    def insertar_glider_dos(self, i1, j1):
        i2 = i1 + 1
        i3 = i2 + 1
        i4 = i3 + 1
        j2 = j1 + 1
        j3 = j2 + 1

        item1 = self.cuadritos[i1, j1]
        item2 = self.cuadritos[i1, j2]
        item3 = self.cuadritos[i1, j3]
        item4 = self.cuadritos[i2, j1]
        item5 = self.cuadritos[i2, j2]
        item6 = self.cuadritos[i2, j3]
        item7 = self.cuadritos[i3, j1]
        item8 = self.cuadritos[i3, j2]
        item9 = self.cuadritos[i3, j3]
        item10 = self.cuadritos[i4, j1]
        item11 = self.cuadritos[i4, j2]
        item12 = self.cuadritos[i4, j3]

        if self.celulas[i1, j1] == 0:
            self.celulas[i1, j1] = 1
            self.contador += 1
            self.canvas.itemconfig(item1, fill=self.unos)
        if self.celulas[i1, j2] == 1:
            self.celulas[i1, j2] = 0
            self.contador -= 1
            self.canvas.itemconfig(item2, fill=self.ceros)
        if self.celulas[i1, j3] == 1:
            self.celulas[i1, j2] = 0
            self.contador -= 1
            self.canvas.itemconfig(item3, fill=self.ceros)

        if self.celulas[i2, j1] == 1:
            self.celulas[i2, j1] = 0
            self.contador -= 1
            self.canvas.itemconfig(item4, fill=self.ceros)
        if self.celulas[i2, j2] == 1:
            self.celulas[i2, j2] = 0
            self.contador -= 1
            self.canvas.itemconfig(item5, fill=self.ceros)
        if self.celulas[i2, j3] == 0:
            self.celulas[i2, j3] = 1
            self.contador += 1
            self.canvas.itemconfig(item6, fill=self.unos)

        if self.celulas[i3, j1] == 1:
            self.celulas[i3, j1] = 0
            self.contador -= 1
            self.canvas.itemconfig(item7, fill=self.ceros)
        if self.celulas[i3, j2] == 1:
            self.celulas[i3, j2] = 0
            self.contador -= 1
            self.canvas.itemconfig(item8, fill=self.ceros)
        if self.celulas[i3, j3] == 0:
            self.celulas[i3, j3] = 1
            self.contador += 1
            self.canvas.itemconfig(item9, fill=self.unos)

        if self.celulas[i4, j1] == 0:
            self.celulas[i4, j1] = 1
            self.contador += 1
            self.canvas.itemconfig(item10, fill=self.unos)
        if self.celulas[i4, j2] == 1:
            self.celulas[i4, j2] = 0
            self.contador -= 1
            self.canvas.itemconfig(item11, fill=self.ceros)
        if self.celulas[i4, j3] == 1:
            self.celulas[i4, j3] = 0
            self.contador -= 1
            self.canvas.itemconfig(item12, fill=self.ceros)

    def insertar_glider_tres(self, i2, j2):
        i1 = i2 - 1
        i3 = i2 + 1
        j1 = j2 - 1
        j3 = j2 + 1

        item1 = self.cuadritos[i1, j1]
        item2 = self.cuadritos[i1, j2]
        item3 = self.cuadritos[i1, j3]
        item4 = self.cuadritos[i2, j1]
        item5 = self.cuadritos[i2, j2]
        item6 = self.cuadritos[i2, j3]
        item7 = self.cuadritos[i3, j1]
        item8 = self.cuadritos[i3, j2]
        item9 = self.cuadritos[i3, j3]

        if self.celulas[i1, j1] == 1:
            self.celulas[i1, j1] = 0
            self.contador -= 1
            self.canvas.itemconfig(item1, fill=self.ceros)
        if self.celulas[i1, j2] == 0:
            self.celulas[i1, j2] = 1
            self.contador += 1
            self.canvas.itemconfig(item2, fill=self.unos)
        if self.celulas[i1, j3] == 1:
            self.celulas[i1, j2] = 0
            self.contador -= 1
            self.canvas.itemconfig(item3, fill=self.ceros)

        if self.celulas[i2, j1] == 1:
            self.celulas[i2, j1] = 0
            self.contador -= 1
            self.canvas.itemconfig(item4, fill=self.ceros)
        if self.celulas[i2, j2] == 1:
            self.celulas[i2, j2] = 0
            self.contador -= 1
            self.canvas.itemconfig(item5, fill=self.ceros)
        if self.celulas[i2, j3] == 0:
            self.celulas[i2, j3] = 1
            self.contador += 1
            self.canvas.itemconfig(item6, fill=self.unos)

        if self.celulas[i3, j1] == 0:
            self.celulas[i3, j1] = 1
            self.contador += 1
            self.canvas.itemconfig(item7, fill=self.unos)
        if self.celulas[i3, j2] == 0:
            self.celulas[i3, j2] = 1
            self.contador += 1
            self.canvas.itemconfig(item8, fill=self.unos)
        if self.celulas[i3, j3] == 0:
            self.celulas[i3, j3] = 1
            self.contador += 1
            self.canvas.itemconfig(item9, fill=self.unos)

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
        scroll = Scrollbar(self, orient=VERTICAL)
        scroll.pack(side=RIGHT, fill=Y)
        scroll.config(command=self.canvas.yview)

        self.canvas.config(yscrollcommand=scroll.set)
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
        self.barra = Scale(self, from_=0, to=100, orient=HORIZONTAL, tickinterval=50, length=200)
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

        self.cubo_image = PhotoImage(file="./data/cuadrado.png")
        btn_cubo = Button(self, image=self.cubo_image, command=self.seleccionar_cubo)
        btn_cubo.pack(side=TOP)

        self.glider = PhotoImage(file="./data/glider.png")
        self.glider = self.glider.subsample(2)
        btn_glider = Button(self, image=self.glider, command=self.seleccionar_glider)
        btn_glider.pack(side=TOP)

        self.glider2 = PhotoImage(file="./data/glider2.png")
        self.glider2 = self.glider2.subsample(2)
        btn_glider2 = Button(self, image=self.glider2, command=self.seleccionar_glider_dos)
        btn_glider2.pack(side=TOP)

        self.glider3 = PhotoImage(file="./data/glider3.png")
        btn_glider3 = Button(self, image=self.glider3, command=self.seleccionar_glider_tres)
        btn_glider3.pack(side=TOP)

        self.oscilador = PhotoImage(file="./data/oscilador.png")
        btn_osilador = Button(self, image=self.oscilador, command=self.seleccionar_oscilador)
        btn_osilador.pack(side=TOP)

    def seleccionar_glider(self):
        self.tipo_insertar = dict_tipos["glider"]

    def seleccionar_glider_dos(self):
        self.tipo_insertar = dict_tipos["glider2"]

    def seleccionar_glider_tres(self):
        self.tipo_insertar = dict_tipos["glider3"]

    def seleccionar_oscilador(self):
        self.tipo_insertar = dict_tipos["oscilador"]

    def seleccionar_cubo(self):
        self.tipo_insertar = dict_tipos["cubo"]

    @staticmethod
    def abrir_archivo():
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
            #print("Termino el t={}".format(self.tiempo))
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


def main():
    root = Tk()
    root.geometry('1360x750+0+0')
    app = Ventana(root)
    app.init_ui()
    app.mainloop()


main()

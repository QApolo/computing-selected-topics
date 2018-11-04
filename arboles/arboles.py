import numpy as np
import sys
import webbrowser

dict_tipos = {
    "life": 1,
    "diffusion": 2,
}


class Arboles:
    def __init__(self, _tam=2, _tipo=dict_tipos["life"]):
        self.tam = tam
        self.tipo = tipo
        self.vida = [2, 3, 3, 3]
        self.diffusion = [7, 7, 2, 2]
        self.regla = self.diffusion
        self.longitud = self.tam * self.tam
        self.max = 2 ** self.longitud
        self.formato = "{{:0{}b}}".format(self.longitud)
        if self.tipo == dict_tipos["life"]:
            self.regla = self.vida

    def obtener_siguiente(self, m):
        nueva_matriz = m.copy()
        for i in range(self.tam):
            for j in range(self.tam):
                suma = self.revisar_vecinos(i, j, m)
                if m[i, j] == 1:
                    if suma < self.regla[0] or suma > self.regla[1]:
                        nueva_matriz[i, j] = 0
                else:
                    if self.regla[2] <= suma <= self.regla[3]:
                        nueva_matriz[i, j] = 1
        return nueva_matriz

    def revisar_vecinos(self, i, j, m):
        vecinos = m[i - 1, j - 1]
        vecinos += m[i - 1, j]
        vecinos += m[i - 1, (j + 1) % self.tam]
        vecinos += m[i, (j + 1) % self.tam]
        vecinos += m[(i + 1) % self.tam, (j + 1) % self.tam]
        vecinos += m[(i + 1) % self.tam, j]
        vecinos += m[(i + 1) % self.tam, j - 1]
        vecinos += m[i, j - 1]
        return vecinos

    def numero_cadena(self, numero):
        return self.formato.format(numero)

    @staticmethod
    def cadena_numero(cadena):
        return int(cadena, 2)

    def cadena_matriz(self, cadena):
        m = np.zeros(shape=(self.tam, self.tam), dtype=int)
        k = 0
        for i in range(self.tam):
            for j in range(self.tam):
                if cadena[k] == '1':
                    m[i, j] = 1
                k += 1
        return m

    def matriz_cadena(self, matriz):
        cadena = ["0"] * self.longitud
        k = 0
        for i in range(self.tam):
            for j in range(self.tam):
                if matriz[i, j] == 1:
                    cadena[k] = "1"
                k += 1
        return "".join(cadena)

    def generar(self):
        temp_nom = "diffusion"
        if self.tipo == dict_tipos["life"]:
            temp_nom = "life"
        nombre_archivo = "tam-{}-{}".format(self.tam, temp_nom)
        archivo = open("{}.wls".format(nombre_archivo), "w")

        archivo.write("Graph[{")
        for i in range(self.max):
            cadena = self.numero_cadena(i)
            m = self.cadena_matriz(cadena)
            m_sig = self.obtener_siguiente(m)
            cadena_sig = self.matriz_cadena(m_sig)
            if i == self.max-1:
                archivo.write('"{}" -> "{}"'.format(cadena, cadena_sig))
            else:
                archivo.write('"{}" -> "{}", '.format(cadena, cadena_sig))
        if self.tam == 2:
            archivo.write('}, VertexLabels->Automatic, GraphLayout -> "RadialEmbedding"]')
        else:
            archivo.write('}, GraphLayout -> "RadialEmbedding"]')
        archivo.close()
        ejecutable = open("ejecutable-{}-{}.bat".format(self.tam, temp_nom), "w")
        ejecutable.write("set MATHE_PATH=C:\\Program Files\\Wolfram Research\\Mathematica\\11.3\n")
        ejecutable.write("set PROJECT_PATH=C:\\Users\\reymy\\Documents\\septimo\\computing-selected-topics\\arboles\n")
        ejecutable.write('"%MATHE_PATH%\\wolframscript.exe" -cloud -print -format PNG -file ')
        ejecutable.write('"%PROJECT_PATH%\\{}.wls" > {}.png'.format(nombre_archivo, nombre_archivo))
        ejecutable.close()


tam = int(sys.argv[1])
tipo = int(sys.argv[2])

life2 = Arboles(tam, tipo)
life2.generar()
webbrowser.open("file:///C:/Users/reymy/Documents/septimo/computing-selected-topics/arboles/index.html")

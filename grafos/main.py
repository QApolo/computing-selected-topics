# libraries
import pandas as pd
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

# #Build a dataframe with 4 connections
# #df = pd.DataFrame({'from': ['A', 'B', 'C', 'A'], 'to': ['D', 'A', 'E', 'C']})
# #x|df
#
# # Build your graph
# G = nx.Graph()
# G.add_edges_from([(1, 2), (1, 3)])
# G2 = nx.Graph()
# G2.add_edges_from([(1, 2), (2, 3)])
# # Plot it
# plt.subplot(221)
# nx.draw(G, with_labels=True, arrows=True)
# plt.subplot(222)
# nx.draw(G2, with_labels=True, arrows=True)
# plt.show()

# lista de todos los grafos
# lista de la relacion de todos los grafos
# una lista por cada grafo

# matriz 1
# buscar si ya existe la matriz
# si ya existe la matriz pasar a la siguiente
# si no existe
#     agregar
#     aplicar regla y generar matriz 2
#     buscar matriz 2 en la lista
#     si ya existe, pasar a la siguiente matriz
#         crear la relacion matriz 1 > matriz 2
#         regresamos al paso uno
#     si no existe
#         agregar a la lista de grafos
#         crear la relacion matriz 1 > matriz 2
#         ahora la matriz 2 es la uno y repetir paso 1
# La funcion hash recorrera la matriz y creara una cadena de longitud N*N
# donde N es el un lado de la matriz

class Grafos:
    def __init__(self):
        self.tam = 4
        self.total = self.tam * self.tam
        self.origen = dict()
        self.regla = [2, 3, 3, 3]
        self.cadena_inicial = "0" * (self.total)
        self.cadena_actual = self.cadena_inicial
        self.matriz_actual = np.zeros(shape=(self.tam, self.tam), dtype=int)
        self.tabla = dict()

    def mi_hash(self, m):
        cadena = ["0"] * (self.total)
        k = 0
        for i in range(self.tam):
            for j in range(self.tam):
                if m[i, j] == 1:
                    cadena[k] = "1"
                k += 1
        return "".join(cadena)
        #m.flags.writeable=False
        #return hash(m.tostring())

    def reverse_hash(self, cadena):
        m = np.zeros(shape=(self.tam, self.tam), dtype=int)
        k = 0
        for i in range(self.tam):
            for j in range(self.tam):
                if cadena[k] == '1':
                    m[i, j] = 1
                k += 1
        return m

    def obtener_siguiente(self, m):
        nueva_matriz = m.copy()
        for i in range(self.tam):
            for j in range(self.tam):
                suma = (m[i - 1, j - 1] + m[i - 1, j] + m[i - 1, (j + 1) % self.tam] + m[i, (j + 1) % self.tam]
                           + m[(i + 1) % self.tam, (j + 1) % self.tam] + m[(i + 1) % self.tam, j]
                           + m[(i + 1) % self.tam, j - 1] + m[i, j - 1])
                if m[i, j] == 1:
                    if suma < self.regla[0] or suma > self.regla[1]:
                        nueva_matriz[i, j] = 0
                else:
                    if suma >= self.regla[2] and suma <= self.regla[3]:
                        nueva_matriz[i, j] = 1
        return nueva_matriz

    def siguiente_cadena(self, cadena):
        """Esta es la unica funcion
        que considero que puedo mejorar"""
        lista = list(cadena)
        i = self.total - 1
        while i > -1:
            if lista[i] == '0':
                lista[i] = '1'
                break
            else:
                lista[i] = '0'
            i -= 1
        return "".join(lista)

    def generar(self):
        m = self.matriz_actual
        continuar = True
        while continuar:
            actual = self.mi_hash(m)
            resultado = self.tabla.get(actual)
            if resultado is None:
                self.tabla.update({actual:"-1"})
            elif resultado == "-1":
                siguiente = self.obtener_siguiente(m)
                sig_resultado = self.mi_hash(siguiente)
                self.tabla.update({actual:sig_resultado})
                m = siguiente
            else:
                cadena_sig = self.siguiente_cadena(self.cadena_actual)
                if cadena_sig == self.cadena_inicial:
                    break
                else:
                    self.cadena_actual = cadena_sig
                    m = self.reverse_hash(cadena_sig)
        print("termino")

grafos = Grafos()
grafos.generar()

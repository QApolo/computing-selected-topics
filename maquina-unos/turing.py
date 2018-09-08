class MaquinaTuring:
    """MaquinaTuring"""
    def __init__(self, estado_inicial, estados_finales, cadena, transiciones):
        self.transiciones = transiciones
        self.inicial = estado_inicial
        self.finales = estados_finales
        self.cinta = list(cadena)
        self.estado_actual = self.inicial
        self.apuntador = 0
        self.blanco = "B"

    def consumir(self):
        if len(self.cinta) - 1 < self.apuntador:
            caracter = 'B'
        else:
            caracter = self.cinta[self.apuntador]
        tupla = (self.estado_actual, caracter)
        if tupla in self.transiciones:
            siguiente = self.transiciones[tupla]
            if len(self.cinta) - 1< self.apuntador:
                self.cinta.append(self.blanco)
            if self.apuntador < 0:
                self.cinta.insert(0, self.blanco)
            self.cinta[self.apuntador] = siguiente[1]
            if siguiente[2] == "R":
                self.apuntador += 1
            else:
                self.apuntador -= 1

            self.estado_actual = siguiente[0]

    def es_final(self):
        if self.estado_actual in self.finales:
            if len(self.cinta) - 1 < self.apuntador or self.apuntador < 0:
                return True
        return False

transiciones = {
            ("q0", "1"): ("q1", "X", "R"),
            ("q0", "Y"): ("q3", "1", "R"),
            ("q1", "1"): ("q1", "1", "R"),
            ("q1", "Y"): ("q1", "Y", "R"),
            ("q1", "B"): ("q2", "Y", "L"),
            ("q2", "1"): ("q2", "1", "L"),
            ("q2", "X"): ("q0", "1", "R"),
            ("q2", "Y"): ("q2", "Y", "L"),
            ("q3", "Y"): ("q3", "1", "R")
            }

maquina = MaquinaTuring("q0", "q3", "11111", transiciones)
while not maquina.es_final():
    print('Cadena:{}'.format(''.join(maquina.cinta)))
    print('Estado: {}, apuntador: {}'.format(maquina.estado_actual, maquina.apuntador+1))
    maquina.consumir()
    print('Siguiente estado: {}'.format(maquina.estado_actual))
    print('*'*20)
print('Cadena:{}'.format(''.join(maquina.cinta)))
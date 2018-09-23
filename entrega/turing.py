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
        self.direccion = None

    def consumir(self):
        """Toma un simbolo de la cinta y lo evalua en la funcion de
        transicion"""
        if len(self.cinta) - 1 < self.apuntador:
            caracter = 'B'
        else:
            caracter = self.cinta[self.apuntador]
        tupla = (self.estado_actual, caracter)
        if tupla in self.transiciones:
            siguiente = self.transiciones[tupla]
            if len(self.cinta) - 1 < self.apuntador:
                self.cinta.append(self.blanco)
            if self.apuntador < 0:
                self.cinta.insert(0, self.blanco)
            self.cinta[self.apuntador] = siguiente[1]
            if siguiente[2] == "R":
                self.apuntador += 1
            else:
                self.apuntador -= 1

            self.estado_actual = siguiente[0]
            self.direccion = siguiente[2]
            return True
        else:
            return False

    def es_final(self):
        """Metodo para comprobar si nos encontramos en un estado final"""
        if self.estado_actual in self.finales:
            if len(self.cinta) - 1 < self.apuntador or self.apuntador < 0:
                return True
        return False

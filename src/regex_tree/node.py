"""
Definición de la clase Nodo, usada para construir el árbol sintáctico
de la expresión regular en notación postfija.
"""

class Nodo:
    def __init__(self, valor, izquierda=None, derecha=None):
        self.valor = valor
        self.izquierda = izquierda
        self.derecha = derecha
        self.id = id(self)  # identificador único para dibujar

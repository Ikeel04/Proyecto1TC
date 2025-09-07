"""
Módulo parser: construcción y visualización del árbol sintáctico
a partir de una expresión regular en notación postfija.
"""

import os
from graphviz import Digraph
from .node import Nodo

# Carpeta donde se guardarán las imágenes
RESULTS_DIR = os.path.join(os.path.dirname(__file__), "..", "results")
os.makedirs(RESULTS_DIR, exist_ok=True)


def construir_arbol(postfix: list[str]) -> Nodo:
    """
    Construye un árbol sintáctico a partir de la expresión en postfijo.
    Devuelve el nodo raíz.
    """
    pila = []
    for token in postfix:
        if token in {'*', '+', '?'}:  # operadores unarios
            if not pila:
                raise ValueError(f"Falta operando para '{token}'")
            nodo = Nodo(token, izquierda=pila.pop())
            pila.append(nodo)
        elif token in {'.', '|'}:  # operadores binarios
            if len(pila) < 2:
                raise ValueError(f"Faltan operandos para '{token}'")
            der = pila.pop()
            izq = pila.pop()
            nodo = Nodo(token, izquierda=izq, derecha=der)
            pila.append(nodo)
        else:  # operando (símbolo del alfabeto o ε)
            pila.append(Nodo(token))
    if len(pila) != 1:
        raise ValueError("Expresión postfija mal balanceada")
    return pila[-1]


def dibujar_arbol(raiz: Nodo, filename: str):
    """
    Dibuja el árbol sintáctico usando Graphviz y lo exporta como PNG
    en la carpeta src/results.
    """
    dot = Digraph()

    def agregar_nodos(nodo: Nodo):
        if nodo is None:
            return
        dot.node(str(nodo.id), nodo.valor)
        if nodo.izquierda:
            dot.edge(str(nodo.id), str(nodo.izquierda.id))
            agregar_nodos(nodo.izquierda)
        if nodo.derecha:
            dot.edge(str(nodo.id), str(nodo.derecha.id))
            agregar_nodos(nodo.derecha)

    agregar_nodos(raiz)

    output_path = os.path.join(RESULTS_DIR, filename)
    dot.render(output_path, format='png', cleanup=True)

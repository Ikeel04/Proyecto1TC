"""
Módulo shunting_yard: convierte expresiones regulares de notación infix
a notación postfix (RPN) usando el algoritmo de Shunting Yard.
"""

from typing import List

def shunting_yard(tokens: List[str]) -> List[str]:
    """
    Convierte una lista de tokens en notación infix a notación postfix (RPN).
    Tokens válidos:
      - literales (if, else, \{, \}, ε, etc.)
      - operadores (*, +, ?, ., |)
      - paréntesis ( )
    """
    salida, pila = [], []
    precedencia = {'*': 3, '+': 3, '?': 3, '.': 2, '|': 1}
    operadores = set(precedencia.keys())

    for token in tokens:
        if token in operadores:
            if token in {'*', '+', '?'}:  # operadores unarios (derecha-asociativos)
                while (pila and pila[-1] in operadores and
                       precedencia[token] < precedencia[pila[-1]]):
                    salida.append(pila.pop())
            else:  # binarios (izquierda-asociativos)
                while (pila and pila[-1] in operadores and
                       precedencia[token] <= precedencia[pila[-1]]):
                    salida.append(pila.pop())
            pila.append(token)

        elif token == '(':
            pila.append(token)

        elif token == ')':
            while pila and pila[-1] != '(':
                salida.append(pila.pop())
            if not pila:
                raise ValueError("Falta paréntesis de apertura")
            pila.pop()  # eliminar '('

        else:
            # literal o símbolo especial (if, else, ε, \{, \}, etc.)
            salida.append(token)

    # vaciar la pila
    while pila:
        top = pila.pop()
        if top in {'(', ')'}:
            raise ValueError("Paréntesis desbalanceados.")
        salida.append(top)

    return salida

"""
Módulo shunting_yard: convierte expresiones regulares de notación infix
a notación postfix (RPN) usando el algoritmo de Shunting Yard.
"""

def shunting_yard(regex: str) -> list[str]:
    salida, pila = [], []
    precedencia = {'*': 3, '.': 2, '|': 1}
    operadores = set(precedencia.keys())
    i = 0
    while i < len(regex):
        c = regex[i]
        if c == ' ':
            i += 1
            continue
        if c == '\\':  # manejar escapes
            if i + 1 < len(regex):
                salida.append('\\' + regex[i + 1])
                i += 2
            else:
                raise ValueError("Secuencia de escape incompleta")
        elif c.isalnum() or c == 'ε':
            salida.append(c)
            i += 1
        elif c == '(':
            pila.append(c)
            i += 1
        elif c == ')':
            while pila and pila[-1] != '(':
                salida.append(pila.pop())
            if not pila:
                raise ValueError("Falta paréntesis de apertura")
            pila.pop()
            i += 1
        elif c in operadores:
            while (pila and pila[-1] in operadores and
                   precedencia[c] <= precedencia[pila[-1]]):
                salida.append(pila.pop())
            pila.append(c)
            i += 1
        else:
            raise ValueError(f"Carácter no reconocido: '{c}'")
    while pila:
        top = pila.pop()
        if top in {'(', ')'}:
            raise ValueError("Paréntesis desbalanceados.")
        salida.append(top)
    return salida

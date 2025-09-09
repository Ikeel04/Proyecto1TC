"""
Módulo tokenizer: se encarga de preparar la expresión regular
antes de pasarla al algoritmo de Shunting Yard.
Incluye:
- expandir clases de caracteres [abc] → (a|b|c)
- insertar concatenaciones explícitas (.)
- expandir operadores + y ?
"""

def expandir_clases(expr: str) -> str:
    """
    Convierte clases de caracteres [abc] en (a|b|c).
    También maneja secuencias de escape con '\'.
    """
    resultado = ''
    i = 0
    while i < len(expr):
        if expr[i] == '\\':
            if i + 1 < len(expr):
                resultado += expr[i:i+2]
                i += 2
            else:
                raise ValueError("Escape incompleto")
        elif expr[i] == '[':
            i += 1
            contenido = ''
            while i < len(expr) and expr[i] != ']':
                contenido += expr[i]
                i += 1
            if i < len(expr) and contenido:
                resultado += '(' + '|'.join(contenido) + ')'
                i += 1
            else:
                raise ValueError("Clase de caracteres sin cerrar o vacía")
        else:
            resultado += expr[i]
            i += 1
    return resultado


def insertar_concatenaciones(expr: str) -> str:
    """
    Inserta el operador de concatenación explícito '.' cuando es necesario.
    Ejemplo: ab → a.b, (a|b)c → (a|b).c
    """
    if not expr:
        return expr
    resultado = ''
    i = 0
    while i < len(expr) - 1:
        c1 = expr[i]
        c2 = expr[i + 1]
        resultado += c1
        if c1 == '\\':  # manejar escapes
            i += 1
            resultado += expr[i]
            if i + 1 < len(expr):
                c2 = expr[i + 1]
            else:
                break
        # regla de concatenación implícita
        if (
            (c1 in {'*', '+', '?', ')', 'ε', '_'} or c1.isalnum()) and
            (c2 in {'(', 'ε', '_'} or c2.isalnum() or c2 == '\\')
        ):
            resultado += '.'
        i += 1
    resultado += expr[-1]
    return resultado


def expandir_operadores(expr: str) -> str:
    i = 0
    resultado = ''
    while i < len(expr):
        if expr[i] == '\\':
            if i + 1 < len(expr):
                resultado += expr[i:i+2]
                i += 2
            else:
                raise ValueError("Escape incompleto")
        elif expr[i] == '+':
            if resultado and resultado[-1] == ')':
                count = 0
                j = len(resultado) - 1
                while j >= 0:
                    if resultado[j] == ')':
                        count += 1
                    elif resultado[j] == '(':
                        count -= 1
                        if count == 0:
                            break
                    j -= 1
                grupo = resultado[j:]
                resultado = resultado[:j] + '(' + grupo + '.' + grupo + '*)'
            else:
                j = len(resultado) - 1
                while j >= 0 and resultado[j] == '.':
                    j -= 1
                if j < 0:
                    raise ValueError("Operador '+' sin operando previo")
                prev = resultado[j]
                resultado = resultado[:j] + '(' + prev + '.' + prev + '*)'
            i += 1
        elif expr[i] == '?':
            if resultado and resultado[-1] == ')':
                count = 0
                j = len(resultado) - 1
                while j >= 0:
                    if resultado[j] == ')':
                        count += 1
                    elif resultado[j] == '(':
                        count -= 1
                        if count == 0:
                            break
                    j -= 1
                grupo = resultado[j:]
                resultado = resultado[:j] + '(' + grupo + '|ε)'
            else:
                j = len(resultado) - 1
                while j >= 0 and resultado[j] == '.':
                    j -= 1
                if j < 0:
                    raise ValueError("Operador '?' sin operando previo")
                prev = resultado[j]
                resultado = resultado[:j] + '(' + prev + '|ε)'
            i += 1
        else:
            resultado += expr[i]
            i += 1
    return resultado


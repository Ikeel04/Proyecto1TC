"""
Módulo tokenizer: se encarga de preparar la expresión regular
antes de pasarla al algoritmo de Shunting Yard.

Incluye:
- expandir clases de caracteres [abc] → (a|b|c)
- insertar concatenaciones explícitas (.)
- expandir operadores + y ?
- tokenizar literales escapados (\{, \}, \?, etc.)
"""

RESERVED_WORDS = {"if", "else", "while", "for"}  # Palabras reservadas válidas


def expandir_clases(expr: str) -> str:
    r"""
    Convierte clases de caracteres [abc] en (a|b|c).
    También maneja secuencias de escape con '\\'.
    """
    resultado = ''
    i = 0
    while i < len(expr):
        if expr[i] == '\\':  # escape
            if i + 1 < len(expr):
                resultado += expr[i:i+2]
                i += 2
            else:
                raise ValueError("Escape incompleto")
        elif expr[i] == '[':  # clase de caracteres
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


def insertar_concatenaciones_tokens(tokens: list[str]) -> list[str]:
    """
    Inserta '.' entre tokens que deben ir concatenados.
    """
    if not tokens:
        return tokens

    resultado = []
    for i in range(len(tokens) - 1):
        t1, t2 = tokens[i], tokens[i+1]
        resultado.append(t1)

        # condiciones para concatenación
        if (
            t1 not in {'(', '|', '.'} and
            t2 not in {')', '|', '*', '+', '?', '.'}
        ):
            # no partimos bloques escapados \{ ... \}
            if not (t1 == '\\{' or t2 == '\\}'):
                resultado.append('.')

    resultado.append(tokens[-1])
    return resultado


def expandir_operadores(expr: str) -> str:
    """
    Expande los operadores + y ? en su forma equivalente:
      A+ → (A.A*)
      A? → (A|ε)
    """
    i = 0
    resultado = ''
    while i < len(expr):
        if expr[i] == '\\':  # caracter escapado
            if i + 1 < len(expr):
                resultado += expr[i:i+2]
                i += 2
            else:
                raise ValueError("Escape incompleto")

        elif expr[i] in {'+', '?'}:
            op = expr[i]
            if resultado and resultado[-1] == ')':
                # buscar inicio del grupo
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
                if j < 0:
                    raise ValueError(f"Paréntesis desbalanceados antes de '{op}'")

                grupo = resultado[j:]
                if op == '+':
                    expansion = f'{grupo}.{grupo}*'
                else:
                    expansion = f'({grupo}|ε)'

                resultado = resultado[:j] + expansion
            else:
                prev = resultado[-1]
                if op == '+':
                    expansion = f'({prev}.{prev}*)'
                else:
                    expansion = f'({prev}|ε)'
                resultado = resultado[:-1] + expansion
            i += 1

        else:
            resultado += expr[i]
            i += 1

    return resultado


def tokenize(regex: str) -> list[str]:
    """
    Convierte la expresión en lista de tokens.
    Divide carácter por carácter, excepto palabras reservadas.
    """
    tokens = []
    i = 0
    while i < len(regex):
        c = regex[i]

        if c == ' ':
            i += 1
            continue

        if c == '\\':  # escape
            if i + 1 < len(regex):
                tokens.append('\\' + regex[i + 1])
                i += 2
            else:
                raise ValueError("Secuencia de escape incompleta")

        elif c in {'*', '+', '?', '.', '|', '(', ')'}:
            tokens.append(c)
            i += 1

        elif c == 'ε':
            tokens.append('ε')
            i += 1

        else:
            # palabra o secuencia de letras
            literal = c
            while (i + 1 < len(regex) and regex[i + 1].isalpha()):
                i += 1
                literal += regex[i]

            if literal in RESERVED_WORDS:
                tokens.append(literal)
            else:
                tokens.extend(list(literal))  # separar cada letra
            i += 1

    return tokens

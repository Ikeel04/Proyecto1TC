"""
Módulo io: funciones de entrada/salida.
- Interpretar cadenas literales (manejar \n, \t, etc.)
- Parsear una línea de archivo en (expresión, cadena)
- Procesar un archivo completo
"""

from lexer.tokenizer import expandir_clases, insertar_concatenaciones, expandir_operadores
from lexer.shunting_yard import shunting_yard
from regex_tree.parser import construir_arbol, dibujar_arbol
from automata.state import State
from automata.thompson import construir_afn_desde_arbol
from automata.draw import dibujar_afn
from automata.simulate import acepta


def interpretar_cadena_literal(s: str) -> str:
    """
    Interpreta escapes como \n, \t, \r, \\ y ε.
    """
    s = s.strip()
    if s == 'ε':
        return ''
    out = []
    i = 0
    while i < len(s):
        if s[i] == '\\' and i + 1 < len(s):
            nxt = s[i+1]
            mapa = {'n': '\n', 't': '\t', 'r': '\r', '\\': '\\'}
            out.append(mapa.get(nxt, nxt))
            i += 2
        else:
            out.append(s[i])
            i += 1
    return ''.join(out)


def parsear_linea(linea: str):
    """
    Parsea una línea del archivo en (expresión regular, cadena).
    Formatos permitidos:
    - regex ; cadena
    - regex  cadena
    - regex  (se asume w = ε)
    """
    linea = linea.strip()
    if not linea:
        return None, None
    if ';' in linea:
        r, w = linea.split(';', 1)
        return r.strip(), w.strip()
    partes = linea.split(None, 1)
    if len(partes) == 1:
        return partes[0], 'ε'
    return partes[0], partes[1]


def procesar_archivo(nombre_archivo: str):
    """
    Procesa un archivo línea por línea:
    - Construye árbol, AFN
    - Genera imágenes
    - Simula cadena w
    """
    with open(nombre_archivo, 'r', encoding='utf-8') as archivo:
        lineas = archivo.readlines()

    for i, linea in enumerate(lineas):
        original = linea.strip()
        if not original:
            continue
        try:
            r, w_raw = parsear_linea(original)
            if r is None:
                continue
            w = interpretar_cadena_literal(w_raw)

            # Preprocesar regex
            clase_expandida = expandir_clases(r)
            con_concat = insertar_concatenaciones(clase_expandida)
            expandida = expandir_operadores(con_concat)

            # Postfix
            postfijo = shunting_yard(expandida)

            # Árbol sintáctico
            raiz = construir_arbol(postfijo)
            nombre_arbol = f'arbol_expr_{i+1}'
            dibujar_arbol(raiz, nombre_arbol)

            # AFN
            State._next_id = 0  # reset ids
            afn = construir_afn_desde_arbol(raiz)
            nombre_afn = f'afn_expr_{i+1}'
            dibujar_afn(afn, nombre_afn)

            # Simulación
            ok = acepta(afn, w)

            print(f"Expresión [{i+1}]: {r}")
            print(f"Cadena w: {repr(w)}")
            print(f"Postfijo: {' '.join(postfijo)}")
            print(f"Árbol: {nombre_arbol}.png")
            print(f"AFN : {nombre_afn}.png")
            print("Resultado:", "sí" if ok else "no")
            print()
        except Exception as e:
            print(f"Error en línea #{i+1}: {e}")

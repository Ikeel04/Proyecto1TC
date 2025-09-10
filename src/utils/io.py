"""
Módulo io: funciones de entrada/salida.
- Interpretar cadenas literales (manejar \n, \t, etc.)
- Parsear una línea de archivo en (expresión, cadena)
- Procesar un archivo completo: árbol, AFN, AFD, AFDmin y simulación
"""

from lexer.tokenizer import (
    expandir_clases,
    expandir_operadores,
    insertar_concatenaciones_tokens,
    tokenize,
    tokenizar_cadena,
)
from lexer.shunting_yard import shunting_yard
from regex_tree.parser import construir_arbol, dibujar_arbol
from automata.state import State
from automata.thompson import construir_afn_desde_arbol
from automata.draw import dibujar_afn, dibujar_afd, dibujar_afd_min
from automata.simulate import acepta, acepta_afd
from automata.subset import construir_afd_desde_afn
from automata.minimize import minimizar_afd


def interpretar_cadena_literal(s: str) -> str:
    """
    Interpreta escapes como \n, \t, \r, \\ y ε.
    Retorna un string literal (ej. '{y}').
    """
    s = s.strip()
    if s == 'ε':
        return ''
    out = []
    i = 0
    while i < len(s):
        if s[i] == '\\' and i + 1 < len(s):
            nxt = s[i + 1]
            mapa = {'n': '\n', 't': '\t', 'r': '\r', '\\': '\\'}
            out.append(mapa.get(nxt, nxt))  # deja literal si no está en mapa
            i += 2
        else:
            out.append(s[i])
            i += 1
    return ''.join(out)


def parsear_linea(linea: str):
    """
    Parsea una línea del archivo en (expresión regular, cadena).
    Formatos permitidos:
      regex ; cadena
      regex  cadena
      regex  (se asume w = ε)
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
      - Construye árbol sintáctico
      - Construye AFN
      - Construye AFD por subconjuntos
      - Minimiza el AFD
      - Genera imágenes en src/results/
      - Simula la cadena w en AFN, AFD y AFDmin
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
            w_literal = interpretar_cadena_literal(w_raw)

            print(f"\n=== Procesando línea {i+1} ===")
            print("Original:", r)
            print("Cadena w:", repr(w_literal))

            # 1) expandir clases y operadores
            clase_expandida = expandir_clases(r)
            expandida = expandir_operadores(clase_expandida)
            print("Expandida (operadores):", expandida)

            # 2) tokenizar regex
            tokens = tokenize(expandida)
            print("Tokens:", tokens)

            # 3) insertar concatenaciones explícitas
            tokens_con_concat = insertar_concatenaciones_tokens(tokens)
            print("Tokens con concat.:", tokens_con_concat)

            # 4) pasar al shunting yard
            postfijo = shunting_yard(tokens_con_concat)
            print("Postfija:", ' '.join(postfijo))

            # 5) construir árbol sintáctico
            raiz = construir_arbol(postfijo)
            dibujar_arbol(raiz, f"arbol_expr_{i+1}")

            # 6) construir AFN
            State._next_id = 0  # reset ids de estados
            afn = construir_afn_desde_arbol(raiz)
            dibujar_afn(afn, f"afn_expr_{i+1}")

            # 7) construir AFD
            start_dfa, dfa_states = construir_afd_desde_afn(afn)
            dibujar_afd(start_dfa, dfa_states, f"afd_expr_{i+1}")

            # 8) minimizar AFD
            start_min, min_states = minimizar_afd(start_dfa, dfa_states)
            dibujar_afd_min(start_min, min_states, f"afd_min_expr_{i+1}")

            # 9) procesar cadena w como lista de caracteres
            tokens_w = tokenizar_cadena(w_literal) if w_literal else []
            print("Tokens w:", tokens_w)

            # 10) simulación
            ok_afn = acepta(afn, tokens_w)
            ok_afd = acepta_afd(start_dfa, tokens_w)
            ok_min = acepta_afd(start_min, tokens_w)

            print(f"Árbol: src/results/arbol_expr_{i+1}.png")
            print(f"AFN : src/results/afn_expr_{i+1}.png")
            print(f"AFD : src/results/afd_expr_{i+1}.png")
            print(f"AFDmin: src/results/afd_min_expr_{i+1}.png")
            print("Resultado AFN   :", "sí" if ok_afn else "no")
            print("Resultado AFD   :", "sí" if ok_afd else "no")
            print("Resultado AFDmin:", "sí" if ok_min else "no")
            print()

        except Exception as e:
            print(f"Error en línea #{i+1}: {e}")

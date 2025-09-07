"""
Funciones para dibujar AFNs y AFDs usando Graphviz.
Los resultados se guardan en src/results/.
"""

import os
from graphviz import Digraph
from .state import State

# Carpeta donde se guardarán las imágenes
RESULTS_DIR = os.path.join(os.path.dirname(__file__), "..", "results")
os.makedirs(RESULTS_DIR, exist_ok=True)


def _recolectar_estados(start):
    """
    Recorre todos los estados alcanzables desde un estado inicial.
    """
    vistos = set()
    pila = [start]
    while pila:
        s = pila.pop()
        if s in vistos:
            continue
        vistos.add(s)
        for dests in s.edges.values():
            pila.extend(dests)
        pila.extend(s.eps)
    return vistos


def _mostrar_simbolo(sym):
    """
    Traduce símbolos especiales para que se vean bien en Graphviz.
    """
    if sym.startswith('\\'):
        m = sym[1:]
        mapa = {'n': '\\n', 't': '\\t', 'r': '\\r', '\\': '\\\\'}
        return mapa.get(m, '\\' + m)
    return sym


def dibujar_afn(fragment, filename, aceptar_ids=None):
    """
    Dibuja un AFN construido con Thompson.
    """
    if aceptar_ids is None:
        aceptar_ids = {s.id for s in fragment.accepts}
    dot = Digraph()
    dot.attr(rankdir='LR')

    dot.node('start', shape='point')
    dot.edge('start', str(fragment.start.id), label='')

    estados = _recolectar_estados(fragment.start)

    for s in estados:
        shape = 'doublecircle' if s.id in aceptar_ids else 'circle'
        dot.node(str(s.id), shape=shape, label=f'q{s.id}')

    for s in estados:
        for sym, dests in s.edges.items():
            for d in dests:
                dot.edge(str(s.id), str(d.id), label=_mostrar_simbolo(sym))
        for d in s.eps:
            dot.edge(str(s.id), str(d.id), label='ε')

    output_path = os.path.join(RESULTS_DIR, filename)
    dot.render(output_path, format='png', cleanup=True)


def dibujar_afd(start_dfa, estados, filename):
    """
    Dibuja un AFD construido con el algoritmo de subconjuntos.
    """
    dot = Digraph()
    dot.attr(rankdir='LR')

    dot.node('start', shape='point')
    dot.edge('start', str(start_dfa.id))

    for s in estados:
        shape = 'doublecircle' if s.is_accept else 'circle'
        dot.node(str(s.id), shape=shape, label=f'D{s.id}')

    for s in estados:
        for sym, dest in s.edges.items():
            dot.edge(str(s.id), str(dest.id), label=_mostrar_simbolo(sym))

    output_path = os.path.join(RESULTS_DIR, filename)
    dot.render(output_path, format='png', cleanup=True)

def dibujar_afd_min(start_min, estados, filename):
    """
    Dibuja el AFD minimizado.
    """
    dot = Digraph()
    dot.attr(rankdir='LR')

    dot.node('start', shape='point')
    dot.edge('start', str(start_min.id))

    for s in estados:
        shape = 'doublecircle' if s.is_accept else 'circle'
        dot.node(str(s.id), shape=shape, label=f'M{s.id}')

    for s in estados:
        for sym, dest in s.edges.items():
            dot.edge(str(s.id), str(dest.id), label=_mostrar_simbolo(sym))

    output_path = os.path.join(RESULTS_DIR, filename)
    dot.render(output_path, format='png', cleanup=True)


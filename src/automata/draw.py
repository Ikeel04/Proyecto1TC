"""
Funciones para dibujar AFNs (y en el futuro AFDs) usando Graphviz.
"""

from graphviz import Digraph
from .state import State

def _recolectar_estados(start):
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
    if sym.startswith('\\'):
        m = sym[1:]
        mapa = {'n': '\\n', 't': '\\t', 'r': '\\r', '\\': '\\\\'}
        return mapa.get(m, '\\' + m)
    return sym

def dibujar_afn(fragment, filename, aceptar_ids=None):
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

    dot.render(filename, format='png', cleanup=True)

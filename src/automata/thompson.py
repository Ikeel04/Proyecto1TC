"""
Construcción de un AFN a partir de un árbol sintáctico usando
el algoritmo de Thompson.
"""

from .state import State
from .fragment import Fragment

def _lit(symbol):
    s = State()
    f = State()
    if symbol == 'ε':
        s.eps.add(f)
    else:
        s.edges.setdefault(symbol, set()).add(f)
    return Fragment(s, {f})

def _concat(a, b):
    for x in a.accepts:
        x.eps.add(b.start)
    return Fragment(a.start, b.accepts)

def _alt(a, b):
    s = State()
    f = State()
    s.eps.update([a.start, b.start])
    for x in a.accepts:
        x.eps.add(f)
    for x in b.accepts:
        x.eps.add(f)
    return Fragment(s, {f})

def _star(a):
    s = State()
    f = State()
    s.eps.update([a.start, f])
    for x in a.accepts:
        x.eps.update([a.start, f])
    return Fragment(s, {f})

def construir_afn_desde_arbol(nodo):
    """
    Construye un AFN completo a partir del árbol de la ER.
    """
    if nodo is None:
        return _lit('ε')

    v = nodo.valor
    if nodo.izquierda is None and nodo.derecha is None:
        return _lit(v)

    if v == '.':
        return _concat(construir_afn_desde_arbol(nodo.izquierda),
                       construir_afn_desde_arbol(nodo.derecha))
    elif v == '|':
        return _alt(construir_afn_desde_arbol(nodo.izquierda),
                    construir_afn_desde_arbol(nodo.derecha))
    elif v == '*':
        return _star(construir_afn_desde_arbol(nodo.izquierda))
    elif v == '+':
        A = construir_afn_desde_arbol(nodo.izquierda)
        return _concat(A, _star(A))
    elif v == '?':
        A = construir_afn_desde_arbol(nodo.izquierda)
        return _alt(A, _lit('ε'))

    raise ValueError(f"Operador no soportado en árbol: {v}")

"""
Construcción de un AFN a partir de un árbol sintáctico usando
el algoritmo de Thompson.
"""

from .state import State
from .fragment import Fragment


def _lit(symbol: str) -> Fragment:
    """
    Construye un fragmento para un literal o epsilon.
    """
    s = State()
    f = State()
    if symbol == 'ε':
        # transición epsilon directa
        s.eps.add(f)
    else:
        # transición con símbolo (puede ser 'a', 'if', '\{', etc.)
        s.edges.setdefault(symbol, set()).add(f)
    return Fragment(s, {f})


def _concat(a: Fragment, b: Fragment) -> Fragment:
    """
    Concatenación de fragmentos A.B
    """
    for x in a.accepts:
        x.eps.add(b.start)
    return Fragment(a.start, b.accepts)


def _alt(a: Fragment, b: Fragment) -> Fragment:
    """
    Alternativa (A|B).
    """
    s = State()
    f = State()
    s.eps.update([a.start, b.start])
    for x in a.accepts:
        x.eps.add(f)
    for x in b.accepts:
        x.eps.add(f)
    return Fragment(s, {f})


def _star(a: Fragment) -> Fragment:
    """
    Cierre de Kleene (A*).
    """
    s = State()
    f = State()
    s.eps.update([a.start, f])
    for x in a.accepts:
        x.eps.update([a.start, f])
    return Fragment(s, {f})


def _plus(a: Fragment) -> Fragment:
    """
    Uno o más (A+).
    Implementado como A concatenado con A*.
    """
    return _concat(a, _star(a))


def _optional(a: Fragment) -> Fragment:
    """
    Cero o uno (A?).
    Implementado como A | ε.
    """
    return _alt(a, _lit('ε'))


def construir_afn_desde_arbol(nodo) -> Fragment:
    """
    Construye un AFN completo a partir del árbol sintáctico
    de una expresión regular.

    nodo.valor puede ser:
      - '.'  → concatenación
      - '|'  → alternativa
      - '*'  → estrella de Kleene
      - '+'  → uno o más
      - '?'  → cero o uno
      - literal (a, b, if, else, \{, \}, ε, etc.)
    """
    if nodo is None:
        return _lit('ε')

    v = nodo.valor

    # caso hoja
    if nodo.izquierda is None and nodo.derecha is None:
        return _lit(v)

    # caso operador
    if v == '.':
        return _concat(
            construir_afn_desde_arbol(nodo.izquierda),
            construir_afn_desde_arbol(nodo.derecha)
        )
    elif v == '|':
        return _alt(
            construir_afn_desde_arbol(nodo.izquierda),
            construir_afn_desde_arbol(nodo.derecha)
        )
    elif v == '*':
        return _star(construir_afn_desde_arbol(nodo.izquierda))
    elif v == '+':
        return _plus(construir_afn_desde_arbol(nodo.izquierda))
    elif v == '?':
        return _optional(construir_afn_desde_arbol(nodo.izquierda))

    # si llegó aquí, es un operador inesperado
    raise ValueError(f"Operador no soportado en árbol: {v}")

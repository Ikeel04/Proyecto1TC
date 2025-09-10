# automata/thompson.py
r"""
Construcción de un AFN a partir de un árbol sintáctico usando
el algoritmo de Thompson.

Notas:
- Las hojas del árbol pueden ser literales como 'a', 'if', 'else', 'ε', '\{', '\}', '\(' ...
- Durante la construcción des-escapamos: '\{' -> '{', '\}' -> '}', '\?' -> '?', '\.' -> '.', etc.
- 'ε' se interpreta como transición epsilon (None).
"""

from .state import State
from .fragment import Fragment


def _decode_literal(symbol: str):
    """
    Convierte el token de la ER a la etiqueta real de transición:
      - 'ε'  -> None  (transición epsilon)
      - tokens que empiezan con '\\' se des-escapan:
        '\\n' -> '\n', '\\t' -> '\t', '\\r' -> '\r', '\\\\' -> '\\', '\\s' -> ' ',
        y genérico: '\\{' -> '{', '\\}' -> '}', '\\(' -> '(', '\\)' -> ')', '\\?' -> '?', '\\.' -> '.'
      - el resto se deja tal cual (por ejemplo 'a', 'if', 'else').
    """
    if symbol == 'ε':
        return None
    if symbol.startswith('\\') and len(symbol) >= 2:
        s = symbol[1:]
        mapa = {'n': '\n', 't': '\t', 'r': '\r', '\\': '\\', 's': ' '}
        return mapa.get(s, s)
    return symbol


def _lit(symbol: str) -> Fragment:
    """
    Construye un fragmento para un literal o epsilon.
    """
    s = State()
    f = State()
    decoded = _decode_literal(symbol)
    if decoded is None:
        # transición epsilon
        s.eps.add(f)
    else:
        # transición con símbolo real (p. ej., '{', '}', 'if', 'else', 'a', ...)
        s.edges.setdefault(decoded, set()).add(f)
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
    Uno o más (A+): A concatenado con A*
    """
    return _concat(a, _star(a))


def _optional(a: Fragment) -> Fragment:
    """
    Cero o uno (A?): A | ε
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

    # caso hoja (literal/ε)
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

    raise ValueError(f"Operador no soportado en árbol: {v}")

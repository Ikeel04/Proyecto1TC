"""
Funciones para simular cadenas en un AFN o AFD.
Ahora soporta tokens multicaracter (ej. 'if', 'else', '\{', '\}').
"""

def epsilon_cierre(states):
    """
    Retorna el ε-cierre de un conjunto de estados del AFN.
    """
    stack = list(states)
    seen = set(states)
    while stack:
        s = stack.pop()
        for nxt in s.eps:
            if nxt not in seen:
                seen.add(nxt)
                stack.append(nxt)
    return seen


def mover(states, token: str):
    """
    Conjunto de estados alcanzables desde 'states' con el token dado.
    """
    out = set()
    for s in states:
        for sym, dests in s.edges.items():
            if _simbolo_coincide(sym, token):
                out.update(dests)
    return out


def _simbolo_coincide(sym: str, token: str) -> bool:
    """
    Verifica si un símbolo de transición 'sym' coincide con el token de entrada.
    Maneja escapes (\n, \t, \r, \\, \{, \}, \(, \), \?).
    """
    if sym == token:
        return True

    # manejar escapes comunes
    if sym.startswith('\\'):
        mapa = {
            'n': '\n',
            't': '\t',
            'r': '\r',
            '\\': '\\',
            '{': '{',
            '}': '}',
            '(': '(',
            ')': ')',
            '?': '?'
        }
        return mapa.get(sym[1:], None) == token

    return False


def acepta(fragment, tokens: list[str]) -> bool:
    """
    Simula un AFN con una lista de tokens (no caracteres sueltos).
    """
    current = epsilon_cierre({fragment.start})
    for tok in tokens:
        current = epsilon_cierre(mover(current, tok))
        if not current:
            return False
    return any(st in current for st in fragment.accepts)


def acepta_afd(start_dfa, tokens: list[str]) -> bool:
    """
    Simula un AFD con una lista de tokens.
    Usa _simbolo_coincide para soportar escapes y tokens multicaracter.
    """
    current = start_dfa
    for tok in tokens:
        found = False
        for sym, nxt in current.edges.items():
            if _simbolo_coincide(sym, tok):
                current = nxt
                found = True
                break
        if not found:
            return False
    return current.is_accept

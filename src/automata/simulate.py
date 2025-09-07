"""
Funciones para simular cadenas en un AFN construido con Thompson.
"""

def epsilon_cierre(states):
    stack = list(states)
    seen = set(states)
    while stack:
        s = stack.pop()
        for nxt in s.eps:
            if nxt not in seen:
                seen.add(nxt)
                stack.append(nxt)
    return seen

def mover(states, c):
    out = set()
    for s in states:
        for sym, dests in s.edges.items():
            if _simbolo_coincide(sym, c):
                out.update(dests)
    return out

def _simbolo_coincide(sym, c):
    if sym == c:
        return True
    if sym.startswith('\\'):
        m = sym[1:]
        mapa = {'n': '\n', 't': '\t', 'r': '\r', '\\': '\\'}
        return mapa.get(m, None) == c
    return False

def acepta(fragment, w: str) -> bool:
    current = epsilon_cierre({fragment.start})
    for ch in w:
        current = epsilon_cierre(mover(current, ch))
        if not current:
            return False
    return any(st in current for st in fragment.accepts)

def acepta_afd(start_dfa, w: str) -> bool:
    current = start_dfa
    for ch in w:
        if ch not in current.edges:
            return False
        current = current.edges[ch]
    return current.is_accept


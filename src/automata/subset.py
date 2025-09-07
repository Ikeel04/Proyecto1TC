"""
Algoritmo de subconjuntos: convierte un AFN en un AFD.
"""

from .simulate import epsilon_cierre, mover
from .state import State

class DFAState:
    _next_id = 0
    def __init__(self, nfa_states, is_accept=False):
        self.id = DFAState._next_id
        DFAState._next_id += 1
        self.nfa_states = frozenset(nfa_states)  # conjunto de estados del AFN
        self.edges = {}   # dict[símbolo, DFAState]
        self.is_accept = is_accept

    def __hash__(self):
        return hash(self.nfa_states)

    def __eq__(self, other):
        return self.nfa_states == other.nfa_states


def construir_afd_desde_afn(afn_fragment):
    """
    Construye un AFD a partir de un AFN usando el algoritmo de subconjuntos.
    Retorna: (estado_inicial, lista_de_estados)
    """
    from .draw import _recolectar_estados

    # todos los símbolos del alfabeto (excepto ε)
    nfa_states = _recolectar_estados(afn_fragment.start)
    alphabet = set()
    for s in nfa_states:
        alphabet.update(s.edges.keys())
    if 'ε' in alphabet:
        alphabet.remove('ε')

    start_set = epsilon_cierre({afn_fragment.start})
    start_dfa = DFAState(start_set, is_accept=bool(afn_fragment.accepts & start_set))

    dfa_states = {start_dfa}
    worklist = [start_dfa]
    dfa_map = {start_dfa.nfa_states: start_dfa}

    while worklist:
        current = worklist.pop()
        for sym in alphabet:
            move_set = mover(current.nfa_states, sym)
            closure = epsilon_cierre(move_set)
            if not closure:
                continue
            is_accept = bool(afn_fragment.accepts & closure)
            closure_frozen = frozenset(closure)
            if closure_frozen not in dfa_map:
                new_dfa = DFAState(closure, is_accept=is_accept)
                dfa_map[closure_frozen] = new_dfa
                dfa_states.add(new_dfa)
                worklist.append(new_dfa)
            current.edges[sym] = dfa_map[closure_frozen]

    return start_dfa, list(dfa_states)

"""
Algoritmo de minimización de AFD usando particiones (Hopcroft simplificado).
"""

def minimizar_afd(start_dfa, estados):
    """
    Recibe el AFD como (estado inicial, lista de estados DFA).
    Devuelve (nuevo_estado_inicial, lista_de_estados_minimizados).
    """
    # alfabeto
    alphabet = set()
    for s in estados:
        alphabet.update(s.edges.keys())

    # particiones iniciales: finales y no finales
    F = {s for s in estados if s.is_accept}
    NF = set(estados) - F
    P = [F, NF] if NF else [F]

    # refinamiento de particiones
    changed = True
    while changed:
        changed = False
        new_P = []
        for group in P:
            # dividir grupo por comportamiento frente a cada símbolo
            partitions = {}
            for state in group:
                signature = []
                for sym in alphabet:
                    target = state.edges.get(sym, None)
                    # buscar a qué grupo pertenece el destino
                    dest_group = None
                    for idx, g in enumerate(P):
                        if target in g:
                            dest_group = idx
                            break
                    signature.append(dest_group)
                signature = tuple(signature)
                partitions.setdefault(signature, set()).add(state)
            if len(partitions) > 1:
                changed = True
                new_P.extend(partitions.values())
            else:
                new_P.append(group)
        P = new_P

    # crear nuevos estados minimizados
    class MinState:
        _next_id = 0
        def __init__(self, nfa_set, is_accept=False):
            self.id = MinState._next_id
            MinState._next_id += 1
            self.nfa_set = nfa_set
            self.edges = {}
            self.is_accept = is_accept

    state_map = {}
    min_states = []
    for group in P:
        repr_state = next(iter(group))
        is_accept = repr_state.is_accept
        new_state = MinState(group, is_accept)
        min_states.append(new_state)
        for s in group:
            state_map[s] = new_state

    # reconstruir transiciones
    for group in P:
        repr_state = next(iter(group))
        new_state = state_map[repr_state]
        for sym, dest in repr_state.edges.items():
            new_state.edges[sym] = state_map[dest]

    # estado inicial minimizado
    start_min = state_map[start_dfa]

    return start_min, min_states

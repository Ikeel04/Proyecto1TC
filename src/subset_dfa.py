"""
Construcción por subconjuntos: NFA -> DFA
"""

from typing import Dict, List, Optional, Set, Tuple
from collections import deque


class DFA:
    def __init__(self, start: int, accepts: Set[int], trans: Dict[int, Dict[str, int]], alphabet: List[str]):
        self.start = start
        self.accepts = set(accepts)
        self.trans = {s: dict(ts) for s, ts in trans.items()}
        self.alphabet = list(alphabet)

    def to_dot(self) -> str:
        lines = []
        lines.append('digraph DFA {')
        lines.append('  rankdir=LR;')
        lines.append('  node [shape=circle];')
        lines.append('  __start [shape=plaintext,label=""];')
        lines.append(f'  __start -> {self.start};')
        for a in self.accepts:
            lines.append(f'  {a} [shape=doublecircle];')
        for s, outs in self.trans.items():
            for sym, d in outs.items():
                lines.append(f'  {s} -> {d} [label="{sym}"];')
        lines.append('}')
        return '\n'.join(lines)


def epsilon_closure(states: Set['State'], eps: str) -> Set['State']:
    stack = list(states)
    closure = set(states)
    while stack:
        s = stack.pop()
        for sym, dests in s.trans.items():
            if sym is None:  # epsilon
                for d in dests:
                    if d not in closure:
                        closure.add(d)
                        stack.append(d)
    return closure


def move(states: Set['State'], symbol: str) -> Set['State']:
    out = set()
    for s in states:
        if symbol in s.trans:
            out |= s.trans[symbol]
    return out


def determinize(nfa, alphabet: List[str]) -> Tuple[DFA, Dict[frozenset, int]]:
    # Q0 = ε-closure({nfa.start})
    start_cl = frozenset(epsilon_closure({nfa.start}, nfa.eps))
    state_id_of: Dict[frozenset, int] = {start_cl: 0}
    trans: Dict[int, Dict[str, int]] = {}
    accepts: Set[int] = set()
    queue = deque([start_cl])
    next_id = 1

    nfa_accept = nfa.accept

    while queue:
        curr = queue.popleft()
        curr_id = state_id_of[curr]
        trans.setdefault(curr_id, {})
        # marcar aceptador si incluye accept de NFA
        if nfa_accept in curr:
            accepts.add(curr_id)

        for sym in alphabet:
            # mover y cerrar
            m = move(curr, sym)
            if not m:
                continue
            cl = frozenset(epsilon_closure(m, nfa.eps))
            if cl not in state_id_of:
                state_id_of[cl] = next_id
                next_id += 1
                queue.append(cl)
            trans[curr_id][sym] = state_id_of[cl]

    dfa = DFA(0, accepts, trans, alphabet)
    return dfa, state_id_of

"""
Construcción de Thompson desde RPN.
Cada fragmento mantiene un start y un accept (único).
"""

from typing import Dict, List, Optional, Set

EPSILON_DEFAULT = 'ε'


class State:
    __slots__ = ('id', 'trans')
    def __init__(self, id_: int):
        self.id = id_
        # trans: Dict[str|None, Set[State]]
        self.trans: Dict[Optional[str], Set['State']] = {}

    def add(self, symbol: Optional[str], to_state: 'State'):
        self.trans.setdefault(symbol, set()).add(to_state)


class Fragment:
    __slots__ = ('start', 'accept', 'states')
    def __init__(self, start: 'State', accept: 'State', states: Set['State']):
        self.start = start
        self.accept = accept
        self.states = states


class NFA:
    __slots__ = ('start', 'accept', 'states', 'eps')
    def __init__(self, start: 'State', accept: 'State', states: Set['State'], eps: str = EPSILON_DEFAULT):
        self.start = start
        self.accept = accept
        self.states = states
        self.eps = eps

    def to_dot(self) -> str:
        lines = []
        lines.append('digraph NFA {')
        lines.append('  rankdir=LR;')
        lines.append('  node [shape=circle];')
        lines.append('  __start [shape=plaintext,label=""];')
        lines.append(f'  __start -> {self.start.id};')
        lines.append(f'  {self.accept.id} [shape=doublecircle];')
        for s in self.states:
            for sym, dests in s.trans.items():
                for d in dests:
                    label = sym if sym is not None else self.eps
                    lines.append(f'  {s.id} -> {d.id} [label="{label}"];')
        lines.append('}')
        return '\n'.join(lines)


class ThompsonBuilder:
    def __init__(self, eps: str = EPSILON_DEFAULT):
        self.eps = eps
        self._next_id = 0

    def _new_state(self) -> State:
        s = State(self._next_id)
        self._next_id += 1
        return s

    def build(self, postfix: List[str]) -> NFA:
        stack: List[Fragment] = []

        for tok in postfix:
            if tok in ['*', '+', '?', '|', '.']:
                if tok == '*':
                    frag = stack.pop()
                    start = self._new_state()
                    accept = self._new_state()
                    start.add(None, frag.start)
                    start.add(None, accept)
                    frag.accept.add(None, frag.start)
                    frag.accept.add(None, accept)
                    states = frag.states | {start, accept}
                    stack.append(Fragment(start, accept, states))

                elif tok == '+':
                    frag = stack.pop()
                    start = self._new_state()
                    accept = self._new_state()
                    start.add(None, frag.start)          # al menos una vez
                    frag.accept.add(None, frag.start)    # repetir
                    frag.accept.add(None, accept)        # o salir
                    states = frag.states | {start, accept}
                    stack.append(Fragment(start, accept, states))

                elif tok == '?':
                    frag = stack.pop()
                    start = self._new_state()
                    accept = self._new_state()
                    start.add(None, frag.start)          # tomar A
                    start.add(None, accept)              # o saltar A (ε)
                    frag.accept.add(None, accept)
                    states = frag.states | {start, accept}
                    stack.append(Fragment(start, accept, states))

                elif tok == '|':
                    frag2 = stack.pop()
                    frag1 = stack.pop()
                    start = self._new_state()
                    accept = self._new_state()
                    start.add(None, frag1.start)
                    start.add(None, frag2.start)
                    frag1.accept.add(None, accept)
                    frag2.accept.add(None, accept)
                    states = frag1.states | frag2.states | {start, accept}
                    stack.append(Fragment(start, accept, states))

                elif tok == '.':
                    frag2 = stack.pop()
                    frag1 = stack.pop()
                    frag1.accept.add(None, frag2.start)
                    start = frag1.start
                    accept = frag2.accept
                    states = frag1.states | frag2.states
                    stack.append(Fragment(start, accept, states))

            else:
                # operando: literal o ε
                s1 = self._new_state()
                s2 = self._new_state()
                sym = None if tok == self.eps else tok
                s1.add(sym, s2)
                stack.append(Fragment(s1, s2, {s1, s2}))

        if len(stack) != 1:
            raise ValueError("ER mal formada (sobran/faltan operadores).")
        f = stack.pop()
        return NFA(f.start, f.accept, f.states, eps=self.eps)

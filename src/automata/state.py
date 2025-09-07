"""
Definición de la clase State: representa un estado en el AFN.
Cada estado tiene:
- id único
- transiciones etiquetadas (edges)
- transiciones epsilon (eps)
"""

class State:
    _next_id = 0  # contador global

    def __init__(self):
        self.id = State._next_id
        State._next_id += 1
        self.edges = {}   # dict[str, set[State]]
        self.eps = set()  # transiciones epsilon

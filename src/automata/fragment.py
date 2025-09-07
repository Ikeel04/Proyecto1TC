"""
Definición de la clase Fragment: representa un fragmento de AFN
con un estado inicial y un conjunto de estados de aceptación.
"""

class Fragment:
    def __init__(self, start, accepts):
        self.start = start
        self.accepts = set(accepts)

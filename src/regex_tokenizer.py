"""
Tokenizador para expresiones regulares con concatenación implícita.
Soporta: literales del alfabeto, ε, (, ), |, *, +, ?
Convierte concatenación implícita en un token explícito '.'
"""

from typing import List, Set

METAS = set(['|', '*', '+', '?', '(', ')', '.'])  # '.' se usa para CONCAT


def insert_concat(tokens: List[str]) -> List[str]:
    """
    Inserta '.' de concatenación cuando corresponda.
    Reglas: X Y  => X . Y  si
      X ∈ {literal, ε, ')', '*', '+', '?'}  y  Y ∈ {literal, ε, '('}
    """
    out = []
    for i, t in enumerate(tokens):
        if i > 0:
            prev = tokens[i-1]
            prev_is_atom = (prev not in ['|', '('])   # literal, ε, ')', '*', '+', '?', '.'
            curr_is_atom = (t not in ['|', ')', '*', '+', '?'])  # literal, ε, '('
            if prev_is_atom and curr_is_atom:
                if out and out[-1] != '.':
                    out.append('.')
        out.append(t)
    return out


def tokenize(regex: str, alphabet: Set[str], eps: str = 'ε') -> List[str]:
    if not regex:
        raise ValueError("ER vacía.")

    raw = []
    for ch in regex:
        if ch.isspace():
            continue
        if ch == eps:
            raw.append(eps)
        elif ch in METAS or ch in ['|', '(', ')']:
            raw.append(ch)
        elif ch in alphabet:
            raw.append(ch)
        else:
            raise ValueError(f"Símbolo fuera del alfabeto o no reconocido: {repr(ch)}")

    tokens = insert_concat(raw)

    # Validación simple de paréntesis
    bal = 0
    for t in tokens:
        if t == '(':
            bal += 1
        elif t == ')':
            bal -= 1
            if bal < 0:
                raise ValueError("Paréntesis desbalanceados: ')' extra.")
    if bal != 0:
        raise ValueError("Paréntesis desbalanceados.")

    return tokens

"""
Convierte ER tokenizada (con '.' para concatenación) a notación postfija (RPN).
Precedencias:  '*' '+' '?'  >  '.'  >  '|'
Asociatividad: '.' y '|' son izquierdas; los unarios son posfijos.
"""

from typing import List

PRECEDENCE = {'|': 1, '.': 2, '*': 3, '+': 3, '?': 3}
LEFT_ASSOC = set(['|', '.'])  # unarios posfijos no aplican


def to_postfix(tokens: List[str]) -> List[str]:
    out: List[str] = []
    opstack: List[str] = []

    for t in tokens:
        if t == '(':
            opstack.append(t)
        elif t == ')':
            while opstack and opstack[-1] != '(':
                out.append(opstack.pop())
            if not opstack:
                raise ValueError("Paréntesis desbalanceados: falta '('")
            opstack.pop()  # descarta '('
        elif t in PRECEDENCE:
            while opstack and opstack[-1] != '(':
                top = opstack[-1]
                if ((top in PRECEDENCE) and
                    ((t in LEFT_ASSOC and PRECEDENCE[t] <= PRECEDENCE[top]) or
                     (t not in LEFT_ASSOC and PRECEDENCE[t] < PRECEDENCE[top]))):
                    out.append(opstack.pop())
                else:
                    break
            opstack.append(t)
        else:
            # operando (literal o ε)
            out.append(t)

    while opstack:
        op = opstack.pop()
        if op in ['(', ')']:
            raise ValueError("Paréntesis desbalanceados al final.")
        out.append(op)

    return out

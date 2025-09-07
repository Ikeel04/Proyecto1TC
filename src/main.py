"""
CLI mínima para:
ER -> tokens -> RPN -> NFA(Thompson) -> DFA(Subconjuntos)
Escribe NFA y DFA a archivos .dot y muestra tokens/RPN por pantalla.
"""

import argparse, os
from typing import List

from regex_tokenizer import tokenize
from shunting_yard import to_postfix
from thompson_nfa import ThompsonBuilder
from subset_dfa import determinize


def write(path: str, data: str):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(data)


def run(regex: str, alphabet: str, eps: str, outdir: str, verbose: bool):
    A = list(dict.fromkeys(alphabet))  # símbolos únicos, en orden
    tokens = tokenize(regex, set(A), eps)
    rpn = to_postfix(tokens)

    if verbose:
        print("Tokens:", tokens)
        print("RPN   :", rpn)

    nfa = ThompsonBuilder(eps=eps).build(rpn)
    nfa_dot = nfa.to_dot()
    write(os.path.join(outdir, 'nfa.dot'), nfa_dot)

    dfa, _ = determinize(nfa, A)
    dfa_dot = dfa.to_dot()
    write(os.path.join(outdir, 'dfa.dot'), dfa_dot)

    print(f"Listo. Se escribieron: {os.path.join(outdir, 'nfa.dot')} y {os.path.join(outdir, 'dfa.dot')}")


def parse_args():
    p = argparse.ArgumentParser(description="ER→RPN→NFA(Thompson)→DFA(Subconjuntos)")
    p.add_argument("--regex", required=True, help="Expresión regular entre comillas")
    p.add_argument("--alphabet", "-A", default="ab", help='Alfabeto, p.ej. "ab01"')
    p.add_argument("--eps", default="ε", help="Símbolo para épsilon (default: ε)")
    p.add_argument("--out", default="out", help="Directorio de salida")
    p.add_argument("--verbose", "-v", action="store_true", help="Imprimir tokens y RPN")
    return p.parse_args()


def main():
    args = parse_args()
    run(args.regex, args.alphabet, args.eps, args.out, args.verbose)


if __name__ == "__main__":
    main()

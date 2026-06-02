from __future__ import annotations

from dataclasses import dataclass
from itertools import combinations
import re
import shlex
from typing import Dict, Iterable, List, Sequence, Set, Tuple

Symbol = str
Production = Tuple[Symbol, ...]
Grammar = Dict[Symbol, Set[Production]]


VARIABLE_RE = re.compile(r"^[A-Z][A-Za-z0-9_]*$")
EPSILON_TOKENS = {"ε", "epsilon", "eps", "lambda", ""}


@dataclass
class CNFResult:
    start_symbol: Symbol
    grammar: Grammar


def is_variable(symbol: Symbol, variables: Set[Symbol]) -> bool:
    return symbol in variables or bool(VARIABLE_RE.match(symbol))


def parse_grammar(grammar_definition: str) -> Tuple[Grammar, Symbol, Set[Symbol]]:
    grammar: Grammar = {}
    variables: Set[Symbol] = set()
    start_symbol: Symbol | None = None

    lines = [line.strip() for line in grammar_definition.strip().splitlines() if line.strip()]
    for line in lines:
        if "->" not in line:
            raise ValueError(f"Invalid production line: {line!r}")
        lhs, rhs_text = line.split("->", 1)
        lhs = lhs.strip()
        rhs_text = rhs_text.strip()
        if not lhs:
            raise ValueError(f"Missing left-hand side in line: {line!r}")
        if start_symbol is None:
            start_symbol = lhs
        variables.add(lhs)
        grammar.setdefault(lhs, set())

        for alternative in rhs_text.split("|"):
            alt = alternative.strip()
            if alt in EPSILON_TOKENS:
                grammar[lhs].add(())
                continue
            tokens = shlex.split(alt)
            if not tokens:
                grammar[lhs].add(())
            else:
                grammar[lhs].add(tuple(tokens))

    if start_symbol is None:
        raise ValueError("Empty grammar definition")

    return grammar, start_symbol, variables


def fresh_symbol(base: str, used: Set[Symbol]) -> Symbol:
    if base not in used:
        used.add(base)
        return base

    index = 1
    while True:
        candidate = f"{base}{index}"
        if candidate not in used:
            used.add(candidate)
            return candidate
        index += 1


def add_production(grammar: Grammar, lhs: Symbol, rhs: Production) -> None:
    grammar.setdefault(lhs, set()).add(rhs)


def add_new_start_symbol(grammar: Grammar, start_symbol: Symbol, variables: Set[Symbol]) -> Symbol:
    new_start = fresh_symbol("S0", variables)
    new_grammar: Grammar = {lhs: set(rhss) for lhs, rhss in grammar.items()}
    new_grammar[new_start] = {(start_symbol,)}
    grammar.clear()
    grammar.update(new_grammar)
    variables.add(new_start)
    return new_start


def nullable_variables(grammar: Grammar, variables: Set[Symbol]) -> Set[Symbol]:
    nullable: Set[Symbol] = set()

    changed = True
    while changed:
        changed = False
        for lhs, productions in grammar.items():
            if lhs in nullable:
                continue
            for rhs in productions:
                if len(rhs) == 0:
                    nullable.add(lhs)
                    changed = True
                    break
                if all(is_variable(sym, variables) and sym in nullable for sym in rhs):
                    nullable.add(lhs)
                    changed = True
                    break
    return nullable


def remove_epsilon_productions(grammar: Grammar, start_symbol: Symbol, variables: Set[Symbol]) -> Grammar:
    nullable = nullable_variables(grammar, variables)
    new_grammar: Grammar = {lhs: set() for lhs in grammar}

    for lhs, productions in grammar.items():
        for rhs in productions:
            if len(rhs) == 0:
                continue

            nullable_positions = [i for i, sym in enumerate(rhs) if is_variable(sym, variables) and sym in nullable]
            # Keep every non-empty subset of the original RHS formed by deleting
            # nullable symbols. This is the standard epsilon-elimination step.
            for mask_bits in range(1 << len(nullable_positions)):
                to_remove = {nullable_positions[i] for i in range(len(nullable_positions)) if (mask_bits >> i) & 1}
                candidate = tuple(sym for i, sym in enumerate(rhs) if i not in to_remove)
                if candidate:
                    add_production(new_grammar, lhs, candidate)
                elif lhs == start_symbol:
                    add_production(new_grammar, lhs, ())

    # If the start symbol can derive epsilon, keep only the new start symbol epsilon.
    if start_symbol in nullable:
        add_production(new_grammar, start_symbol, ())

    return new_grammar


def unit_closure(grammar: Grammar, variables: Set[Symbol]) -> Dict[Symbol, Set[Symbol]]:
    closure: Dict[Symbol, Set[Symbol]] = {v: {v} for v in variables}

    changed = True
    while changed:
        changed = False
        for a in variables:
            reach = closure.setdefault(a, {a})
            for rhs in grammar.get(a, set()):
                if len(rhs) == 1 and is_variable(rhs[0], variables):
                    b = rhs[0]
                    if b not in reach:
                        reach.add(b)
                        changed = True
                    for c in closure.get(b, {b}):
                        if c not in reach:
                            reach.add(c)
                            changed = True
    return closure


def remove_unit_productions(grammar: Grammar, variables: Set[Symbol]) -> Grammar:
    closure = unit_closure(grammar, variables)
    new_grammar: Grammar = {lhs: set() for lhs in grammar}

    for a in variables:
        for b in closure.get(a, {a}):
            for rhs in grammar.get(b, set()):
                if len(rhs) == 1 and is_variable(rhs[0], variables):
                    continue
                add_production(new_grammar, a, rhs)

    return new_grammar


def replace_terminals_and_binarize(grammar: Grammar, variables: Set[Symbol]) -> Tuple[Grammar, Set[Symbol]]:
    used = set(variables)
    terminal_to_var: Dict[Symbol, Symbol] = {}
    helper_cache: Dict[Production, Symbol] = {}
    new_grammar: Grammar = {lhs: set() for lhs in grammar}

    def terminal_var(t: Symbol) -> Symbol:
        if t not in terminal_to_var:
            base = f"U_{re.sub(r'[^A-Za-z0-9_]', '_', t)}"
            if base == "U_":
                base = "U"
            terminal_to_var[t] = fresh_symbol(base, used)
        return terminal_to_var[t]

    def helper_var_for(rhs: Production) -> Symbol:
        """Return a shared helper variable for a binary production body."""
        if len(rhs) != 2:
            raise ValueError("helper_var_for only accepts binary productions")
        if rhs not in helper_cache:
            helper_cache[rhs] = fresh_symbol("X", used)
            add_production(new_grammar, helper_cache[rhs], rhs)
        return helper_cache[rhs]

    def build_binary_chain(symbols: Sequence[Symbol]) -> Symbol:
        """Collapse a sequence of length >= 2 into shared binary helpers."""
        if len(symbols) == 2:
            return helper_var_for((symbols[0], symbols[1]))
        tail_var = build_binary_chain(symbols[1:])
        return helper_var_for((symbols[0], tail_var))

    for lhs, productions in grammar.items():
        for rhs in productions:
            if len(rhs) == 0:
                add_production(new_grammar, lhs, rhs)
                continue

            # CNF allows A -> a directly, so only introduce terminal helper
            # variables when the production has length at least 2.
            if len(rhs) == 1 and not is_variable(rhs[0], variables):
                add_production(new_grammar, lhs, rhs)
                continue

            symbols: List[Symbol] = []
            for sym in rhs:
                if is_variable(sym, variables):
                    symbols.append(sym)
                else:
                    tv = terminal_var(sym)
                    symbols.append(tv)

            # Add terminal rules for any newly introduced terminal variables.
            for terminal, var in terminal_to_var.items():
                add_production(new_grammar, var, (terminal,))

            if len(symbols) == 1:
                add_production(new_grammar, lhs, tuple(symbols))
                continue

            if len(symbols) == 2:
                add_production(new_grammar, lhs, tuple(symbols))
                continue

            # Binarize longer productions, reusing shared helper variables for
            # repeated binary tails (for example, multiple S A suffixes).
            chain_var = build_binary_chain(tuple(symbols[1:]))
            add_production(new_grammar, lhs, (symbols[0], chain_var))

    return new_grammar, used


def to_chomsky_normal_form(grammar_definition: str) -> CNFResult:
    grammar, start_symbol, variables = parse_grammar(grammar_definition)
    start_symbol = add_new_start_symbol(grammar, start_symbol, variables)
    grammar = remove_epsilon_productions(grammar, start_symbol, variables)
    grammar = remove_unit_productions(grammar, variables)
    grammar, variables = replace_terminals_and_binarize(grammar, variables)
    return CNFResult(start_symbol=start_symbol, grammar=grammar)


def format_grammar(grammar: Grammar, start_symbol: Symbol) -> str:
    lines: List[str] = []
    ordered_lhs = [start_symbol] + sorted([lhs for lhs in grammar if lhs != start_symbol])
    seen_lhs: Set[Symbol] = set()
    for lhs in ordered_lhs:
        if lhs in seen_lhs or lhs not in grammar:
            continue
        seen_lhs.add(lhs)
        productions = sorted(grammar[lhs], key=lambda rhs: (len(rhs), rhs))
        parts: List[str] = []
        for rhs in productions:
            if len(rhs) == 0:
                parts.append("ε")
            else:
                parts.append(" ".join(rhs))
        lines.append(f"{lhs} -> {' | '.join(parts)}")
    return "\n".join(lines)

from automata.fa.dfa import DFA

# Cadeias possuem um número ímpar de a's
D1 = DFA(
    states={'q0', 'q1'},
    input_symbols={'a', 'b'},
    transitions={
        'q0': {'a': 'q1', 'b': 'q0'},
        'q1': {'a': 'q0', 'b': 'q1'}
    },
    initial_state='q0',
    final_states={'q1'}
)

# Cadeia é vazia ou termina com 0
D2 = DFA(
    states={'q1', 'q2'},
    input_symbols={'0', '1'},
    transitions={
        'q1': {'0': 'q1', '1': 'q2'},
        'q2': {'0': 'q1', '1': 'q2'}
    },
    initial_state='q1',
    final_states={'q1'}
)

# Cadeia pelo menos um 1  ou um número par de ocorrências de  0  seguem o último  1
D3 = DFA(
    states={'q1', 'q2', 'q3'},
    input_symbols={'0', '1'},
    transitions={
        'q1': {'0': 'q1', '1': 'q2'},
        'q2': {'0': 'q3', '1': 'q2'},
        'q3': {'0': 'q2', '1': 'q2'}
    },
    initial_state='q1',
    final_states={'q2'}
)

# Cadeia cuja soma dos números módulo 3 é zero e a contagem é resetada toda vez que R for encontrado 
D4 = DFA(
    states={'q0', 'q1', 'q2'},
    input_symbols={'0', '1', '2', 'R'},
    transitions={
        'q0': {'0': 'q0', '1': 'q1', '2': 'q2', 'R': 'q0'},
        'q1': {'0': 'q1', '1': 'q2', '2': 'q0', 'R': 'q0'},
        'q2': {'0': 'q2', '1': 'q0', '2': 'q1', 'R': 'q0'}
    },
    initial_state='q0',
    final_states={'q0'}
)

# Reconhece a linguagem vazia
D5 = DFA(
    states={'q0', 'q1', 'q2'},
    input_symbols={'a', 'b'},
    transitions={
        'q0': {'a': 'q1', 'b': 'q0'},
        'q1': {'a': 'q1', 'b': 'q2'},
        'q2': {'a': 'q2', 'b': 'q2'},
    },
    initial_state='q0',
    final_states=set()
)

D6 = DFA(
    states={'q0', 'q1'},
    input_symbols={'0', '1'},
    transitions={
        'q0': {'0': 'q0', '1': 'q1'},
        'q1': {'0': 'q1', '1': 'q0'}
    },
    initial_state='q0',
    final_states={'q0'}
)

D7 = DFA(
    states={'s0', 's1', 's2'},
    input_symbols={'0', '1'},
    transitions={
        's0': {'0': 's0', '1': 's1'},
        's1': {'0': 's2', '1': 's0'},
        's2': {'0': 's2', '1': 's0'}
    },
    initial_state='s0',
    final_states={'s0'}
)

# Reconhece a Linguagem Vazia
D8 = DFA(
    states={'q1', 'q2', 'q3'},
    input_symbols={'0', '1'},
    transitions={
        'q1': {'0': 'q1', '1': 'q3'},
        'q2': {'0': 'q3', '1': 'q3'},
        'q3': {'0': 'q3', '1': 'q3'}
    },
    initial_state='q1',
    final_states={'q2'}
)


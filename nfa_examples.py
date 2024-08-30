from automata.fa.nfa import NFA

# Cadeia contém 101 ou 11
N1 = NFA(
    states={'q1','q2','q3','q4'},
    input_symbols={'0','1'},
    transitions={
        'q1' : {'0': {'q1'}, '1':{'q1','q2'}},
        'q2' : {'0': {'q3'}, '': {'q3'}},
        'q3' : {'1': {'q4'}},
        'q4' : {'0': {'q4'}, '1': {'q4'}}
    },
    initial_state='q1',
    final_states={'q4'}
)

# Cadeia possui 1 na terceira posição da direita para a esquerda
N2 = NFA(
    states={'q1','q2','q3','q4'},
    input_symbols={'0','1'},
    transitions={
        'q1' : {'0': {'q1'}, '1':{'q1','q2'}},
        'q2' : {'0': {'q3'}, '1': {'q3'}},
        'q3' : {'0': {'q4'}, '1': {'q4'}},
        'q4' : {}
    },
    initial_state='q1',
    final_states={'q4'}
)

# Cadeia cadeias 0^k onde k é múltiplo de 2 ou 3
N3 = NFA(
    states={'q1','q2','q3','q4','q5','q6'},
    input_symbols={'0'},
    transitions={
        'q1' : {'': {'q2','q3'}},
        'q2' : {'0': {'q4'}},
        'q3' : {'0': {'q5'}},
        'q4' : {'0': {'q2'}},
        'q5' : {'0': {'q6'}},
        'q6' : {'0': {'q3'}}
    },
    initial_state='q1',
    final_states={'q2', 'q3'}
)

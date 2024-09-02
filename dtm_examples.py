from automata.tm.dtm import DTM

M0 = DTM(
    states={'q0', 'q1', 'q_acc','q_rej'},
    input_symbols={'a'},
    tape_symbols={'a', '.'},
    transitions={
        'q0': {
            'a': ('q1', '.', 'R'),
            '.': ('q_acc', '.', 'R')
        },
        'q1': {
            'a': ('q0', '.', 'R'),
            '.': ('q_rej', '.', 'R')
        }
    },
    initial_state='q0',
    blank_symbol='.',
    final_states={'q_acc'}
)


M1 = DTM(
    states={'start','have0','have1','match0','match1','back','check','accept'},
    input_symbols={'0', '1'},
    tape_symbols={'0', '1', 'x', '#', '.'},
    transitions={
        'start': {
            '0': ('have0', '.', 'R'),
            '1': ('have1', '.', 'R'),
            '#': ('check','#','R')
        },
        'have0': {
            '1': ('have0', '1', 'R'),
            '0': ('have0', '0', 'R'),
            '#': ('match0', '#', 'R')
        },
        'have1': {
            '1': ('have1', '1', 'R'),
            '0': ('have1', '0', 'R'),
            '#': ('match1', '#', 'R')
        },
        'match0': {
            '0': ('back', 'x', 'L'),
            'x': ('match0', 'x', 'R')
        },
        'match1': {
            '1': ('back', 'x', 'L'),
            'x': ('match1', 'x', 'R')
        },
        'back': {
            '0': ('back', '0', 'L'),
            '1': ('back', '1', 'L'),
            '#': ('back', '#', 'L'),
            'x': ('back', 'x', 'L'),
            '.' :('start', '.', 'R')
        },
        'check': {
            'x': ('check', 'x', 'R'),
            '.': ('accept','.','R')
        }
    },
    initial_state='start',
    blank_symbol='.',
    final_states={'accept'}
)

M2 = DTM(
    states={'start', 'track', 'back', 'clear1', 'accept'},
    input_symbols={'0', '1'},
    tape_symbols={'0', '1', 'x', 'y', '.'},
    transitions={
        'start': {
            '0': ('track', 'x', 'R'),
            'y': ('clear1', 'y', 'R'),
            '.': ('accept', '.', 'R')
        },
        'track': {
            '0': ('track', '0', 'R'),
            '1': ('back', 'y', 'L'),
            'y': ('track', 'y', 'R')
        },
        'back': {
            '0': ('back', '0', 'L'),
            'x': ('start', 'x', 'R'),
            'y': ('back', 'y', 'L')
        },
        'clear1': {
            'y': ('clear1', 'y', 'R'),
            '.': ('accept', '.', 'R')
        }
    },
    initial_state='start',
    blank_symbol='.',
    final_states={'accept'}
)

M3 = DTM(
    states={'right', 'carry', 'done'},
    input_symbols={'0', '1'},
    tape_symbols={'0', '1', '.'},
    transitions={
        'right': {
            '0': ('right', '0', 'R'),
            '1': ('right', '1', 'R'),
            '.': ('carry','.','L')
        },
        'carry': {
            '1': ('carry', '0', 'L'),
            '0': ('done', '1', 'L'),
            '.': ('done', '1', 'L')
        },
    },
    initial_state='right',
    blank_symbol='.',
    final_states={'done'}
)

M5 = DTM(
    states={'q0', 'q1', 'q_accept', 'q_reject', 'q_loop'},
    input_symbols={'0', '1'},
    tape_symbols={'0', '1', '.'},
    transitions={
        'q0': {
            '0': ('q1', '0', 'R'),
            '1': ('q_loop', '1', 'R'),  
            '.': ('q_accept', '.', 'R')  
        },
        'q1': {
            '0': ('q1', '0', 'R'),
            '1': ('q1', '1', 'R'),
            '.': ('q_accept', '.', 'R') 
        },
        'q_loop': {
            '0': ('q_loop', '0', 'R'),  
            '1': ('q_loop', '1', 'R'),
            '.': ('q_loop', '.', 'R')
        }
    },
    initial_state='q0',
    blank_symbol='.',
    final_states={'q_accept'}
)

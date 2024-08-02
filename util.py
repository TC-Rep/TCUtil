from automata.base.exceptions import RejectionException
from automata.tm.dtm import TMTape
from automata.tm.dtm import TMConfiguration
from automata.tm.mntm import MTMConfiguration
from automata.fa.nfa import NFA
from automata.fa.dfa import DFA

# Valida a cadeia de entrada nas simulações de FAs
def validate_string(cadeia,fa):
  import sys
  if not all(a in fa.input_symbols for a in cadeia):
    print("Cadeia inválida")
    sys.exit(0)

# Imprime o rastreamento para a execução de um DFA
def print_rastreamento_dfa(gen,fa,cadeia):
  try:
    print("Rastreamento de todos os estados alcançados:")
    i = 0
    atual = next(gen)
    for g in gen:
      novo = g
      print(f"{chr(0x03B4)}({atual},{cadeia[i]}) -> {novo}")
      i+=1
      atual = novo
  except RejectionException:
    print("")

# Imprime o rastreamento para a execução de um NFA
def print_rastreamento(gen,fa,cadeia):
  try:
    print("Rastreamento de todos os estados alcançados:")
    i = 0
    atual = set(next(gen))
    for g in gen:
      novo = set(g)
      print(f"{chr(0x03B4)}({atual},{cadeia[i]}) -> {novo}")
      i+=1
      atual = novo
  except RejectionException:
    print("")

# Imprime o rastreamento para a execução de um NPDA
def print_rastreamento_npda(gen,cadeia):
  for g in gen:
    for c in g:
      s_list = list(c.stack)
      s_list.reverse()
      print(f"({c.state},'{c.remaining_input}',Pilha:[{''.join(s_list)}])", end=" | ")
    print()
    if g == set():
      print(f"Cadeia {cadeia} não é aceita")
      sys.exit(0)
  print(f"Cadeia {cadeia} é aceita")

def dtm_configurations(gen):
  conf = []
  final_tape = ''
  current_state = ''
  try:
    for g in gen:
      current_state = g.state
      tmtape = g.tape
      index = tmtape.current_position
      blank = tmtape.blank_symbol
      left = "".join(tmtape.tape[0:index])
      right = "".join(tmtape.tape[index:len(tmtape.tape)])
      conf.append(f"{left}<{g.state}>{right}")
      final_tape = left+right
  except RejectionException:
    pass
  return current_state,final_tape.strip(),conf

# Cria um dfa no formato json exportado por
# https://www.eecis.udel.edu/~silber/automata/
def convert_to_dfa(dfa_definition):
  import json
  dfa_data = json.loads(dfa_definition)
  states = set(state["label"] for state in dfa_data["states"])
  initial_state = next(state["label"] for state in dfa_data["states"] if state["isStart"])
  final_states = set(state["label"] for state in dfa_data["states"] if state["isFinal"])
  transitions = {}
  input_symbols = set()
  for transition in dfa_data["transitions"]:
    source = transition["sourceState"]
    labels = transition["label"].split(",")
    dest = transition["destState"]
    for label in labels:
        if source not in transitions:
            transitions[source] = {}
        transitions[source][label] = dest
        input_symbols.add(label)
  dfa = DFA(
    states=states,
    input_symbols=input_symbols,
    transitions=transitions,
    initial_state=initial_state,
    final_states=final_states
  )
  return dfa

# Gerando uma tabela de transição
# Código de: https://www.eecis.udel.edu/~silber/automata/
def make_table(target_fa):
    import pandas as pd
    initial_state = target_fa.initial_state
    final_states = target_fa.final_states

    table = {}

    for from_state, to_state, symbol in target_fa.iter_transitions():
        # Prepare nice string for from_state
        if isinstance(from_state, frozenset):
            from_state_str = str(set(from_state))
        else:
            from_state_str = str(from_state)

        if from_state in final_states:
            from_state_str = "*" + from_state_str
        if from_state == initial_state:
            from_state_str = "→" + from_state_str

        # Prepare nice string for to_state
        if isinstance(to_state, frozenset):
            to_state_str = str(set(to_state))
        else:
            to_state_str = str(to_state)

        if to_state in final_states:
            to_state_str = "*" + to_state_str

        # Prepare nice symbol
        if symbol == "":
            symbol = "λ"

        from_state_dict = table.setdefault(from_state_str, dict())
        from_state_dict.setdefault(symbol, set()).add(to_state_str)

    # Reformat table for singleton sets
    for symbol_dict in table.values():
        for symbol in symbol_dict:
            if len(symbol_dict[symbol]) == 1:
                symbol_dict[symbol] = symbol_dict[symbol].pop()


    df = pd.DataFrame.from_dict(table).fillna("∅").T
    return df.reindex(sorted(df.columns), axis=1)
  
def ntm_configurations(gen):
  conf = []
  final_tape = ''
  current_state = ''
  try:
    for g in gen:
      sub_conf = [] 
      for e in g:
        current_state = e.state
        tmtape = e.tape
        index = tmtape.current_position
        blank = tmtape.blank_symbol
        left = "".join(tmtape.tape[0:index])
        right = "".join(tmtape.tape[index:len(tmtape.tape)])
        sub_conf.append(f"{left}<{e.state}>{right}")
      conf.append(sub_conf)
  except RejectionException:
    pass
  return conf
  

def mntm_configurations(gen):
  conf = []
  final_tape = ''
  current_state = ''
  try:
    for g in gen:
      confline = ""
      for e in g:
        cont = 1
        for t in e.tapes:
          index = t.current_position
          blank = t.blank_symbol
          left = "".join(t.tape[0:index])
          right = "".join(t.tape[index:len(t.tape)])
          confline = confline + (f"  Fita {cont}: {left}<{e.state}>{right}")
          cont += 1
      conf.append(confline)
  except RejectionException:
    pass
  return conf

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
  except Exception:
    print("")

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
  for transition in dfa_data["transitions"]:
    source = transition["sourceState"]
    label = transition["label"]
    dest = transition["destState"]
    if source not in transitions:
        transitions[source] = {}
    transitions[source][label] = dest
  dfa = DFA(
    states=states,
    input_symbols=set(transition["label"] for transition in dfa_data["transitions"]),
    transitions=transitions,
    initial_state=initial_state,
    final_states=final_states
  )
  return dfa
  
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

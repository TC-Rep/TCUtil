from automata.base.exceptions import RejectionException
from automata.tm.dtm import TMTape
from automata.tm.dtm import TMConfiguration
from automata.tm.mntm import MTMConfiguration

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

import networkx as nx
import matplotlib.pyplot as plt
import graphviz
from PIL import Image

# Desenha um DFA no formato Graphviz para uso no VSCode
def drawgv_DFA(fa, layoutid='dot', name='out'):
  SD1 = graphviz.Digraph(name=name, 
                       format='png', 
                       engine=layoutid)
  SD1.attr(rankdir='LR')
  for s in fa.states:
    str_s = str(s)
    if s in fa.final_states and not s == fa.initial_state:
      SD1.node(str_s, shape='doublecircle', style='filled', fillcolor="lightblue")
    elif s == fa.initial_state:
      if s in fa.final_states:
          SD1.node(str_s, shape='doublecircle', style='filled', fillcolor='beige')
      else:
          SD1.node(str_s, shape='circle', style='filled', fillcolor='beige') 
    else:
      SD1.node(str_s, shape='circle', style='filled', fillcolor="lightblue")
  for s,s_dict in fa.transitions.items():
      str_s = str(s)
      for i,t in s_dict.items():
        str_t = str(t)
        SD1.edge(str_s, str_t, label=f"{i}")
  if name == "":
    for n,v in globals().items():
      if v is fa:
        name = n
  SD1.render(name)
  img = Image.open(name+'.png')
  img.show()

# Desenha um NFA no formato Graphviz para uso no VSCode
def drawgv_NFA(fa, layoutid='dot', name='out'):
  SD1 = graphviz.Digraph(name=name, 
                       format='png', 
                       engine=layoutid)
  SD1.attr(rankdir='LR')
  for s in fa.states:
    str_s = str(s)
    if s in fa.final_states and not s == fa.initial_state:
      SD1.node(str_s, shape='doublecircle', style='filled', fillcolor="lightblue")
    elif s == fa.initial_state:
      if s in fa.final_states:
          SD1.node(str_s, shape='doublecircle', style='filled', fillcolor='beige')
      else:
          SD1.node(str_s, shape='circle', style='filled', fillcolor='beige') 
    else:
      SD1.node(str_s, shape='circle', style='filled', fillcolor="lightblue")
  for s,s_dict in fa.transitions.items():
      str_s = str(s)
      for i,t_set in s_dict.items():
        for t in t_set:
            str_t = str(t)
            if i=='':
              SD1.edge(str_s,str_t,label="ε")
            else:
              SD1.edge(str_s,str_t,label=f"{i}")
  if name == "":
    for n,v in globals().items():
      if v is fa:
        name = n
  SD1.render(name)
  img = Image.open(name+'.png')
  img.show()

# Desenha um NPDA no formato Graphviz
def drawgv_NPDA(npda, layoutid='dot', name='out'):
  SD1 = graphviz.Digraph(name=name, 
                       format='png', 
                       engine=layoutid)
  SD1.attr(rankdir='LR')
  for s in npda.states:
    if s in npda.final_states and not s == npda.initial_state:
      SD1.node(s, shape='doublecircle', style='filled', fillcolor="lightblue")
    elif s == npda.initial_state:
      if s in npda.final_states:
          SD1.node(s, shape='doublecircle', style='filled', fillcolor='beige')
      else:
          SD1.node(s, shape='circle', style='filled', fillcolor='beige') 
    else:
      SD1.node(s, shape='circle', style='filled', fillcolor="lightblue")
  for s,s_dict in npda.transitions.items():
      for i,st_dict in s_dict.items():
        if i == '':
          s_i = "ε"
        else:
          s_i = f"{i}"
        for x,t_set in st_dict.items():
          if x == '':
            s_x = "ε"
          else:
            s_x = f"{x}"
          for t,y in t_set:
              if y == '':
                s_y = "ε"
              else:
                s_y = "".join(y)
              SD1.edge(s,t,label=f"{s_i},{s_x} → {s_y}")
  if name == "":
    for n,v in globals().items():
      if v is npda:
        name = n
  SD1.render(name)
  img = Image.open(name+'.png')
  img.show()

# Desenha uma TM no formato GraphViz
def drawgv_TM(dtm, layoutid='dot', name=''):
  #blank = chr(0x2294)
  blank = chr(0x25A0)
  SD1 = graphviz.Digraph(name=name, 
                       #filename=name+ '.gv', 
                       format='png', 
                       engine=layoutid)
  SD1.attr(rankdir='LR')
  for s in dtm.states:
    if s in dtm.final_states:
      SD1.node(s, shape='doublecircle', style='filled', fillcolor='lightblue')
    elif s == dtm.initial_state:
      SD1.node(s, shape='circle', style='filled', fillcolor='beige')
    else:
      SD1.node(s, shape='circle', style='filled', fillcolor='lightgray')
  for s,s_dict in dtm.transitions.items():
      for i,t_tuple in s_dict.items():
        t,j,m = t_tuple
        if i == dtm.blank_symbol:
          i = blank
        if j == dtm.blank_symbol:
          j= blank
        SD1.edge(s,t,label=f"{i} {chr(0x2192)} {j}, {m}")
  if name == "":
    for n,v in globals().items():
      if v is dtm:
        name = n
  SD1.render(name)
  img = Image.open(name+'.png')
  img.show()

# Desenha uma NTM no formato graphviz
def drawgv_NTM(dtm, layoutid='dot', name=''):
  #blank = chr(0x2294)
  blank = chr(0x25A0)
  SD1 = graphviz.Digraph(name=name, 
                       #filename=name+ '.gv', 
                       format='png', 
                       engine=layoutid)
  SD1.attr(rankdir='LR')
  for s in dtm.states:
    if s in dtm.final_states:
      SD1.node(s, shape='doublecircle', style='filled', fillcolor='lightblue')
    elif s == dtm.initial_state:
      SD1.node(s, shape='circle', style='filled', fillcolor='beige')
    else:
      SD1.node(s, shape='circle', style='filled', fillcolor='lightgray')
  for s,s_dict in dtm.transitions.items():
      #print(s,s_dict)
      for i,t_dict in s_dict.items():
        #print(t_dict)
        for t_tuple in t_dict:
          t,j,m = t_tuple
          if i == dtm.blank_symbol:
            i = blank
          if j == dtm.blank_symbol:
            j= blank
          SD1.edge(s,t,label=f"{i} {chr(0x2192)} {j}, {m}")
  if name == "":
    for n,v in globals().items():
      if v is dtm:
        name = n
  SD1.render(name)
  img = Image.open(name+'.png')
  img.show()


# Desenha uma MNTM no formato graphviz
def drawgv_MNTM(dtm, layoutid='dot', name=''):
  #blank = chr(0x2294)
  blank = chr(0x25A0)
  SD1 = graphviz.Digraph(name=name, 
                       #filename=name+ '.gv', 
                       format='png', 
                       engine=layoutid)
  SD1.attr(rankdir='LR')
  for s in dtm.states:
    if s in dtm.final_states:
      SD1.node(s, shape='doublecircle', style='filled', fillcolor='lightblue')
    elif s == dtm.initial_state:
      SD1.node(s, shape='circle', style='filled', fillcolor='beige')
    else:
      SD1.node(s, shape='circle', style='filled', fillcolor='lightgray')
  for s,s_dict in dtm.transitions.items():
      for i,tdict in s_dict.items():
        for t_tuple in tdict:
          t,m = t_tuple
          r_str = ','.join(list(i))
          w_str = ','.join([x for x,y in m])
          m_str = ','.join([y for x,y in m])
          label = (f"({r_str}) {chr(0x2192)} ({w_str}), ({m_str})").replace(dtm.blank_symbol,blank)
          SD1.edge(s,t,label=label)
  SD1.render(name)
  img = Image.open(name+'.png')
  img.show()


# Desenha uma DTM. O parâmetro dtm é uma TM determinística no formato de automata-lib
def draw_TM(dtm,layoutid):
  blank = chr(0x2294)
  SD1 = nx.DiGraph()
  SD1.add_nodes_from(dtm.states)
  for s,s_dict in dtm.transitions.items():
    for i,t_tuple in s_dict.items():
      t,j,m = t_tuple
      if i == dtm.blank_symbol:
        i = blank
      if j == dtm.blank_symbol:
        j= blank
      #print(s,i,t,j,m)
      SD1.add_edge(s,t,label=f"{i} {chr(0x2192)} {j}, {m}")
  pos=nx.nx_agraph.pygraphviz_layout(SD1, layoutid)
  nx.draw_networkx_labels(SD1,pos=pos,font_size=8)
  nx.draw_networkx_edges(SD1,pos=pos,edgelist=list(SD1.edges()),
                       edge_color='black',
                       node_size=1000,
                       min_target_margin=1,

                       arrowsize=20)
  nx.draw_networkx_edge_labels(SD1,pos=pos,
                             edge_labels=nx.get_edge_attributes(SD1,'label'),
                             font_size=8,
                             node_size=1000)
  other = [s for s in dtm.states if not s==dtm.initial_state and not s in dtm.final_states]
  nx.draw_networkx_nodes(SD1, pos, 
      nodelist = other,
      node_size=1000, node_color='beige')
  nx.draw_networkx_nodes(SD1, pos, 
      nodelist = [dtm.initial_state],
      node_size=1000, node_color='yellow')
  nx.draw_networkx_nodes(SD1, pos, 
      nodelist = dtm.final_states,
      node_size=1000, node_color='lightgreen')
  plt.axis(False)
  plt.show()

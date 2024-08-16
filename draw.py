import networkx as nx
import matplotlib.pyplot as plt
import graphviz
from PIL import Image

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
  display(img)

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
      print(s,s_dict)
      for i,t_dict in s_dict.items():
        print(t_dict)
        for t_tuple in t_dict.items():
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
  display(img)

drawgv_NTM(ntm5,'dot','ntm5') 


# Desenha uma MNTM no formato graphviz
def drawgv_MNTM(dtm, layoutid, name):
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
      for t_dict in sdict.items():
        for i,t_tuple in t_dict.items():
          t,m = t_tuple[0]
          r_str = ','.join(list(i))
          w_str = ','.join([x for x,y in m])
          m_str = ','.join([y for x,y in m])
          label = (f"({r_str}) {chr(0x2192)} ({w_str}), ({m_str})").replace(dtm.blank_symbol,blank)
          SD1.edge(s,t,label=label)
  SD1.render(name)
  img = Image.open(name+'.png')
  display(img)


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

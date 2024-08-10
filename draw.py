import networkx as nx
import matplotlib.pyplot as plt

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
  print(other)
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

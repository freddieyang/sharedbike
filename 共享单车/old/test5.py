#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
==================
Heavy Metal Umlaut
==================

Example using unicode strings as graph labels.

Also shows creative use of the Heavy Metal Umlaut:
https://en.wikipedia.org/wiki/Heavy_metal_umlaut
"""
# Author: Aric Hagberg (hagberg@lanl.gov)

#    Copyright (C) 2006-2018 by
#    Aric Hagberg <hagberg@lanl.gov>
#    Dan Schult <dschult@colgate.edu>
#    Pieter Swart <swart@lanl.gov>
#    All rights reserved.
#    BSD license.

import matplotlib.pyplot as plt
import networkx as nx

try:
    v1 = '1'
    v2 = '2'
    v3 = '3'
    v4 = '4'
    v5 = '5'
except NameError:
    v1 = '1'
    v2 = '2'
    v3 = '3'
    v4 = '4'
    v5 = '5'

G = nx.Graph()
G.add_edge(v1, v2)
G.add_edge(v1, v3)
G.add_edge(v1, v4)
G.add_edge(v1, v5)
G.add_edge(v2, v3)
G.add_edge(v2, v4)
G.add_edge(v3, v4)
G.add_edge(v3, v5)
G.add_edge(v4, v5)


# write in UTF-8 encoding
fh = open('edgelist.utf-8', 'wb')
fh.write('# -*- coding: utf-8 -*-\n'.encode('utf-8'))  # encoding hint for emacs
nx.write_multiline_adjlist(G, fh, delimiter='\t', encoding='utf-8')

# read and store in UTF-8
fh = open('edgelist.utf-8', 'rb')
H = nx.read_multiline_adjlist(fh, delimiter='\t', encoding='utf-8')

for n in G.nodes():
    if n not in H:
        print(False)

print(list(G.nodes()))

pos = nx.spring_layout(G)
nx.draw(G, pos, font_size=16, with_labels=False)
for p in pos:  # raise text positions
    pos[p][1] += 0.07
nx.draw_networkx_labels(G, pos)
plt.show()

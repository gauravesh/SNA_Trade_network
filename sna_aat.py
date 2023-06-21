# -*- coding: utf-8 -*-
"""SNA AAT.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1ymXqJS1ryen2DrnNKk_12WprqAl5r-Wy
"""

import numpy as np
import pandas as pd

df=pd.read_csv('/content/WITS-Partner (1).csv',encoding='latin-1')
df

!echo "deb http://downloads.skewed.de/apt focal main" >> /etc/apt/sources.list
!apt-key adv --keyserver keyserver.ubuntu.com --recv-key 612DEFB798507F25
!apt-get update
!apt-get install python3-graph-tool python3-matplotlib python3-cairo
!apt purge python3-cairo
!apt install libcairo2-dev pkg-config python3-dev
!pip install --force-reinstall pycairo
!pip install zstandard
!apt-get install libcairo2-dev
!pip install pycairo
!sudo echo "deb http://downloads.skewed.de/apt bionic main" >> /etc/apt/sources.list
!sudo apt-key adv --keyserver keys.openpgp.org --recv-key 612DEFB798507F25
!sudo apt-get update
!sudo apt-get install python3-graph-tool python3-matplotlib
!sudo ln -s /usr/lib/python3/dist-packages/gi/_gi.cpython-{36m,37m}-x86_64-linux-gnu.so

from google.colab import drive
drive.mount('/content/drive')

from graph_tool.all import *

g = Graph(directed=True)

vlist=g.add_vertex(219)
g

graph_draw(g)

print(list(vlist))

v_prop = g.new_vertex_property("string")
for i in range (1,219):
  v_prop[g.vertex(i)]=df.iloc[i-1,1]
v_prop[g.vertex(0)]='India'
graph_draw(g, vertex_text=v_prop)

elist=[]
for i in range(1,219):
  elist.append((0,i))
  elist.append((i,0))
e=g.add_edge_list(elist)
graph_draw(g, vertex_text=v_prop)

"""Betweenness Centrality"""

vertex_betweenness,edge_betweeness=graph_tool.centrality.betweenness(g)

print(list(vertex_betweenness))

print(list(edge_betweeness))

"""Eigenvector Centrality"""

import scipy

m = adjacency(g)
ee, x = scipy.sparse.linalg.eigs(m, k=1)
print(ee,x)

"""Minimum spanning tree"""

tree_map=graph_tool.topology.min_spanning_tree(g)

t=graph_tool.GraphView(g,efilt=tree_map)
graph_draw(t)

"""Strongly connected components"""

comp,hist=graph_tool.topology.label_components(g)
print(list(comp))
print(hist)

"""Weakly Connected Components- Do not exist in this graph since all nodes are reachable from every other node"""

undirected_g=graph_tool.Graph(directed=False)
undirected_g=g
undirected_g.set_directed(False)
graph_draw(undirected_g)

comp, hist=graph_tool.topology.label_components(g)
print(comp.a)
print(hist)

"""Drawing graph for only trade balance"""

adj=np.zeros((219,219))
for i in range(219):
  if(df.iloc[i,8]>=0):
    adj[0][i]=df.iloc[i,8]
  else:
    adj[i][0]=df.iloc[i,8]
adj

g1 = graph_tool.Graph(directed=True)
g1.add_edge_list(np.transpose(adj.nonzero()))

graph_draw(g1)

"""Betweenness Centrality"""

vertex_betweenness,edge_betweeness=graph_tool.centrality.betweenness(g1)

print(list(vertex_betweenness))

print(list(edge_betweeness))

"""Eigenvector Centrality"""

m = adjacency(g1)
ee, x = scipy.sparse.linalg.eigs(m, k=1)
print(ee,x)

"""Minimum spanning tree"""

tree_map=graph_tool.topology.min_spanning_tree(g1)

t=graph_tool.GraphView(g1,efilt=tree_map)
graph_draw(t)

"""Strongly connected components"""

comp, hist=graph_tool.topology.label_components(g1)
print(list(comp))
print(hist)

"""Weakly connected components"""

undirected_g1=graph_tool.Graph(directed=False)
undirected_g1=g1
undirected_g1.set_directed(False)
graph_draw(undirected_g1)

comp, hist=graph_tool.topology.label_components(g)
print(comp.a)
print(hist)

"""undirected"""

adj=np.zeros((219,219))
for i in range(219):
  if(df.iloc[i,8]>=0):
    adj[0][i]=df.iloc[i,8]
  else:
    adj[i][0]=df.iloc[i,8]
adj

g2 = graph_tool.Graph(directed=False)
g2.add_edge_list(np.transpose(adj.nonzero()))

graph_draw(g2)

"""Bipartite"""

is_bi, part = graph_tool.topology.is_bipartite(g, partition=True)
print(is_bi)
graph_draw(g, vertex_fill_color=part)

is_bi, part = graph_tool.topology.is_bipartite(g1, partition=True)
print(is_bi)
graph_draw(g1, vertex_fill_color=part)

"""Planar graph layout"""

#! wget -O miniconda.sh https://repo.anaconda.com/miniconda/Miniconda3-py37_4.10.3-Linux-x86_64.sh
#! chmod +x miniconda.sh
#! bash ./miniconda.sh -b -f -p /usr/local
#! rm miniconda.sh
#! conda config --add channels conda-forge
#! conda install -qy mamba
#! mamba update -qy --all
#! mamba install -yq -c conda-forge graph-tool
#! mamba clean -qafy  # clean up after

#import sys
#sys.path.append('/usr/local/lib/python3.7/site-packages/')

## prioritize Conda libs
#import os
#os.environ['LD_LIBRARY_PATH'] = "/usr/local/lib:" + os.environ['LD_LIBRARY_PATH']

"""planar"""





"""INDEGREE AND OUTDEGREE"""

indegree = g1.get_in_degrees(g1.get_vertices())

outdegree = g1.get_out_degrees(g1.get_vertices())

for v in g1.iter_vertices():
    print(f"Vertex {v}: Indegree={indegree[v]}, Outdegree={outdegree[v]}")

"""DENSITY"""

import graph_tool.all as gt

num_vertices = g1.num_vertices()
num_edges = g1.num_edges()
density = num_edges / (num_vertices * (num_vertices - 1))
print(f"Density: {density}")

"""CLUSTERING CO-EFFICIENT"""

clustering_coeffs = gt.local_clustering(g1)
for v1 in g1.iter_vertices():
    print(f"Vertex {v1}: Clustering Coefficient={clustering_coeffs[v1]}")

"""TRANSITIVITY"""

transitivity = gt.global_clustering(g1)
print(f"Transitivity: {transitivity}")

clustering_coefficient1 = graph_tool.topology.local_clustering(g1, vertex=100)
print(f"Clustering Coefficient of Node 100: {clustering_coefficient1}")

indegree = g2.get_in_degrees(g2.get_vertices())



outdegree = g2.get_out_degrees(g2.get_vertices())

for v in g2.iter_vertices():
    print(f"Vertex {v}: Indegree={indegree[v]}, Outdegree={outdegree[v]}")

num_vertices = g2.num_vertices()
num_edges = g2.num_edges()
density =  2num_edges / (num_vertices * (num_vertices - 1))
print(f"Density: {density}")
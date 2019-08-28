# -*- coding: utf-8 -*-
"""
Created on Tue Mar 26 18:34:14 2019

@author: raphael
"""

import os
from os import path
import csv
from igraph import Graph

home = path.expanduser('~')

from enumeration import Enumerate

folder = 'Random_graphs/SBM_v6'

def import_graph(file_name):
    graph = Graph.Read_Edgelist(file_name, directed = False)
    return graph


k = 5
true_folder = '../%s' % folder
Data = '%s/Graphs/%s/Data/Edgelists' % (home, folder)
Results = '%s/Results' % true_folder
if not 'Results' in os.listdir(true_folder):
    os.mkdir(Results)
if not 'Positions' in os.listdir(Results):
    os.mkdir(Results + '/Positions')
    
with open('%s/graphlets_per_graph.csv' % Results, 'w') as to_write:
    csvw = csv.writer(to_write, delimiter = ';')
    csvw.writerow(['graph'] + ['graphlet_%s' % i for i in range(10,31)])

for gname in os.listdir(Data):
    print('%s/%s' % (Data, gname))
    graph = import_graph('%s/%s' % (Data, gname))
    pt, ps = Enumerate(graph, k).characterize_with_patterns()
    with open('%s/graphlets_per_graph.csv' % Results, 'a') as to_write:
        csvw = csv.writer(to_write, delimiter = ';')
        csvw.writerow([gname] + pt[10:])

    with open('%s/Positions/%s.csv' % (Results, gname), 'w') as to_write:
        csvw2 = csv.writer(to_write, delimiter = ';')
        for pos in ps:
            csvw2.writerow(pos) 
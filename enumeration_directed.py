# -*- coding: utf-8 -*-
"""
Created on Tue Mar 26 18:58:50 2019

@author: raphael
"""


class Enumerate_directed(object):
    DICT_PATTERNS = {
        '[1, 1, 6]' : (1, '021D'),
        '[2, 3, 3]' : (2, '021U'),
        '[1, 3, 4]' : (3, '021C'),
        '[3, 4, 5]' : (4, '111D'),
        '[1, 4, 7]' : (5, '111U'),
        '[2, 4, 6]' : (6, '030T'),
        '[4, 4, 4]' : (7, '030C'),
        '[4, 4, 8]' : (8, '201'),
        '[5, 5, 6]' : (9, '120D'),
        '[2, 7, 7]' : (10, '120U'),
        '[4, 5, 7]' : (11, '120C'),
        '[5, 7, 8]' : (12, '210'),
        '[8, 8, 8]' : (13, '300')
     }

    DICT_POSITIONS = [
        {1 : 1, 6 : 2}, #1
        {2 : 6, 3 : 7}, #2
        {1 : 3, 3 : 4, 4 : 5}, #3
        {3 : 12, 4 : 13, 5 : 14}, #4
        {1 : 15, 4 : 16, 7 : 17},#5
        {2 : 9, 4 : 10, 6 : 11}, #6
        {4 : 8}, #7
        {4 : 25, 8 : 26},#8
        {5 : 20, 6 : 21},#9
        {2 : 18, 7 : 19},#10
        {4 : 22, 5 : 23, 7 : 24},#11
        {5 : 27, 7 : 28, 8 : 29},#12
        {8 : 30},#13
    ]

    def __init__(self, graph, k):
        self.patterns_tab = []
        self.positions_tab = []
        self.special_patterns_dict = {}
        self._graph = graph
        self._k = k

    def create_list_neighbors(self):
        for v in self._graph.vs:
            v['list_neighbors'] = {'ALL' : set(), 'IN' : set(), 'OUT' : set()}
        for e in self._graph.es:
            if e.target == e.source:
                continue
            self._graph.vs[e.target]['list_neighbors']['ALL'].add(e.source)
            self._graph.vs[e.source]['list_neighbors']['ALL'].add(e.target)
            self._graph.vs[e.target]['list_neighbors']['IN'].add(e.source)
            self._graph.vs[e.source]['list_neighbors']['OUT'].add(e.target)
        for v in self._graph.vs:
            v['list_neighbors'] = \
                {
                    'ALL' : sorted(list(v['list_neighbors']['ALL']), reverse = True),
                    'IN' : sorted(list(v['list_neighbors']['IN']), reverse = True),
                    'OUT' : sorted(list(v['list_neighbors']['OUT']), reverse = True)
                }

    def graph_to_triad_index(self, graph_sub):
        tab = [0,0,0]
        for e in graph_sub.es:
            tab[e.target] += 1
            tab[e.source] += 3
        tab.sort()
        return tab

    def index_pattern(self, graph_sub):
        if len(graph_sub.vs) != self._k:
            return
        new_pattern, new_pattern_name = self.DICT_PATTERNS[str(self.graph_to_triad_index(graph_sub))]
        self.patterns_tab[new_pattern - 1] += 1
        new_positions = self.DICT_POSITIONS[new_pattern - 1]
        for v in graph_sub.vs:
            self.positions_tab[v['id_principal']][new_positions[v.indegree() + 3*v.outdegree()] - 1] += 1

    def in_neighborhood_vsub(self, list_neighbors, length_vsub):
        for n in list_neighbors['ALL']:
            if self._graph.vs[n]['id_sub'] != -1 and self._graph.vs[n]['id_sub'] != length_vsub-1:
                return True
        return False

    def add_vertex(self, graph_sub, vertex):
        vertex['id_sub'] = len(graph_sub.vs)
        graph_sub.add_vertex(name = vertex['name'], **{'id_principal' : vertex.index})

    def extend_subgraph(self, graph_sub, v, vext):
        if len(graph_sub.es) > 0 :
            self.index_pattern(graph_sub)
        if len(graph_sub.vs) == self._k:
            return
        while vext:
            new_vertex = vext.pop()
            vext2 = list(vext)
            self.add_vertex(graph_sub, new_vertex)
            for nei_of_new_vertex in new_vertex['list_neighbors']['ALL']:
                u = self._graph.vs[nei_of_new_vertex]
                if u.index >= v.index:
                    if u['id_sub'] == -1 :
                        if not self.in_neighborhood_vsub(u['list_neighbors'], len(graph_sub.vs)):
                            vext2.append(u)
                    else:
                        if u.index in new_vertex['list_neighbors']['IN']:
                            graph_sub.add_edge(u['id_sub'], len(graph_sub.vs) - 1)
                        if u.index in new_vertex['list_neighbors']['OUT']:
                            graph_sub.add_edge(len(graph_sub.vs) - 1, u['id_sub'])
                else:
                    break

            self.extend_subgraph(graph_sub, v, vext2)
            graph_sub.delete_vertices(new_vertex['id_sub'])
            new_vertex['id_sub'] = -1

    def characterize_directed_with_patterns(self):
        self.create_list_neighbors()
        self.patterns_tab = 13*[0]
        for v in self._graph.vs:
            self.positions_tab.append(30*[0])
            v['id_sub'] = -1
        for v in self._graph.vs:
            graph_sub = Graph(directed = True)
            v['id_sub'] = 0
            if not 'name' in v.attributes():
                v['name'] = str(v.index)
            graph_sub.add_vertex(name = v['name'], **{'id_principal' : v.index, 'evol_class' : 1, 'pattern_sub' : 0})

            vext = []
            for nei in v['list_neighbors']['ALL']:
                if nei > v.index:
                    vext.append(self._graph.vs[nei])

            if len(vext) > 0:
                self.extend_subgraph(graph_sub, v, vext)
            v['id_sub'] = -1
        print self.patterns_tab
        for pos in self.positions_tab:
            print pos
        return (self.patterns_tab, self.positions_tab)

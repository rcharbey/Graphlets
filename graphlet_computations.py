# -*- coding: utf-8 -*-
"""
Created on Thu Jan 31 09:54:34 2019

@author: raphael
"""
  
import math

class Graphlets_computation(object):
    def __init__(self, graphlets_per_graph, graphs = None):
        self.graphlets_per_graph = graphlets_per_graph
        self.graphs = graphs
        self.nb_graphlets = len(list(graphlets_per_graph.values())[0])
        
class Sum(Graphlets_computation):
    def __init__(self, graphlets_per_graph, graphs = None):
        Graphlets_computation.__init__(self, graphlets_per_graph, graphs = None)
    
    def compute(self):
        sum_graphlets = [0]*self.nb_graphlets
        for graph in self.graphlets_per_graph:
            for i in range(self.nb_graphlets):
                sum_graphlets[i] += self.graphlets_per_graph[graph][i]
        return sum_graphlets
        
class Local_frequency(Graphlets_computation):
    def __init__(self, graphlets_per_graph, graphs = None):
        Graphlets_computation.__init__(self, graphlets_per_graph, graphs = None)
        
    def compute(self):
        result = {}
        for graph in self.graphlets_per_graph:
            result[graph] = [] 
            total_graphlets = sum(self.graphlets_per_graph[graph])
            for g in self.graphlets_per_graph[graph]:
                if total_graphlets == 0:
                    result[graph].append(0.0)
                else:
                    result[graph].append(g / float(total_graphlets))
        return result


class Global_frequency(Graphlets_computation):
    def __init__(self, graphlets_per_graph):
        Graphlets_computation.__init__(self, graphlets_per_graph)
        
    def compute(self):
        sum_graphlets = Sum(self.graphlets_per_graph).compute()
        return [g/float(sum(sum_graphlets)) for g in sum_graphlets]

class Representativity(Graphlets_computation):                 
    def __init__(self, graphlets_per_graph, graphs = None):
        Graphlets_computation.__init__(self, graphlets_per_graph, graphs = None) 
        self.global_freq = self.compute_global_freq()
        self.local_freq = self.compute_local_freq()
        self.graphs = graphs
        print(self.global_freq)
        
    def compute_local_freq(self):
        return Local_frequency(self.graphlets_per_graph, self.graphs).compute()
        
    def compute_global_freq(self):
        return Global_frequency(self.graphlets_per_graph).compute()
        
    def compute(self):
        result = {}
        for graph in self.local_freq: 
            result[graph] = []            
            for i, g_freq in enumerate(self.local_freq[graph]):                
                temp_repr = g_freq/self.global_freq[i]
                if temp_repr > 1:
                    temp_repr = 2 - 1 / temp_repr
                    
                result[graph].append(temp_repr)
                    
        return result
    
    def compute_per_cluster(self, label_per_graph):
        sum_graphlets = Sum(self.graphlets_per_graph).compute()
        
        graphlets_per_label = {}
        for graph in label_per_graph:
            this_label = label_per_graph[graph]
            if not this_label in graphlets_per_label:
                graphlets_per_label[this_label] = [0]*len(sum_graphlets)
            for i,graphlet in enumerate(self.graphlets_per_graph[graph]):
                graphlets_per_label[this_label][i] += graphlet
                
        
        self.graphlets_per_graph = graphlets_per_label
        self.local_freq = self.compute_local_freq()
        print('--------------')
        print([round(x, 2) for x in self.global_freq])
        for cluster in self.local_freq:
            print([round(x, 2) for x in self.local_freq[cluster]])
        
        return self.compute()
        
    def compute_class(self):
        sum_graphlets = [0]*self.nb_graphlets
        for graph in self.graphs:
            for i in range(self.nb_graphlets):
                sum_graphlets[i] += self.graphlets_per_graph[graph][i]
        
        self.graphlets_per_graph = {'class' : sum_graphlets}
        self.graphs = None
        self.local_freq = self.compute_local_freq()
        
        return self.compute()
        
class RGF(Graphlets_computation):
    def __init__(self, graphlets_per_graph, graphs = None):
            Graphlets_computation.__init__(self, graphlets_per_graph, graphs = None)        
                
    def compute(self):
        local_frequencies = Local_frequency(self.graphlets_per_graph, self.graphs).compute()
        result = {}
        for graph in local_frequencies:
            total_graphlets = sum(local_frequencies[graph])            
            result[graph] = []
            for g in local_frequencies[graph]:
                if g == 0.0:
                    result[graph].append(0.0)
                else:
                    result[graph].append(-math.log(g / float(total_graphlets)))
        return result
import sys

class Graph:
    """A mutable, unweighted, directed graph type"""
    def __init__(self):
        self.graph = dict()
        
    def addEdge(self, a, b):
        """Adds a single edge to the graph"""
        if self.graph.has_key(a):
            self.graph[a].add(b)
        else:
            self.graph[a] = set(b)
    
    def addEdges(self, edges):
        """Adds edges from the provided collection of tuples.
        Each tuple's first value is an origin node and its second
        value is the corresponding destination."""
        for edge in edges:
            self.addEdge(edge[0], edge[1])
            
    def edges(self):
        """Generates edges represented by tuples"""
        for a, others in self.graph.iteritems():
            for b in others:
                yield (a, b)

# Read the edges from the standard input stream as tuples
edges = [tuple(line.strip().split('\t')) for line in sys.stdin.readlines()]

# Assemble the edges into a graph structure represented by a dictionary
graph = Graph()
graph.addEdges(edges)

# TODO - Eliminate nodes with only one input and one output edge

# Disregard the ordering (for now, at least), since we have probably added additional edges

for edge in graph.edges():
    print edge[0] + '\t' + edge[1]

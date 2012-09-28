from sys import stdin

class Graph:
    """A mutable, unweighted, directed graph type"""
    def __init__(self):
        self.graph = dict()
        
    def addEdge(self, a, b):
        """Adds a single edge to the graph if it does not already exist.
        
        Each node has a key in the graph dictionary, but may or may not
        have target nodes associated with it.
        
        """
        if self.graph.has_key(a):
            self.graph[a].add(b)
        else:
            self.graph[a] = set(b)
        
        if not self.graph.has_key(b):
            self.graph[b] = set()
    
    def addEdges(self, edges):
        """Adds edges from the provided collection of tuples.
        
        Each tuple's first value is an origin node and its second
        value is the corresponding destination.
        
        """
        for edge in edges:
            self.addEdge(edge[0], edge[1])
            
    def iterEdges(self):
        """Generates edges represented by tuples"""
        for a, others in self.graph.iteritems():
            for b in others:
                yield (a, b)
    
    def nodes(self):
        """Returns a list of all nodes"""
        return self.graph.keys()
    
    def nodesForInputEdges(self, node):
        """Nodes corresponding to the given node's input edges.
        
        Currently O(N), but we can probably do better.
        
        """
        return [a for a, others in self.graph.iteritems() if node in others];
    
    def nodesForOutputEdges(self, node):
        """Nodes corresponding to the given node's output edges"""
        if self.graph.has_key(node):
            return [b for b in self.graph[node]]
    
    def removeNode(self, node):
        """Removes a node from the graph"""
        if self.graph.has_key(node):
            # Remove node as source
            del self.graph[node]
            
            # Remove node as destination
            for targets in self.graph.itervalues():
                targets.discard(node)

# Read the edges from the standard input stream as tuples
def edges():
    for line in stdin.readlines():
        yield tuple(line.strip().split('\t'))

# Assemble the edges into a graph structure represented by a dictionary
graph = Graph()
graph.addEdges(edges())

# Eliminate nodes with only one input and one output edge. For now, this is
#  done in multiple passes. In each pass, nodes that should be deleted are
#  removed, but the process may result in new nodes that should be deleted.
# In the worst case, this is O(n^2) (assuming we fix the nodesForInputEdges
#  attribute). Can we do better?
needsAnotherPass = True
while needsAnotherPass:
    # We'll flag this as true if we delete any more.
    needsAnotherPass = False
    for node in graph.nodes():
        inputNodes = graph.nodesForInputEdges(node)
        outputNodes = graph.nodesForOutputEdges(node)
        if len(inputNodes) == 1 and len(outputNodes) == 1:
            graph.removeNode(node)
            if inputNodes[0] != outputNodes[0]:
                graph.addEdge(inputNodes[0], outputNodes[0])
            needsAnotherPass = True

# Disregard the ordering (for now, at least), since we have probably added additional edges
for edge in graph.iterEdges():
    print edge[0] + '\t' + edge[1]

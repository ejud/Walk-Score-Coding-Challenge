from sys import stdin

class Graph:
    """A mutable, unweighted, directed graph type"""
    def __init__(self):
        self.graph = dict()
        
    def addEdge(self, a, b):
        """Adds a single edge to the graph if it does not already exist.
        
        The edge must start and end at different nodes.
        
        """
        
        # Disallow an edge that starts and ends at the same node.
        assert a != b
        if a == b:
            return
        
        # Each key in self.graph is the name of a node, and each node
        #  is represented as such.
        # Values in the dictionary are tuples of two dimensions. Each
        #  value in the tuple is a set of nodes, the first of which
        #  represents nodes for the key's output edges, and the second
        #  of which represents the nodes for the key's input edges.
        # Thus, if there is a directed edge from A to B, then
        #      'B' in self.graph['A'][0]
        #  and 'A' in self.graph['B'][1]
        if self.graph.has_key(a):
            self.graph[a][0].add(b)
        else:
            self.graph[a] = (set(b), set())
        
        if self.graph.has_key(b):
            self.graph[b][1].add(a)
        else:
            self.graph[b] = (set(), set(a))
    
    def addEdges(self, edges):
        """Adds edges from the provided collection of tuples.
        
        Each tuple's first value is an origin node and its second
        value is the corresponding destination.
        
        """
        for edge in edges:
            self.addEdge(edge[0], edge[1])
    
    def edgeExists(self, a, b):
        return self.graph.has_key(a) and b in self.graph[a][0]
            
    def iterEdges(self):
        """Generates edges represented by tuples"""
        for a, tup in self.graph.iteritems():
            for b in tup[0]:
                assert a in self.graph[b][1]
                yield (a, b)
    
    def nodes(self):
        """Returns a list of all nodes"""
        return self.graph.keys()
    
    def nodesForInputEdges(self, node):
        """Nodes corresponding to the given node's input edges"""
        if self.graph.has_key(node):
            return [a for a in self.graph[node][1]]
        else:
            return []
    
    def nodesForOutputEdges(self, node):
        """Nodes corresponding to the given node's output edges"""
        if self.graph.has_key(node):
            return [b for b in self.graph[node][0]]
        else:
            return []
    
    def removeNode(self, node):
        """Removes a node from the graph, along with all of its edges"""
        if self.graph.has_key(node):
            # Note which nodes are connected to this node.
            outputEdgeNodes = self.graph[node][0]
            inputEdgeNodes = self.graph[node][1]
            
            # Remove the node from the dictionary key
            del self.graph[node]
            
            # Remove the node from its connections
            for b in outputEdgeNodes:
                # Edge to b was an output of node,
                #  so b's input edges contain node
                self.graph[b][1].discard(node)
                
            for a in inputEdgeNodes:
                # Edge from a was an input edge of node,
                #  so a's output edges contain node
                self.graph[a][0].discard(node)

# Read the edges from the standard input stream as tuples
def edges():
    for line in stdin.readlines():
        yield tuple(line.strip().split('\t'))

# Assemble the edges into a graph structure represented by a dictionary
graph = Graph()
graph.addEdges(edges())

# Eliminate nodes with only one input and one output edge.
# This is done one node at a time, but we may have to revisit
#  some nodes under certain circumstances.
# We track a set of nodes. When we are checking a node for
#  possible deletion, we pop it off the set. When a node must
#  be revisited, it is added back to the set.
checkNodes = set(graph.nodes())
while len(checkNodes) > 0:
    node = checkNodes.pop()
    inputNodes = graph.nodesForInputEdges(node)
    outputNodes = graph.nodesForOutputEdges(node)
    
    if len(inputNodes) == 0 and len(outputNodes) == 0:
        # The node is an orphan. Remove it.
        graph.removeNode(node)
    elif len(inputNodes) == 1 and len(outputNodes) == 1:
        # The node must be removed
        graph.removeNode(node)
        
        origin, destination = inputNodes[0], outputNodes[0]
        
        # Note that we have three scenarios here:
        #  1. The origin is the destination.
        # Or, the origin is not the destination, and either:
        #  2. There is already an edge from the origin to the destination
        #  3. There is not already an edge from the origin to the destination
        if origin == destination:
            # Scenario 1
            # We'll re-check it so it can be removed if it is orphaned.
            checkNodes.add(origin)
        elif graph.edgeExists(origin, destination):
            # Scenario 2
            # Since the edge already exists, the cardinality of both the
            #  origin's and destination's edges have changed, so if they have
            #  already been processed, we need to do it again.
            checkNodes.add(origin)
            checkNodes.add(destination)
        else:
            # Scenario 3
            # We'll add the edge here. Note that the edges we're adding back
            #  to each node are in the same direction as the edges we removed.
            # The cardinality of the edges of both nodes have remained the same,
            #  so we do not need to force another visit.
            graph.addEdge(origin, destination)
    
# Disregard the ordering (for now, at least), since we have probably added additional edges
for edge in graph.iterEdges():
    print edge[0] + '\t' + edge[1]

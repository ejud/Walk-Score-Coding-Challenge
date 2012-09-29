from sys import stdin
import itertools

class Graph:
    """A mutable, unweighted, directed graph type"""
    def __init__(self):
        self.graph = {}
        
    def addEdge(self, a, b, attribute=None):
        """Adds a single edge to the graph if it does not already exist.
        
        If the edge already exists, it is updated with the new attribute.
        
        The edge must start and end at different nodes.
        
        """
        
        # Disallow any edge that starts and ends at the same node.
        assert a != b
        if a == b:
            return
        
        # Each key in self.graph is the name of a node, and each node
        #  is represented as such.
        # Values in the dictionary are tuples of two dimensions.
        # The first value in the tuple is a dictionary of nodes to
        #  attributes. The nodes (keys) in this nested dictionary represent the
        #  destinations of output edges from the key of the outer dictionary.
        #  The attributes (values of the nested dictionary) represent the
        #  attribute object for the edge that was passed to this method.
        # The second value in the tuple is just a set of nodes representing
        #  the input edges to the outer dictionary's key.
        # From the above, if there is a directed edge from 'A' to 'B' with
        #  attribute 'foo', then:
        #      self.graph['A'][0]['B'] == 'foo'
        #  and 'A' in self.graph['B'][1]
        if self.graph.has_key(a):
            self.graph[a][0][b] = attribute
        else:
            self.graph[a] = ({b: attribute}, set())
        
        if self.graph.has_key(b):
            self.graph[b][1].add(a)
        else:
            self.graph[b] = ({}, set(a))
    
    def addEdges(self, edges):
        """Adds attributed edges from the provided collection of tuples.

        Each tuple should be of the form (origin, destination, attribute)

        """
        for edge in edges:
            assert(len(edge) in [2, 3])
            self.addEdge(edge[0], edge[1], edge[2] if len(edge) >= 3 else None)

    def edgeExists(self, a, b):
        return self.graph.has_key(a) and self.graph[a][0].has_key(b)
        
    def iterEdges(self):
        """Generates edges represented by tuples of the form (a, b, attribute)"""
        for a, tup in self.graph.iteritems():
            for b, attribute in tup[0].iteritems():
                assert a in self.graph[b][1]
                yield (a, b, attribute)
    
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
            return [b for b in self.graph[node][0].iterkeys()]
        else:
            return []
    
    def removeNode(self, node):
        """Removes a node from the graph, along with all of its edges"""
        if self.graph.has_key(node):
            # Note which nodes are connected to this node.
            outputEdgeNodes = self.graph[node][0].keys()
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
                del self.graph[a][0][node]

# Read the edges from the standard input stream as tuples
def inputEdges():
    for line in stdin.readlines():
        yield tuple(line.strip().split('\t'))

# Assemble the edges into a graph structure represented by a dictionary
graph = Graph()

# Track the edge count, which will be used to attribute our edges
edgeCounter = itertools.count()

# Read in the input edges and attribute them with the counter value
graph.addEdges([edge + tuple([edgeCounter.next()]) for edge in inputEdges()])

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
            #  origin's and destination's edges have changed, so we need to
            #  make sure they are processed hereafter.
            checkNodes.add(origin)
            checkNodes.add(destination)
        else:
            # Scenario 3
            # We'll add the edge here. Note that the edges we're adding back
            #  to each node are in the same direction as the edges we removed.
            # The cardinality of the edges of both nodes have remained the same,
            #  so we do not need to force another visit.
            graph.addEdge(origin, destination, edgeCounter.next())
    
# Sort the edges by their attribute value, which is the order in which we
#  added them to the graph. If any input edges still exist, they are inserted
#  in their original order.
edges = sorted(graph.iterEdges(), key=lambda edge: edge[2])

for edge in edges:
    print edge[0] + '\t' + edge[1]

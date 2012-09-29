from sys import stdin
import itertools
from graph import Graph

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

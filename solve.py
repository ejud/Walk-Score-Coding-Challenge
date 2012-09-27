import sys

# Read the edges from the standard input stream as tuples
edges = [tuple(line.strip().split('\t')) for line in sys.stdin.readlines()]

# Assemble the edges into a graph structure represented by a dictionary
graph = dict()
for edge in edges:
    if graph.has_key(edge[0]):
        graph[edge[0]].add(edge[1])
    else:
        graph[edge[0]] = set(edge[1])

# TODO - Eliminate nodes with only one input and one output edge

# Build the output collection of edges.
# Disregard the ordering (for now, at least), since we have probably added additional edges
#  at this point.
edges = [(origin, dest) for origin, destinations in graph.iteritems() for dest in destinations]

for edge in edges:
    print edge[0] + '\t' + edge[1]

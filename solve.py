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

# Print the edges back to the standard output stream
# We want to preserve the ordering of the graph, but it was lost in the data structure.
# For now, we'll use a less-than-optimal method, iterating over the original collection and
#  asking the graph whether the edge exists.
edges = [edge for edge in edges if graph.has_key(edge[0]) and edge[1] in graph[edge[0]]]

for edge in edges:
    print edge[0] + '\t' + edge[1]


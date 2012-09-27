import sys

# Read the edges from the standard input stream as tuples
edges = [tuple(line.strip().split('\t')) for line in sys.stdin.readlines()]

# TODO - Eliminate nodes with only one input and one output edge

# Print the edges back to the standard output stream
for edge in edges:
    print edge[0] + '\t' + edge[1]

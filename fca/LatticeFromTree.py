from ConceptTree import Concept, ConceptTree
import datetime
import numpy as np

input_file = "reuters_tree.json"
print("Start time: " + str(datetime.datetime.now()))
reuters = ConceptTree(input_file)
print("Tree built: " + str(datetime.datetime.now()))
print(len(reuters.edges))
print(len(reuters.paths))
max = 0
for path in reuters.paths:
    if len(path) > max:
        max = len(path)

print("Maximum path length: " + str(max))
reuters.generateLattice_v2()
print("Lattice complete: "  + str(datetime.datetime.now()))
#reuters.visualiseLattice("reuters_graph", view=True)
print(len(reuters.attributes))
print(len(reuters.attribute_labels))
print(len(reuters.attribute_nodes))
print(len(reuters.node_attributes))

reuters.findNeighbours()
reuters.generateDistances()
print(reuters.distances.values)
print("Distances complete: "  + str(datetime.datetime.now()))
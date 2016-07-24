from ConceptTree import Concept, ConceptTree
import datetime
import numpy as np
import pandas as pd

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
print("Lattice complete: " + str(datetime.datetime.now()))
#reuters.visualiseLattice("reuters_graph", view=True)
print(len(reuters.attributes))
print(len(reuters.attribute_labels))
print(len(reuters.attribute_nodes))
print(len(reuters.node_attributes))

reuters.findNeighbours()
reuters.generateDistances()
print(reuters.distances.values)
print("Distances complete: " + str(datetime.datetime.now()))

input = "../DataEngineering/reuters_tdm.csv"
f = open(input)
vocab = f.readline()
f.close()
vocab_leng = len(vocab)
proximity_matrix = np.array((vocab_leng, vocab_leng))

max_sd = reuters.distances.values.max()
for i in vocab:
    node_i = reuters.attribute_labels[i]
    for j in vocab:
        node_j = reuters.attribute_labels[j]
        proximity_matrix[i][j] = 1 - (reuters.distances[node_i][node_j] / max_sd)

print(proximity_matrix)
print("Proximities complete: " + str(datetime.datetime.now()))

np.savetxt("reuters_proximities.csv", proximity_matrix, delimiter=',')
X = pd.read_csv(input, delimiter=',')
new_TDM = np.dot(X.values, proximity_matrix)

print("New TDM complete: " + str(datetime.datetime.now()))
np.savetxt("reuters_new_tdm.csv", new_TDM, delimiter=',')

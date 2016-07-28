from ConceptTree import Concept, ConceptTree
import datetime, random
import numpy as np
import pandas as pd
from Dijkstra import dijkstra

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
print(len(reuters.lattice))
print("Lattice complete: " + str(datetime.datetime.now()))
#reuters.visualiseLattice("reuters_graph", view=True)
print(len(reuters.attributes))
print(len(reuters.attribute_labels))
print(len(reuters.attribute_nodes))
print(len(reuters.node_attributes))

"""
reuters.findNeighbours()
reuters.generateDistances()
print(reuters.distances.values)
print("Distances complete: " + str(datetime.datetime.now()))
"""
edge_list = []
for edge in reuters.lattice:
    if edge[0] != 0 and edge[1] != 0:
        edge_list.append((edge[0], edge[1], 1))
        edge_list.append((edge[1], edge[0], 1))
test_nodes = random.sample(reuters.concepts, 50)
for i in test_nodes:
    for j in test_nodes:
        print dijkstra(edge_list, i, j)
"""
input = "../DataEngineering/CleanTrainingData/clean_reuters_tdm.csv"
f = open(input)
vocab = f.readline()
f.close()
vocab = vocab[:-1]
vocab = vocab.split(',')
vocab_leng = len(vocab)
prox_seed = [[0.0 for i in range(vocab_leng)] for i in range(vocab_leng)]
proximity_matrix = np.array(prox_seed)

max_sd = reuters.distances.values.max()
print("Maximum distance: ", max_sd)
for i in range(vocab_leng):
    node_i = reuters.attribute_labels[vocab[i]]
    for j in range(vocab_leng):
        node_j = reuters.attribute_labels[vocab[j]]
        proximity_matrix[i][j] = 1 - (float(reuters.distances[node_i][node_j]) / float(max_sd))

print(proximity_matrix)
print("Proximities complete: " + str(datetime.datetime.now()))

np.savetxt("reuters_proximities.csv", proximity_matrix, delimiter=',')
X = pd.read_csv(input, delimiter=',')
new_TDM = np.dot(X.values, proximity_matrix)

print("New TDM complete: " + str(datetime.datetime.now()))
np.savetxt("reuters_new_tdm.csv", new_TDM, delimiter=',')
"""
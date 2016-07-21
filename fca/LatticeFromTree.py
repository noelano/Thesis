from ConceptTree import Concept, ConceptTree
import datetime
import Dijkstra
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

att_dict = reuters.attribute_labels
att_list = att_dict.keys()
total = len(att_list)
dist_matrix = np.zeros((total,total))
new_edge_list = []
for edge in reuters.lattice:
    new_edge_list.append((edge[0], edge[1], 1))
    new_edge_list.append((edge[1], edge[0], 1))

for i in range(total):
    if i % 100 == 0:
        print("Completed " + str(i) + " rows")
    for j in range(i+1, total):
        dist = Dijkstra.dijkstra(new_edge_list, att_dict[att_list[i]], att_dict[att_list[j]])
        try:
            dist_matrix[i][j] = dist[0]
        except:
            dist_matrix[i][j] = dist

print("Distances complete: " + str(datetime.datetime.now()))
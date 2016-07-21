from ConceptTree import Concept, ConceptTree
import numpy as np
import Dijkstra

input_file = "tealady_tree.json"
#input_file = "people_tree.json"
tree = ConceptTree(input_file)
tree.generateLattice_v2()
for edge in tree.lattice:
    print(edge)
for att in tree.attribute_labels:
    print att, tree.attribute_labels[att]
#tree.visualiseLattice("testvis.gz", view=True)

att_dict = tree.attribute_labels
att_list = att_dict.keys()
total = len(att_list)
dist_matrix = np.zeros((total,total))
new_edge_list = []
for edge in tree.lattice:
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


print(dist_matrix)
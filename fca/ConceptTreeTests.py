from ConceptTree import Concept, ConceptTree

input_file = "tealady_tree.json"
#input_file = "people_tree.json"
tree = ConceptTree(input_file)
tree.generateLattice_v2()
for edge in tree.lattice:
    print(edge)
for att in tree.attribute_labels:
    print att, tree.attribute_labels[att]
tree.visualiseLattice("testvis.gz", view=True)
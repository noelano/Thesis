import json
from graphviz import Digraph
from operator import itemgetter

class ConceptTree():
    """
    Tree structure formed from formal concept
    Consists of sets of concepts, paths, intents and objects
    Has methods to create full lattice
    """

    def __init__(self, file):
        f = open(file)
        input = f.read()
        f.close()
        input = json.loads(input)
        self.paths = []
        self.objects = []
        self.attributes = []
        self.concepts = {}
        self.edges = []
        self.edgeDict = {}
        self.branch_points = []
        self.attribute_nodes = {}
        self.object_nodes = {}
        self.attribute_labels = {}
        self.lattice = []

        self.generateEdge(input)
        self.generateEdgeDict()
        self.generatePaths([], 0)
        self.path_number = len(self.paths)
        self.addPathsToConcepts()

    def generateEdge(self, input_node, parent=None):
        """
        Generate all edges within the tree

        :param input: json object containing all nested branches
        :return:
        """
        # Add the current node to the tree and path
        current_node = input_node["Node"]
        node = Concept(current_node, input_node["attributes"], input_node["objects"], input_node["own_objects"])

        for object in node.extent:
            try:
                self.object_nodes[object].append(current_node)
            except:
                self.object_nodes[object] = [current_node]
        for attribute in node.intent:
            try:
                self.attribute_nodes[attribute].append(current_node)
            except:
                self.attribute_nodes[attribute] = [current_node]
        self.objects = list(set(self.objects).union(set(node.extent)))
        self.attributes = list(set(self.attributes).union(set(node.intent)))
        self.concepts[input_node["Node"]] = node
        if not parent == None:
            self.edges.append((parent, current_node))
            # Add child to the parent and take the intent from the parent
            self.concepts[parent].addChild(current_node)
            node.extendIntent(self.concepts[parent].full_intent[:])

        # Check for children - if any, repeat the path recursively
        try:
            if len(input_node["children"]) > 1:
                self.branch_points.append(current_node)

            for child in input_node["children"]:
                self.generateEdge(child, current_node)
        except:
            pass

    def generatePaths(self, path, node):
        """
        Generate list of all possible paths from root to leaf

        :return: path list
        """
        path.append(node)

        if len(self.edgeDict[node]) > 0:
            for child in self.edgeDict[node]:
                self.generatePaths(path[:], child)
        else:
            self.paths.append(path)

    def getPredecessors(self, node):
        """
        Get predecessors for the given node

        :param node: Concept object
        :return: predecessors: List of parents
        """

        node_label = node.label
        path_label = node.paths[0]
        path = self.paths[path_label][::-1]
        predecessors = []

        while True:
            parent = path.pop()
            if parent == node_label:
                break
            else:
                predecessors.append(parent)

        return predecessors

    def generateEdgeDict(self):

        for c in self.concepts:
            self.edgeDict[c] = []

        for edge in self.edges:
            self.edgeDict[edge[0]].append(edge[1])

    def addPathsToConcepts(self):
        """
        Add the indices of each path to each concept on it
        """

        for i in range(self.path_number):
            for p in self.paths[i]:
                if i not in self.concepts[p].paths:
                    self.concepts[p].addPath(i)


    def generateLattice_v1(self):
        """
        Generate the concept lattice from the tree

        For each concept - check if it has another parent on a different path
        Each path only needs to be checked once ie once a parent is found, move to next path
        Parents have intents which comprise a subset of the current nodes intent
        In addition the extent of the current node is a subset of the parents extent

        :return lattice_edges: list of edges in the generated lattice
        """
        lattice_edges = self.edges[:]

        for c in self.concepts:
            concept = self.concepts[c]
            already_checked = self.getPredecessors(concept)
            existing_paths = concept.paths

            # Prepare lists of paths to check
            paths_to_check = [x for x in range(self.path_number) if x not in existing_paths]

            for path_ind in paths_to_check:
                path = self.paths[path_ind][::-1]
                path = list(set(path) - set(already_checked))
                for node in path:
                    # Check if the node is a parent
                    test_concept = self.concepts[node]
                    if set(test_concept.intent).issubset(set(concept.intent)) and \
                            set(concept.extent).issubset(set(test_concept.extent)):
                        lattice_edges.append((test_concept.label, concept.label))
                        print("Added path: " + str(test_concept.label) + "," + str(concept.label))
                        already_checked += path
                        break
                    else:
                        already_checked.append(node)

        return lattice_edges

    def generateLattice_v2(self):
        """
        Generate a lattice by checking for duplicate attribute labels
        Those labels which have duplicates represent pruned edges.
        The node list attached to each such attribute will in fact form a sub-lattice
        By iterating over this, the remaining connections can be added back
        """
        self.lattice = self.edges[:]

        for att in self.attribute_nodes:
            if len(self.attribute_nodes[att]) == 1:
                # Set the label as the only node manifesting the attribute
                self.attribute_labels[att] = self.attribute_nodes[att][0]
            else:
                # Multiple nodes => edges have been cut => Form the completed sub-lattice
                self.subLatticeGeneration(self.attribute_nodes[att], att)

        # The lattice may contain duplicates of the same edge - use the 'set' object to remove these
        self.lattice = list(set(self.lattice))
        self.lattice.sort()

    def subLatticeGeneration(self, node_list, att):
        """
        The key step in the lattice generation - forming the sub-lattice from the list of input nodes
        :param node_list: list of nodes forming the sublattice
        """
        for node in node_list:
            concept = self.concepts[node]
            possible_predecessors = []
            new_list = node_list[:]
            new_list.remove(node)
            for test_node in new_list:
                nodes_to_check = self.getChildrenFromNode(test_node)
                for n in nodes_to_check:
                    test_concept = self.concepts[n]
                    if set(test_concept.full_intent).issubset(set(concept.full_intent)):
                        possible_predecessors.append(n)

            if not possible_predecessors:
                self.attribute_labels[att] = node
            elif len(possible_predecessors) == 1:
                self.lattice.append((possible_predecessors[0], node))
            else:
                for n in possible_predecessors:
                    direct = 1
                    test_concept = self.concepts[n]
                    rest = possible_predecessors
                    rest.remove(n)
                    for p in rest:
                        if set(test_concept.full_intent).issubset(set(self.concepts[p].full_intent)):
                            direct = 0
                            break
                    if direct:
                        self.lattice.append((n, node))

    def getChildrenFromNode(self, node):
        """
        Recursively generate list of all dependents starting at given node
        :param node: index of a concept node
        :param node_list: list of existing nodes that have been appended so far
        :return: list of dependent nodes
        """
        concept = self.concepts[node]
        node_list = [node]
        if concept.children:
            for child in concept.children:
                node_list += self.getChildrenFromNode(child)

        return node_list

    def visualiseLattice(self, filename, view=False):
        self.dot = Digraph(filename=filename,
                           node_attr=dict(shape='circle', width='.25', style='filled', label=''),
                           edge_attr=dict(dir='none', labeldistance='1.5', minlen='2'),)

        # Get the labels associated with any nodes
        node_labels = {}
        for node in self.concepts:
            node_labels[node] = None
        for att in self.attribute_labels:
            node_labels[self.attribute_labels[att]] = att

        for node in node_labels:
            self.dot.node(str(node), label=str(node))
        for edge in self.lattice:
            self.dot.edge(str(edge[0]), str(edge[1]))

        self.dot.render(filename=filename, view=view)


class Concept:
    """
    Concept consisting of label, intent and extent
    """

    def __init__(self, label, intent, extent, own_objects, paths=[]):
        self.intent = intent[:]
        self.extent = extent[:]
        self.label = label
        self.own_objects = own_objects
        self.full_intent = intent[:]
        self.paths = paths[:]
        self.children = []

    def addPath(self, node):
        self.paths.append(node)

    def extendIntent(self, attributes):
        self.full_intent += attributes

    def addChild(self, child):
        self.children.append(child)


if __name__ == "__main__":
    input_file = "liveinwater_tree.json"
    tree = ConceptTree(input_file)

    test_type = 2

    if test_type == 0:
        print(tree.attributes)
        print(tree.objects)
        print(tree.concepts)
        print(tree.branch_points)
        for edge in tree.edges:
            print(edge)
        print(tree.edgeDict)
        for path in tree.paths:
            print path

    if test_type == 1:
        for c in tree.concepts:
            print tree.concepts[c].paths

        for c in tree.concepts:
            concept = tree.concepts[c]
            print concept.label, concept.intent, concept.extent

    if test_type == 2:
        tree.generateLattice_v2()
        lattice = list(set(tree.lattice))
        lattice.sort()
        for edge in lattice:
            print edge
        print(str(len(lattice)))

    if test_type == 3:
        for c in tree.concepts:
            concept = tree.concepts[c]
            print(concept.label, concept.own_objects, concept.extent)
            #print(concept.label, concept.intent, concept.full_intent)

    if test_type == 4:
        print("Objects:")
        for o in tree.object_nodes:
            print("\t" + str(o) + ": " + str(tree.object_nodes[o]))
        print("Attributes:")
        for a in tree.attribute_nodes:
            print("\t" + str(a) + ": " + str(tree.attribute_nodes[a]))

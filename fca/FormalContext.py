import json
import pandas as pd

class Concept:
    def __init__(self, label, intent, extent):
        self.intent = intent[:]
        self.extent = extent[:]
        self.label = label
        self.neighbours = []

class Galois:
    def __init__(self, file):
        f = open(file)
        input = f.read()
        f.close()
        input = json.loads(input)

        self.concepts = {}
        self.attributeNodes = {}
        self.nodeAttributes = {}
        self.objectNodes = {}

        self.addConcepts(input)

        self.source = min(self.concepts)
        self.sink = max(self.concepts)

        self.attributeLabels = {}
        self.objectLabels = {}
        self.lattice = []
        self.generateLattice()

    def addConcepts(self, input):
        for concept in input["Concepts"]:
            label = concept["ConceptId"]
            attributes = concept["attributes"]
            objects = concept["objects"]
            node = Concept(label, attributes, objects)
            self.concepts[label] = node

            for y in attributes:
                try:
                    self.attributeNodes[y].append(node)
                except:
                    self.attributeNodes[y] = [node]

            for x in objects:
                try:
                    self.objectNodes[x].append(node)
                except:
                    self.objectNodes[x] = [node]

    def generateLattice(self):
        for y in self.attributeNodes.keys():
            search_list = sorted(self.attributeNodes[y], key=lambda node: len(node.intent))
            mu_y = search_list[0]
            self.attributeLabels[y] = mu_y.label

            for i in range(len(search_list)):
                children = []
                intent_1 = set(search_list[i].intent)
                for j in range(i+1, len(search_list)):
                    intent_2 = set(search_list[j].intent)
                    if intent_1.issubset(intent_2):
                        test = 1
                        for node in children:
                            intent_3 = set(node.intent)
                            if intent_2.issubset(intent_3):
                                children.remove(node)
                            if intent_3.issubset(intent_2):
                                test = 0
                        if test:
                            children.append(search_list[j])
                for c in children:
                    self.lattice.append((search_list[i].label, c.label))

        self.lattice = list(set(self.lattice))
        self.lattice.sort()

    def generateDistances(self):
        self.findNeighbours()
        for key in self.attributeLabels:
            self.nodeAttributes[self.attributeLabels[key]] = key

        base = [["Inf" for att in self.nodeAttributes] for att in self.nodeAttributes]
        self.distances = pd.DataFrame(index=self.nodeAttributes.keys(), columns=self.nodeAttributes.keys(), data=base)
        distances_found = []
        for i in self.nodeAttributes:
            #print("Working on ", i)
            self.resetSearch()
            self.distances[i][i] = 0
            self.breadthFirstSearch(i, [i], 0, distances_found)
            distances_found.append(i)

    def findNeighbours(self):
        for edge in self.lattice:
            node_1 = self.concepts[edge[0]]
            node_2 = self.concepts[edge[1]]
            node_1.neighbours.append(edge[1])
            node_2.neighbours.append(edge[0])

    def breadthFirstSearch(self, source, current_level, level, distances_found):
        level += 1
        self._already_searched += current_level
        next_level = []
        for node in current_level:
            next_level += self.concepts[node].neighbours
        next_level = list(set(next_level) - set(self._already_searched))

        for node in next_level:
            if node in self.nodeAttributes and node not in distances_found:
                if level < self.distances[source][node]:
                    self.distances[source][node] = level
                    self.distances[node][source] = level

        if next_level:
            self.breadthFirstSearch(source, next_level, level, distances_found)

    def resetSearch(self):
        self._search_counter = None
        if self.source not in self.nodeAttributes:
            self._already_searched = [self.source, self.sink]    # The root node is removed when calculating the distances between nodes.
        else:
            self._already_searched = [self.sink]



if __name__ == "__main__":

    input = "liveinwater_list.json"
    cxt = Galois(input)

    test = 2

    if test == 0:
        for node in cxt.concepts:
            print cxt.concepts[node].label, cxt.concepts[node].intent, cxt.concepts[node].extent

    if test == 1:
        for node in cxt.concepts:
            print cxt.concepts[node].label, cxt.concepts[node].intent, cxt.concepts[node].extent
        for edge in cxt.lattice:
            print edge

    if test == 2:
        cxt.generateDistances()
        print cxt.distances
import json

def latticeEdges(input, edgelist, attributeLabels):
    """
    Given a set of concepts, generate the corresponding lattice structure

    :param input:   json object storing list of concepts
    :param edgelist: filename to output edgelist to
    :param attributeLabels: filename to output list of attribute labels to
    :return: NA
    """
    output = open(edgelist,"w")
    labels = open(attributeLabels, "w")
    attributeList = []

    total = len(input["Concepts"])

    for i in range(total):
        concept = input["Concepts"][i]
        attributes = concept["attributes"]
        attributes.sort()
        att_no = len(attributes)
        source = concept["ConceptId"]
        indices = [x for x in range(total)]
        indices.remove(i)
        for j in indices:
            concept2 = input["Concepts"][j]
            sink = concept2["ConceptId"]
            attributes2 = concept2["attributes"]
            attributes2.sort()
            att_no2 = len(attributes2)
            if att_no2 == att_no + 1 and set(attributes).issubset(attributes2):
                output.write(str(source) + "," + str(sink) + "\n")
                diff = list(set(attributes2) - set(attributes))[0]
                if diff not in attributeList:
                    attributeList.append(diff)
                    labels.write(str(sink) + ": " + diff + "\n")

    output.close()
    labels.close()

f = open("liveinwater_list.json")
input = f.read()
f.close()

concept = json.loads(input)

latticeEdges(concept, "LivesInWater_Edges.txt", "LivesInWater_labels.txt")

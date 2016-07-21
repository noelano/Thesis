import graphviz as gz
import json

def addNode(graph, node):
    """ Add node to the graph """
    label = str(node["Node"])
    graph.node(label)
    try:
        for child in node["children"]:
            graph.edge(label, str(child["Node"]))
            addNode(graph, child)
    except KeyError:
        print("Root node reached")

graph = gz.Graph(format="png")
f = open("reuters_concepts.json")
input = f.read()
f.close()
root = json.loads(input)
addNode(graph, root)

f = graph.render(filename="reuters_graph")
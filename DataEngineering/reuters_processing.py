import xml.dom.minidom, os

data_dir = "../../Datasets/reuters/"
inputs = [x for x in os.listdir(data_dir) if '.sgm' in x]

output = open(data_dir + 'consolidated.txt', "w")

for file in inputs:
    print('Working on file ' + file)
    # f = open(data_dir + file)
    doc = xml.dom.minidom.parse(data_dir + file)
    doclist = doc.getElementsByTagName("REUTERS")
    for d in doclist:
        title = d.getElementsByTagName("TITLE").wholeText
        topics = []
        places = []
        people = []
        orgs = []
        exchanges = []
        companies = []
        for node in d["TOPICS"].childNodes:
            topics.append(node.wholeText)
        for node in d["PLACES"].childNodes:
            topics.append(node.wholeText)
        for node in d["PEOPLE"].childNodes:
            topics.append(node.wholeText)
        for node in d["ORGS"].childNodes:
            topics.append(node.wholeText)
        for node in d["EXCHANGES"].childNodes:
            topics.append(node.wholeText)
        for node in d["COMPANIES"].childNodes:
            topics.append(node.wholeText)

    line = title + "#" + ','.join(topics) + '#' + ','.join(places) + '#' + ','.join(people) + '#' + ','.join(orgs) + \
        '#' + ','.join(exchanges) + '#' + ','.join(companies) + '\n'
    # f.close()
    output.write(line)

output.close()
print("done")
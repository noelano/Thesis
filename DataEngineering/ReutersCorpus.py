from nltk.corpus import reuters

train = [x for x in reuters.fileids() if 'training' in x]
test = [x for x in reuters.fileids() if 'test' in x]

def makeData(file, set):
    labels = []
    f = open(file, "w")
    for doc in set:
        title = []
        label = reuters.categories(doc)[0]
        labels.append(label)
        for i in reuters.words(doc):
            if not i.isupper():
                break
            else:
                title.append(i)
        f.write(' '.join(title) + "\n")
    f.close()

    f = open("labels" + file, "w")
    f.write("\n".join(labels))
    f.close()

makeData('ReutersTraining.txt', train)
makeData('ReutersTest.txt', test)


import textmining

tdm = textmining.TermDocumentMatrix()

snippetsFile = "snippetsTrain.txt"
reutersFile = "reutersTrain.txt"

snippets = open(snippetsFile)
while True:
    doc = snippets.readline()
    if doc == '':
        print("Snippets complete")
        break
    else:
        doc = doc[:-1]
        tdm.add_doc(doc)

snippets.close()
print("Writing tdm to csv..")
tdm.write_csv('clean_snippets_tdm.csv', cutoff=1)
print("Done")

tdm = None
tdm = textmining.TermDocumentMatrix()

reuters = open(reutersFile)
while True:
    doc = reuters.readline()
    if doc == '':
        print("Reuters complete")
        break
    else:
        doc = doc[:-1]
        tdm.add_doc(doc)

reuters.close()
print("Writing tdm to csv..")
tdm.write_csv('clean_reuters_tdm.csv', cutoff=1)
print("Done")
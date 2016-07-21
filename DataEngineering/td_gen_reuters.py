import textmining

f = open("../DataEngineering/ReutersTraining.txt")
tdm = textmining.TermDocumentMatrix()
reuters = f.readlines()
f.close()
print(len(reuters))

for doc in reuters:
    tdm.add_doc(doc)

print("Writing tdm to csv..")
tdm.write_csv('reuters_tdm.csv', cutoff=1)
print("Done")

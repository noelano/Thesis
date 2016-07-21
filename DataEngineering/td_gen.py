import textmining, io
from nltk import word_tokenize
from nltk.corpus import stopwords

snippets = io.open("../../Datasets/data-web-snippets/train.txt", encoding="utf8")
tdm = textmining.TermDocumentMatrix()
labels = []

while True:
    doc = snippets.readline()
    if doc == '':
        print('EOF')
        break
    else:
        doc = doc[:-1]
        word_list = word_tokenize(doc)
        label = word_list.pop()
        labels.append(label)
        try:
            filtered_words = [word for word in word_list if word not in stopwords.words('english')]
        except:
            print(word_list)
            break
        doc = ' '.join(filtered_words)
        tdm.add_doc(doc)

snippets.close()
print("Writing tdm to csv..")
tdm.write_csv('snippets_tdm.csv', cutoff=1)
print("Done")

f = open("snippets_labels.txt", "w")
f.write('\n'.join(labels))
f.close()
import io, codecs
from nltk.corpus import stopwords
from nltk import word_tokenize

snippetCounts = "snippetCounts.txt"
reuterCounts = "reutersCounts.txt"

def removalWordList(dataset):
    """ Generate list of words to be removed """
    f = open(dataset)
    output_list = []
    while True:
        l = f.readline()
        if l == '':
            break
        else:
            bits = l.split(': ')
            if int(bits[1]) == 1:
                output_list.append(bits[0])
    f.close()
    return output_list

snippet_list = removalWordList(snippetCounts)
reuters_list = removalWordList(reuterCounts)

reuters_raw = "../ReutersTest.txt"
snippets_raw = "../../../Datasets/data-web-snippets/test.txt"

snippets_clean = "../CleanTrainingData/snippetsTest.txt"
reuters_clean = "../CleanTrainingData/reutersTest.txt"

stop = stopwords.words('english')
snippet_list += stop
reuters_list += stop

snippets = io.open(snippets_raw, encoding="utf8")
snippet_new = codecs.open(snippets_clean, "w", "utf-8")
while True:
    doc = snippets.readline()
    if doc == '':
        break
    else:
        word_list = word_tokenize(doc)
        label = word_list.pop()
        filtered_words = [word for word in word_list if word not in snippet_list]
        doc = ' '.join(filtered_words)
        snippet_new.write(doc + u'\n')
snippet_new.close()
snippets.close()
print("Snippets written")

reuters = io.open(reuters_raw, encoding="utf8")
reuters_new = open(reuters_clean, "w")
while True:
    doc = reuters.readline()
    if doc == '':
        break
    else:
        word_list = word_tokenize(doc)
        filtered_words = [word for word in word_list if word not in reuters_list]
        doc = ' '.join(filtered_words)
        reuters_new.write(doc + "\n")
reuters.close()
reuters_new.close()

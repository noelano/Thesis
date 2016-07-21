import json
from nltk.corpus import stopwords
from nltk import word_tokenize

f = open("../../Datasets/reuters-21578-master/reuters.json")
reuters = json.load(f)
f.close()

train_labels = []
test_labels = []
train = []
test = []

for doc in reuters:
    try:
        title = doc['title']
    except KeyError:
        continue

    try:
        topic = doc['topics'][0]
    except KeyError:
        continue

    try:
        split = doc['lewissplit']
    except KeyError:
        continue

    if len(title) < 5:
        continue

    title = title.replace("\n", ' ').replace("<", '').replace(">", '').replace(".", '').replace(',', '')
    title = title.replace('-', ' ').replace("\\", ' ').replace("/", '')
    try:
        title = title.lower()
    except AttributeError:
        print("Error: " + title)
    word_list = word_tokenize(title)
    filtered_words = [word for word in word_list if word not in stopwords.words('english')]
    for i in range(len(filtered_words)):
        word = filtered_words[i]
        word = word.replace('`', '').replace("'", '').replace('- ', '').replace(' -', '')
        if len(word) < 2:
            word = ''
        try:
            x = int(word)
            word = ''
        except ValueError:
            pass
        filtered_words[i] = word

    title = ' '.join(filtered_words)

    if split == 'TRAIN':
        train.append(title)
        train_labels.append(topic)
    else:
        test.append(title)
        test_labels.append(topic)

print("Total training: " + str(len(train)))
print("Total test: " + str(len(test)))

f = open("ReutersTraining.txt", "w")
f.write("\n".join(train))
f.close()

f = open("ReutersTest.txt", "w")
f.write("\n".join(test))
f.close()

f = open("labelsReutersTraining.txt", "w")
f.write("\n".join(train_labels))
f.close()

f = open("labelsReutersTest.txt", "w")
f.write("\n".join(test_labels))
f.close()

f = open("labelsReutersTraining.txt")
train = {}
while True:
    l = f.readline()
    if l == '':
        break
    else:
        label = l[:-1]
        if label not in train:
            train[label] = 1
        else:
            train[label] += 1
f.close()

print("Total training topics: " + str(len(train.keys())))

f = open("labelsReutersTest.txt")
test = {}
count = 0
while True:
    count += 1
    l = f.readline()
    if l == '':
        break
    else:
        label = l[:-1]
        if label not in test:
            test[label] = 1
        else:
            test[label] += 1
        if label not in train:
            print("Invalid label!!! Line number " + str(count))
f.close()

print("Total test topics: " + str(len(test.keys())))
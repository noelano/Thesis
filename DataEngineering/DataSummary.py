# Generate summary statistics for snippets dataset

#train = "../../Datasets/data-web-snippets/train.txt"
#test = "../../Datasets/data-web-snippets/test.txt"
train = "CleanTrainingData/snippetsTrain.txt"
test = "CleanTrainingData/snippetsTest.txt"

def getSummary(dataset):
    f = open(dataset)
    max = 0
    min = 200
    words = 0
    lines = 0

    while True:
        l = f.readline()
        if l == '':
            break
        else:
            doc = l.split(' ')
            count = len(doc)
            words += count

            if count > max:
                max = count
            if count < min:
                min = count

            lines += 1
    f.close()

    print("Longest doc: " + str(max))
    print("Shortes doc: " + str(min))
    print("Avg len: " + str(float(words - lines) / lines))

getSummary(train)
getSummary(test)

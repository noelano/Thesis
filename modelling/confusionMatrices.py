import pandas as pd

def makeConfusionMatrix(results_file, train_labels_file, test_labels_file, output_file):
    f = open(results_file)
    predictions = []
    s = []
    while True:
        l = f.readline()
        if l == '':
            break
        elif ']' in l:
            l = l[:-2].replace('[', '').replace(',', '').split(' ')
            l = [float(x) for x in l if len(x) > 0]
            s += l
            predictions.append(s)
            s = []
        else:
            l = l[:-1].replace('[', '').split(' ')
            l = [float(x) for x in l if len(x) > 0]
            s += l
    f.close()

    score = predictions.pop()

    f = open(train_labels_file)
    labels = f.readlines()
    f.close()

    indices = list(set(labels))
    indices = [label.replace("\n", '') for label in indices]

    f = open(test_labels_file)
    labels = f.readlines()
    f.close()

    conf = [[0 for i in indices] for i in indices]

    for i in range(len(labels)):
        label = labels[i].replace("\n", "")
        ind = indices.index(label)
        row = predictions[i]
        m = max(row)
        pred_ind = row.index(m)
        pred = indices[pred_ind]
        print ("Label: " + label + ", prediction: " + pred)
        conf[ind][pred_ind] += 1

    df = pd.DataFrame(data=conf, index=indices, columns=indices)
    df.to_csv(output_file)

if __name__ == "__main__":
    results = "NN_Results/TopPercentile/snippets_lda_0.310559006211_0.029_161_results.txt"
    #results = "NN_Results/fca_reuters_results.txt"
    #train_labels = "../DataEngineering/labelsReutersTraining.txt"
    #test_labels = "../DataEngineering/CleanTestData/labelsReutersTest.txt"
    #train_labels = "../ref_labels/labelsReutersTraining.txt"
    #test_labels = "../ref_labels/labelsReutersTest.txt"
    #train_labels = "../new_snippets_labels.txt"
    #test_labels = "../DataEngineering/CleanTestData/snippets_test_labels.txt"
    train_labels = "../ref_labels/new_snippets_labels.txt"
    test_labels = "../ref_labels/snippets_test_labels.txt"
    output = "NN_Results/ConfusionMatrices/Percentile/lda_snippets_confusion.csv"

    makeConfusionMatrix(results, train_labels, test_labels, output)
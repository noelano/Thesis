def mcNemar(model1, model2, labels):
    """
    Compute the McNemar statistic for two classification models
    :param model1: list of predictions from model 1
    :param model2: list of predictions from model 2
    :param labels: list of class labels
    :return: statistic value, degrees of freedom
    """
    n00 = 0
    n01 = 0
    n10 = 0
    n11 = 0

    df = min(len(model1), len(model2))
    for i in range(df):
        p1 = model1[i]
        p2 = model2[i]
        l = labels[i]

        if p1 == p2 and p1 == l:
            n11 += 1
        elif p1 == l:
            n01 += 1
        elif p2 == l:
            n10 += 1
        else:
            n00 += 1

    print n00, n01, n10, n11
    result = (abs(n01 - n10) - 1) ** 2 / float(n01 + n10)

    return result, df

def loadNNResults(input_file):
    f = open(input_file)
    predictions = []
    labels = f.readline()
    labels = labels[1:-2].replace("'", "").split(', ')
    #print(labels)
    s = []
    while True:
        l = f.readline()
        if l == '':
            break
        elif ']' in l:
            l = l[:-2].replace('[', '').replace(',', '').split(' ')
            l = [float(x) for x in l if len(x) > 0]
            s += l
            ind = l.index(max(l))
            predictions.append(labels[ind])
            s = []
        else:
            l = l[:-1].replace('[', '').split(' ')
            l = [float(x) for x in l if len(x) > 0]
            s += l
    f.close()

    return predictions


if __name__ == "__main__":
    m1 = "KMeans_Results/Percentile/snippets_fca_results.txt"
    m2 = "KMeans_Results/Percentile/snippets_lda_results.txt"
    label_file = "../ref_labels/snippets_test_labels.txt"   #labelsReutersTest; snippets_test_labels
    f = open(label_file)
    labels = f.readlines()
    labels = [x.replace("\n", "") for x in labels]
    f.close()
    f = open(m1)
    preds1 = f.readlines()
    preds1 = [x.replace("\n", "") for x in preds1]
    f.close()
    f = open(m2)
    preds2 = f.readlines()
    preds2 = [x.replace("\n", "") for x in preds2]
    f.close()

    preds1 = preds1[:929] + ["culture-arts-entertainment", "culture-arts-entertainment"] + preds1[930:1679] + ["health"] + preds1[1680:] + ["sports"]
    print(len(preds1))
    print(len(preds2))
    print(len(labels))
    #preds1 = loadNNResults(m1)
    #preds2 = loadNNResults(m2)

    print mcNemar(preds1, preds2, labels)


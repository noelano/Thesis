import pandas as pd

def resultsFromMatrix(confusion_matrix):
    total_records = sum(sum(confusion_matrix.values))

    precisions = []
    recalls = []
    fs = []

    for i in confusion_matrix.index:
        TP = confusion_matrix[i][i]
        FP = sum(confusion_matrix[i]) - TP
        FN = sum(confusion_matrix.loc[i]) - TP
        instances = sum(confusion_matrix.loc[i])

        if TP+FP != 0:
            precision = float(TP) / (TP + FP)
        else:
            precision = 0
        if TP+FN != 0:
            recall = float(TP) / (TP + FN)
        else:
            recall = 0
        if precision + recall != 0:
            f = 2 * precision * recall / float(precision + recall)
        else:
            f = 0

        precisions.append(instances * precision)
        recalls.append(instances * recall)
        fs.append(instances * f)

        print(i, precision, recall, f, instances)

    #total = float(len(confusion_matrix.columns))
    # NB this should be changed to only include the rows where there is an actual instance labelled with that class
    # The reuters data has a number of classes which aren't in fact present, leading to the averages being too small
    p = sum(precisions) / total_records
    r = sum(recalls) / total_records
    f = sum(fs) / total_records

    return p, r, f

if __name__ == "__main__":
    #input = "NN_Results/TopPercentile/snippets_lda_0.310559006211_0.029_161_results.csv"
    #input = "NN_Results/ConfusionMatrices/Correlations/fca_reuters_confusion.csv"
    input = "KMeans_Results/Correlations/snippets_fca_confusion.csv"

    df = pd.read_csv(input, index_col=0)
    #print(df.loc["sports"])
    #print(df["sports"])
    #print(df["sports"]["sports"])

    print(resultsFromMatrix(df))
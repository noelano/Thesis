import pandas as pd

def resultsFromMatrix(confusion_matrix):
    total_records = sum(confusion_matrix.all())

    precisions = []
    recalls = []
    fs = []

    for i in confusion_matrix.index:
        TP = confusion_matrix[i][i]
        FP = sum(confusion_matrix[i]) - TP
        FN = sum(confusion_matrix.loc[i]) - TP

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

        precisions.append(precision)
        recalls.append(recall)
        fs.append(f)

        print(i, precision, recall, f)

    cols = float(len(confusion_matrix.columns))
    p = sum(precisions) / cols
    r = sum(recalls) / cols
    f = sum(fs) / cols

    return p, r, f

if __name__ == "__main__":
    input = "NN_Results/fca_snippets_confusion.csv"

    df = pd.read_csv(input, index_col=0)
    #print(df.loc["sports"])
    #print(df["sports"])
    #print(df["sports"]["sports"])

    print(resultsFromMatrix(df))
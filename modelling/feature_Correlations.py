import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
sns.set(context="paper", font="monospace")

def corrHeatmap(file, index):
    if index:
        df =  pd.read_csv(file, index_col=0)
    else:
        df = pd.read_csv(file)
    corrmat = df.corr()

    fig = plt.figure(figsize=(12, 9))
    ax = sns.heatmap(corrmat, square=True)
    ax.set_xticklabels([])
    ax.set_yticklabels([])
    plt.show()
    # Set up the matplotlib figure
    #f, ax = plt.subplots(figsize=(12, 9))

    # Draw the heatmap using seaborn

def listCorrelatedFeatures(file, index):
    if index:
        df =  pd.read_csv(file, index_col=0)
    else:
        df = pd.read_csv(file)
    corrmat = df.corr().abs()

    s = corrmat.unstack()
    so = s.order(kind="quicksort")
    print(so[-100:-1])

def groupCorrelatedFeatures(file, index, threshold):
    if index:
        df =  pd.read_csv(file, index_col=0)
    else:
        df = pd.read_csv(file)
    corrmat = df.corr().abs()
    col_list = list(df.columns)

    correlated_features = {}
    for i in range(len(col_list)):
        col_1 = col_list[i]
        for j in range(i+1, len(col_list)):
            col_2 = col_list[j]
            if corrmat[col_1][col_2] >= threshold:
                if col_1 in correlated_features:
                    correlated_features[col_1].append(col_2)
                elif col_1 in correlated_features.values():
                    for key, value in correlated_features.items():
                        if value == col_2:
                            correlated_features[value].append(col_2)
                else:
                    correlated_features[col_1] = [col_2]

    return correlated_features

def alternateGroup(file, index, threshold):
    if index:
        df =  pd.read_csv(file, index_col=0)
    else:
        df = pd.read_csv(file)

    corrMatrix = df.corr().abs()

    corrMatrix.loc[:, :] = np.tril(corrMatrix, k=-1)

    already_in = set()
    result = []
    for col in corrMatrix:
        perfect_corr = corrMatrix[col][corrMatrix[col] >= threshold].index.tolist()
        if perfect_corr and col not in already_in:
            already_in.update(set(perfect_corr))
            perfect_corr.append(col)
            result.append(perfect_corr)

    return result


if __name__ == "__main__":
    from datetime import datetime
    #file = "../fca/reuters_new_tdm.csv"
    file = "../fca/snippets_new_tdm.csv"

    #corrHeatmap(file, 1)
    #listCorrelatedFeatures(file, 1)

    cols = groupCorrelatedFeatures(file, 1, 0.8)
    print(len(cols.keys()))
    for k in cols:
        print k, cols[k]

    cols = alternateGroup(file, 1, 0.8)
    print len(cols)
    for i in cols:
        print i

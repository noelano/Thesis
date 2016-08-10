from sklearn.cluster import KMeans
import pandas as pd
import datetime
import numpy as np
from elbow import *

train_file = "../fca/reuters_new_tdm.csv"
#test_file = ""

print("Start time: " + str(datetime.datetime.now()))
train = pd.read_csv(train_file, index_col=0)

print("Data loaded: " + str(datetime.datetime.now()))

elbow2(train, 1, 180, 10, "elbow_fca_reuters_sse3.png")
print("Modelling Complete: " + str(datetime.datetime.now()))
"""vocab = train.columns
s = ''
for i in range(len(vocab)):
    coeff = model.cluster_centers_[0][i]
    if coeff != 0:
      s += str(coeff) + '*' + vocab[i] + " + "
print s

label_file = "../DataEngineering/labelsReutersTraining.txt"
f = open(label_file)
labels = f.readlines()
f.close()
labels = labels[:2635] + labels[2635+1:]

cluster_labels = {}
label_dict = {}
for i in range(78):
    label_dict[i] = []
    cluster_labels[i] = []

for i in range(len(labels)):
    label_dict[model.labels_[i]].append(i)
    cluster_labels[model.labels_[i]].append(labels[i])

print("Evaluating clusters")
for l in cluster_labels[0]:
    print l
"""
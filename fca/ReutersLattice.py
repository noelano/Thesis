from FormalContext import Galois
import datetime
import pandas as pd
import numpy as np

input_file = "reuters_list.json"
print("Start time: " + str(datetime.datetime.now()))
reuters = Galois(input_file)
print("Lattice built: " + str(datetime.datetime.now()))
print(len(reuters.lattice))
print(len(reuters.concepts))

reuters.generateDistances()
print(reuters.distances.values)
print("Distances complete: " + str(datetime.datetime.now()))

max_sd = reuters.distances.values.max()
print(max_sd)

input = "../DataEngineering/CleanTrainingData/clean_reuters_tdm.csv"
f = open(input)
vocab = f.readline()
f.close()
vocab = vocab[:-1]
vocab = vocab.split(',')
vocab_leng = len(vocab)
prox_seed = [[0.0 for i in range(vocab_leng)] for i in range(vocab_leng)]
proximity_matrix = pd.DataFrame(data=prox_seed, columns=vocab, index=vocab)

for i in vocab:
    node_i = reuters.attributeLabels[i]
    for j in vocab:
        node_j = reuters.attributeLabels[j]
        proximity_matrix[i][j] = 1 - (float(reuters.distances[node_i][node_j]) / float(max_sd))

print(proximity_matrix)
print("Proximities complete: " + str(datetime.datetime.now()))

proximity_matrix.to_csv("reuters_proximities.csv")
TDM = pd.read_csv(input, delimiter=',')
# Change to decimal representation for TDM
TDM = TDM.div(TDM.sum(axis=1), axis=0)

# Ensure the column orders match before taking dot product
TDM.sort_index(axis=1)
proximity_matrix.sort_index(axis=1)
new_TDM = np.dot(TDM.values, proximity_matrix.values)

new_df = pd.DataFrame(data=new_TDM, columns=TDM.columns)
print("New TDM complete: " + str(datetime.datetime.now()))
new_df.to_csv("reuters_new_tdm.csv")

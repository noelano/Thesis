from sklearn.cluster import KMeans
import pandas as pd
from lda.lda_gen import ldaModel

def kmeansModelling(training, test):
    alpha = 0.0
    for n_topics in range(10, 100):
        while alpha < 0.5:
            Y = ldaModel(input, n_topics, alpha)
            model = KMeans()
            model.fit(Y.values)

def scoreModel():
    pass

if __name__ == "__main__":
    train = "../DataEngineering/CleanTrainingData/clean_reuters_tdm.csv"
    test = ""
    kmeansModelling(train, test)
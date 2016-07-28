import lda
import pandas as pd
import numpy as np

def ldaModel(input_tdm, n_topics, alpha, output_File=None, n_iter=2000):
    """
    Generate an LDA model for an input TDM file

    :param input_tdm: TDM file
    :param n_topics: number of topics to model
    :param alpha: the dirichlet prior. Float value between 0 and 1
    :param output_File: If supplied, write model to output file
    :param n_iter: number of iterations to run for
    :return: Term weights as a pandas dataframe
    """

    X = pd.read_csv(input_tdm, delimiter=',')
    model = lda.LDA(n_topics=n_topics, n_iter=n_iter, random_state=1, alpha=alpha)
    model.fit(X.values)

    Y = np.dot(model.doc_topic_, model.components_)
    Y = pd.DataFrame(data=Y)

    if output_File:
        Y.to_csv(output_File, index=False)

    return Y

if __name__ == "__main__":
    import datetime

    # Print start time
    print("Start time: " + str(datetime.datetime.now()))

    # Set input TDM file
    input = "../DataEngineering/CleanTrainingData/clean_reuters_tdm.csv"

    Y = ldaModel(input, 20)
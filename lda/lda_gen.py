import lda
import pandas as pd
import numpy as np

def ldaModel(X, n_topics, alpha, beta, output_File=None, n_iter=2000):
    """
    Generate an LDA model for an input TDM file

    :param input_tdm: TDM file
    :param n_topics: number of topics to model
    :param alpha: the dirichlet prior. Float value between 0 and 1
    :param output_File: If supplied, write model to output file
    :param n_iter: number of iterations to run for
    :return: Term weights as a pandas dataframe
    """

    model = lda.LDA(n_topics=n_topics, n_iter=n_iter, random_state=1, alpha=alpha, eta=beta)
    model.fit(X.values)

    Y = np.dot(model.doc_topic_, model.components_)
    Y = pd.DataFrame(data=Y)

    if output_File:
        Y.to_csv(output_File, index=False)

    return Y

def createLDAFiles(alphas, betas, input, topics, output):
    X = pd.read_csv(input, delimiter=',')
    for t in topics:
        a = 50.0 / t
        b = 0.029
        label = output + "_" + str(a) + "_" + str(b) + "_" + str(t) + ".csv"
        Y = ldaModel(X, t, a, b, output_File=label)

if __name__ == "__main__":
    import datetime

    # Print start time
    print("Start time: " + str(datetime.datetime.now()))

    # Set input TDM file
    input = "../clean_snippets_tdm.csv"

    topics = [81 + i for i in range(20)]
    alphas = [50]
    betas = [0.05]

    output = "Snippets/snippets_lda"

    createLDAFiles(alphas, betas, input, topics, output)
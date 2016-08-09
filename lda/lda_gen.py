import lda
import pandas as pd
import numpy as np

def ldaModel(X_train, X_test, n_topics, alpha, beta, logger, output_File=None, n_iter=2000):
    """
    Generate an LDA model for an input TDM file

    :param input_tdm: TDM file
    :param n_topics: number of topics to model
    :param alpha: the dirichlet prior. Float value between 0 and 1
    :param output_File: If supplied, write model to output file
    :param n_iter: number of iterations to run for
    :return: Term weights as a pandas dataframe
    """

    cols = X_train.columns[:]
    model = lda.LDA(n_topics=n_topics, n_iter=n_iter, random_state=1, alpha=alpha, eta=beta)
    model.fit(X_train.values)

    score = str(model.loglikelihood())
    print ("Log likelihood: " + score)
    logger.write(str(n_topics) + ": " + score + "\n")

    Y = np.dot(model.doc_topic_, model.components_)
    Y = pd.DataFrame(data=Y, columns=cols)

    test_dist = model.transform(X_test.values)

    Y_test = np.dot(test_dist, model.components_)
    Y_test = pd.DataFrame(data=Y_test, columns=cols)

    if output_File:
        Y.to_csv(output_File + ".csv", index=False)
        Y_test.to_csv(output_File + "_test.csv", index=False)

    return Y


def perplexity(theta, phi, docs):
    if docs == None: return
    log_per = 0
    N = 0
    for m, doc in enumerate(docs):
        for w in doc:
            log_per -= np.log(np.inner(phi[:, w], theta))
        N += len(doc)
    return np.exp(log_per / N)

def createLDAFiles(alphas, betas, train_input, test_input, topics, output, logger):
    X_train = pd.read_csv(train_input, delimiter=',')
    X_test = pd.read_csv(test_input, delimiter=',', index_col=0)
    for t in topics:
        a = 50.0 / t
        #b = 0.05
        b = 0.029
        label = output + "_" + str(a) + "_" + str(b) + "_" + str(t)
        Y = ldaModel(X_train, X_test, t, a, b, output_File=label, logger=logger)

if __name__ == "__main__":
    import datetime

    # Print start time
    print("Start time: " + str(datetime.datetime.now()))

    # Set input TDM file
    input = "../clean_snippets_tdm.csv"
    test = "../DataEngineering/CleanTestData/snippets_tdm.csv"

    #topics = [1 + i for i in range(0, 150, 5)]
    topics = [161]
    alphas = [50]
    betas = [0.05]

    output = "Snippets/snippets_lda"
    logger = open("Snippets/log_likelihoods2.txt", "w")

    createLDAFiles(alphas, betas, input, test, topics, output, logger)
    logger.close()

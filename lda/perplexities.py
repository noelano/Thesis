from sklearn.decomposition import LatentDirichletAllocation
import pandas as pd
import matplotlib.pyplot as plt

#train_input = "../clean_snippets_tdm.csv"
#test_input = "../DataEngineering/CleanTestData/snippets_tdm.csv"

train_input = "../DataEngineering/CleanTrainingData/clean_reuters_tdm.csv"
test_input = "../DataEngineering/CleanTestData/reuters_tdm.csv"

X_train = pd.read_csv(train_input, delimiter=',')
#X_train.drop(X_train.index[[2635]], inplace=True)
#X_train = X_train.div(X_train.sum(axis=1), axis=0)
X_test = pd.read_csv(test_input, delimiter=',', index_col=0)
#X_test = X_test[(X_test.T != 0).any()]
#X_test = X_test.div(X_test.sum(axis=1), axis=0)

print("Data loaded")

topic_nums = [i for i in range(1, 250, 5)]
perplexities = []

for t in topic_nums:
    a = 50.0 / t
    #b = 0.029
    b = 0.05
    lda = LatentDirichletAllocation(n_topics=t, max_iter=5,
                                    learning_method='batch',
                                    random_state=0,
                                    doc_topic_prior=a,
                                    topic_word_prior=b)

    lda.fit(X_train.values)

    test_gamma = lda.transform(X_test)
    perp = lda.perplexity(X_test, test_gamma)
    perplexities.append(perp)
    print(t, perp)

perp_rates = []
for i in range(1, len(perplexities)):
    rpc = abs((perplexities[i] - perplexities[i-1]) / (topic_nums[i] - topic_nums[i-1]))
    perp_rates.append(rpc)

fig = plt.figure()
ax = fig.add_subplot(111)
ax.plot(topic_nums, perplexities, 'b*-')
plt.grid(True)
plt.xlabel('Number of topics')
plt.ylabel('Perplexities')
#plt.title('Elbow for KMeans clustering')
#plt.savefig(filename)
plt.show()

fig = plt.figure()
ax = fig.add_subplot(111)
ax.plot(topic_nums[1:], perp_rates, 'b*-')
plt.grid(True)
plt.xlabel('Number of topics')
plt.ylabel('RPC values')
plt.show()
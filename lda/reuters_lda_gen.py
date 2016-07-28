import numpy as np
import lda
import matplotlib.pyplot as plt
import datetime
import pandas as pd

try:
    plt.style.use('ggplot')
except:
    # version of matplotlib might not be recent
    pass

# Print start time
print("Start time: " + str(datetime.datetime.now()))

# Set input TDM file
input = "../DataEngineering/CleanTrainingData/clean_reuters_tdm.csv"

# Load header row and tdm
f = open(input)
vocab = f.readline()
f.close()

#X = np.loadtxt(input, delimiter=',', skiprows=1)
X = pd.read_csv(input, delimiter=',')
print("Input TDM loaded")
print("Time: " + str(datetime.datetime.now()))

# Number of topics to generate.
# Since there are 10 classes we'll start with double this as the initial topic number
n_topics = 20

# Fit an LDA model to the tdm
print("Fitting model to TDM...")
model = lda.LDA(n_topics=n_topics, n_iter=2000, random_state=1)
model.fit(X.values)
print("Done")
print("Time: " + str(datetime.datetime.now()))

# Generate the doc - word model
Y = np.dot(model.doc_topic_, model.components_)
Y = pd.DataFrame(data=Y)

# Save for future use
Y.to_csv("snippets_lda.csv", index=False)
print("Generated model written to csv")
print("Time: " + str(datetime.datetime.now()))


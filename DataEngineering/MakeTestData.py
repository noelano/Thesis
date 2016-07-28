import pandas as pd

"""
Using pandas, load the training TDM to get the correct word headers
For each document in the test set, check if each word appears in this list
If it does, increment the corresponding vector component by 1
"""

# Update variables with correct filenames
tdm_file = "CleanTrainingData/clean_snippets_tdm.csv"
test_file = "CleanTrainingData/snippetsTest.txt"
output = "CleanTestData/snippets_test_tdm.csv"

# Load the existing TDM so that the test TDM can be built with the same columns
TDM = pd.read_csv(tdm_file)
Test_TDM = pd.DataFrame(columns=TDM.columns)
vocab = list(TDM.columns)
feature_size = len(vocab)
TDM = None
print("TDM loaded. Checking test file..")

# Loop over documents in the test file, adding the correct vector repn at each step
f = open(test_file)
index = 0
while True:
    l = f.readline()
    if l == '':
        break
    else:
        l = l[:-1]
        words = l.split(' ')
        words.pop()
        Test_TDM.loc[index] = [0 for i in range(feature_size)]
        for word in words:
            if word in vocab:
                Test_TDM[word][index] += 1
    index += 1
    if index % 100 == 0:
        print(str(index) + " documents checked")
f.close()

print("Test TDM generated")

Test_TDM.to_csv(output, index=False, header=False)
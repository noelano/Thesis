from keras.models import Sequential
from keras.layers import Dense, Dropout
import pandas as pd

train_file = "../fca/snippets_new_tdm.csv"
test_file = "../DataEngineering/CleanTestData/snippets_tdm.csv"

train = pd.read_csv(train_file, delimiter=',', index_col=0)
col_len = len(train.columns)

X_train = train.values

f = open("../DataEngineering/snippets_labels.txt")
labels = f.readlines()
f.close()

indices = list(set(labels))
y_train = [[0 for i in range(8)] for i in range(len(labels))]

# Set the y_train vectors to have a 1 for the corresponding label
for i in range(len(labels)):
    ind = indices.index(labels[i])
    y_train[i][ind] = 1

test = pd.read_csv(test_file, delimiter=',', index_col=0)

X_test = test.values

f = open("../DataEngineering/CleanTestData/snippets_test_labels.txt")
labels = f.readlines()
f.close()

indices = list(set(labels))
y_test = [[0 for i in range(8)] for i in range(len(labels))]

# Set the y_train vectors to have a 1 for the corresponding label
for i in range(len(labels)):
    ind = indices.index(labels[i])
    y_test[i][ind] = 1

model = Sequential()
model.add(Dense(col_len, input_dim=20, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(col_len, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(8, activation='softmax'))

model.compile(loss='categorical_crossentropy',
              optimizer='adadelta',
              metrics=['accuracy'])

model.fit(X_train, y_train,
          nb_epoch=20)

y_pred = model.predict(X_test)

f = open("Snippets_Results.txt", "w")
f.write(str(y_pred))
f.write("\n")

score = model.evaluate(X_test, y_test)

f.write(str(score))
f.close()

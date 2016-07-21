import pandas as pd

reuters = "reuters_ctxt.csv"
snippets = "snippets_ctxt.csv"

#r = pd.read_csv(reuters, delimiter=',', skiprows=1)
s = open(reuters)

words = s.readline()[1:-1].split(',')
word_len = len(words)
print(word_len)

counts = [0 for i in range(word_len)]

while True:
    l = s.readline()
    if l == '':
        print("All docs checked")
        break
    else:
        l = l[:-1]
        doc = l.split(',')

        for i in range(1, word_len + 1):
            if doc[i] == "X":
                counts[i - 1] += 1

s.close()

total = 0
f = open("reutersCounts.txt", "w")
for i in range(word_len):
    if counts[i] == 1:
        total += 1
        print(words[i])
    f.write(words[i] + ": " + str(counts[i]) + "\n")
f.close()
print("Total single doc words: " + str(total))
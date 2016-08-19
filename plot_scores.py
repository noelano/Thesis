import matplotlib.pyplot as plt
import numpy as np
import colormaps as cmaps
#plt.set_cmap('viridis')

p = [0.017, 0.22, 0.059, 0.53, 0.001, 0.05, 0.15, 0.48]
r = [0.13, 0.2, 0.13, 0.35, 0.009, 0.12, 0.31, 0.54]
f = [0.03, 0.2, 0.08, 0.34, 0.002, 0.0071, 0.19, 0.49]

N = 8
ind = np.arange(N)  # the x locations for the groups
width = 0.28       # the width of the bars

fig, ax = plt.subplots()
plt.legend(loc="upper left")
rects1 = ax.bar(ind, p, width, color=(0.26700400000000002, 0.0048739999999999999, 0.32941500000000001, 1.0))
#rects2 = ax.bar(ind + width, r, width, color=(0.26700400000000002, 0.0048739999999999999, 0.32941500000000001, 0.6))
#rects3 = ax.bar(ind + 2*width, f, width, color=(0.26700400000000002, 0.0048739999999999999, 0.32941500000000001, 0.2))
rects2 = ax.bar(ind + width, r, width, color=(0.13506599999999999, 0.54485300000000003, 0.55402899999999999, 1.0))
rects3 = ax.bar(ind + 2*width, f, width, color=(0.99324800000000002, 0.90615699999999999, 0.14393600000000001, 1.0))

ax.set_ylabel('Scores')
ax.set_xlabel('Model')
#ax.set_title('Scores by group and gender')
ax.set_xticks(ind + 1.5*width)
ax.set_xticklabels(('M1', 'M2', 'M3', 'M4', 'M5', 'M6', 'M7', 'M8'))
#ax.set_xticklabels(('Snippets-NN-FCA', 'Snippets-NN-LDA', 'Snippets-Kmeans-FCA', 'Snippets-Kmeans-LDA', 'Reuters-NN-FCA', 'Reuters-NN-LDA', 'Reuters-Kmeans-FCA', 'Reuters-Kmeans-LDA'), rotation='vertical')

ax.legend((rects1[0], rects2[0], rects3[0]), ('Precision', 'Recall', 'F-score'), loc="upper left")

plt.show()

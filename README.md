# Thesis
Code snippets used in experiments for thesis on comparing FCA and LDA for short-text classification.

Includes data pre-processing:
- Data cleanup, case conversion, removing stop words, punctutation and words in just one doc.
- Splitting between train and test sets
- Removal of class labels
- TDM generation

FCA:
- Implementation of concept lattice class
- Takes json concepts as input and generates a lattice
- Computes proximites between all concept pairs and returns as pandas dataframe

LDA:
- Uses lda package to generate topic models
- Multiple iterations run with different topic numbers
- Plot of perplexities from each model

Modelling:
- K-means using sklearn
- Neural Networks in keras

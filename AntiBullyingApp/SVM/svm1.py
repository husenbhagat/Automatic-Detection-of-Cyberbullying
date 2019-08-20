import sklearn.datasets
import sklearn.metrics
import sklearn.cross_validation
import sys
import os
import glob
import scipy.sparse as sp
import sklearn.feature_extraction.text
import sklearn.svm
from sklearn.feature_extraction.text import TfidfVectorizer

def bagOfWords(files_data):
	count_vector = sklearn.feature_extraction.text.CountVectorizer()
	return count_vector.fit_transform(files_data)

clf = sklearn.svm.LinearSVC()

training_files = sklearn.datasets.load_files("dataset_training")

#print training_files.data

predict_files = sklearn.datasets.load_files("dataset_prediction")

print predict_files.data

vectorizer = TfidfVectorizer(encoding='latin1')
X_t = vectorizer.fit_transform((open(f).read()
for f in training_files.filenames))
print("n_samples: %d, n_features: %d" % X_t.shape)
assert sp.issparse(X_t)


X_p = vectorizer.transform((open(f).read()
for f in predict_files.filenames))




'''
word_counts_t = bagOfWords(training_files.data)
tf_transformer_t = sklearn.feature_extraction.text.TfidfTransformer(use_idf=True).fit(word_counts_t)
X_t = tf_transformer_t.transform(word_counts_t)

word_counts_p = bagOfWords(predict_files.data)
tf_transformer_p = sklearn.feature_extraction.text.TfidfTransformer(use_idf=True).fit(word_counts_p)
X_p = tf_transformer_p.transform(word_counts_p)
'''

clf.fit(X_t, training_files.target)
y_predicted = clf.predict(X_p)

print y_predicted



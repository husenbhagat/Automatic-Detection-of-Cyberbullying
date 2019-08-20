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
from sklearn.metrics import precision_recall_fscore_support,accuracy_score

clf = sklearn.svm.LinearSVC()

training_files = sklearn.datasets.load_files("/home/ubuntu/Desktop/SVM/dataset_training")

#print training_files.data

predict_files = sklearn.datasets.load_files("/home/ubuntu/Desktop/SVM/dataset_prediction")

print "Predict",predict_files.data

vectorizer = TfidfVectorizer(encoding='utf-8')
X_t = vectorizer.fit_transform((open(f).read() for f in training_files.filenames))
print("n_samples: %d, n_features: %d" % X_t.shape)
assert sp.issparse(X_t)




X_p = vectorizer.transform((open(f).read()
for f in predict_files.filenames))


clf.fit(X_t, training_files.target)
y_predicted=""
y_predicted = clf.predict(X_p)

print y_predicted
if y_predicted[0]==0:
	f1=open("out.txt",'w')
	f1.write("0")
	f1.close()
else:
	f1=open("out.txt",'w')
	f1.write("1")
	f1.close()
#print sklearn.SVM.LinearSVC.score(X_p,predict_files.target)

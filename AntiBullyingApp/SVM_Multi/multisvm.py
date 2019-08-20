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
from sklearn.multiclass import OneVsOneClassifier
from sklearn.svm import LinearSVC



clf = sklearn.svm.LinearSVC()

training_files = sklearn.datasets.load_files("/../../../SVM_Multi/dataset_training")

	#print training_files.data

predict_files = sklearn.datasets.load_files("/../../../SVM/dataset_prediction")

print "Predict",predict_files.data

vectorizer = TfidfVectorizer(encoding='utf-8')
X_t = vectorizer.fit_transform((open(f).read() for f in training_files.filenames))
print("n_samples: %d, n_features: %d" % X_t.shape)
assert sp.issparse(X_t)
	
	


X_p = vectorizer.transform((open(f).read() for f in predict_files.filenames))
	
y= OneVsOneClassifier(LinearSVC(random_state=0)).fit(X_t,training_files.target).predict(X_p)	
print y[0]
if y[0]==0:
	f1=open("/../../../SVM/out.txt",'w')
	f1.write("0")
	f1.close()
elif y[0]==1:
	f1=open("/../../../SVM/out.txt",'w')
	f1.write("1")
	f1.close()
elif y[0]==2:
	f1=open("/../../../SVM/out.txt",'w')
	f1.write("2")
	f1.close()

from django.shortcuts import render,redirect
from django import forms
from django.http import HttpResponseRedirect
from .forms import TextForm 
from sklearn.multiclass import OneVsOneClassifier
from sklearn.svm import LinearSVC
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
import csv
from django.shortcuts import render_to_response
from django.http import HttpResponse
import random

# Create your views here.


def tweet_dict(twitterData):  
    twitter_list_dict = []
    twitterfile = open(twitterData)
    twitterreader = csv.reader(twitterfile)
    for line in twitterreader:
        twitter_list_dict.append(line[0])
    return twitter_list_dict
    
def sentiment_dict(sentimentData):
    afinnfile = open(sentimentData)
    scores = {} # initialize an empty dictionary
    for line in afinnfile:
        term, score  = line.split("\t")  # The file is tab-delimited. "\t" means "tab character"
        scores[term] = float(score)  # Convert the score to an integer.
       
    return scores # Print every (term, score) pair in the dictionary


def home(request):
    return render(request,'home.html',{})
def chart(request):
	directory = '/home/ubuntu/Desktop/SVM/dataset_training/bully'
	number_of_files = len([item for item in os.listdir(directory) if os.path.isfile(os.path.join(directory, item))])
	flb= number_of_files
	directory = '/home/ubuntu/Desktop/SVM/dataset_training/nonbully'
	number_of_files = len([item for item in os.listdir(directory) if os.path.isfile(os.path.join(directory, item))])
	flt= number_of_files
	return render(request,'doughnut.html',{'tweets':flt,'bully':flb})

def dashboard(request):
	directory = '/home/ubuntu/Desktop/SVM/dataset_training/bully'
	number_of_files = len([item for item in os.listdir(directory) if os.path.isfile(os.path.join(directory, item))])
	flb= number_of_files
	directory = '/home/ubuntu/Desktop/SVM/dataset_training/nonbully'
	number_of_files = len([item for item in os.listdir(directory) if os.path.isfile(os.path.join(directory, item))])
	flt=flb+number_of_files
	lines1=[]
	with open("/home/ubuntu/Desktop/SVM/delete.txt") as f1:
		for m1 in f1:
                	lines1.append(m1.strip('\n').strip(" "))
	
	return render(request,'dashboard.html',{'tweets':flt,'bully':flb,'participants':100,'mis':340,'text':lines1})
   
def form(request):
	if request.method=="POST":
		form=TextForm(request.POST)
		if form.is_valid():
			text=form.cleaned_data['text']
			form.save(commit=True)
			return index(request)
	else :
		form=TextForm()
	#print request.POST.get('text')
	lines = []
	lines1 = []
	with open("/home/ubuntu/Desktop/SVM/data_print") as f:
		for m in f:
                	lines.append(m.strip('\n').strip(" "))
	with open("/home/ubuntu/Desktop/SVM/optional_data_print") as f1:
		for m1 in f1:
                	lines1.append(m1.strip('\n').strip(" "))
	
	return render(request,'form.html',{'form':lines,'form1':lines1})


def return_data(request):
	clf = sklearn.svm.LinearSVC()

	training_files = sklearn.datasets.load_files("/home/ubuntu/Desktop/SVM/dataset_training")
	f=open("/home/ubuntu/Desktop/SVM/dataset_prediction/test/lol.txt",'w')
	fil=open("/home/ubuntu/Desktop/SVM/data_print",'a')
	fil.write("\n")
	text=request.POST.get('text')
	
	fil.close()
	f.write(text)
	f.close()
	#print "Text ",text
	
	#print training_files.data

	predict_files = sklearn.datasets.load_files("/home/ubuntu/Desktop/SVM/dataset_prediction")

	#print "Predict",predict_files.data

	vectorizer = TfidfVectorizer(encoding='utf-8')
	X_t = vectorizer.fit_transform((open(f).read() for f in training_files.filenames))
	#print("n_samples: %d, n_features: %d" % X_t.shape)
	assert sp.issparse(X_t)



	X_p = vectorizer.transform((open(f).read() for f in predict_files.filenames))

	#print X_p
	clf.fit(X_t, training_files.target)
	y_predicted=""
	y_predicted = clf.predict(X_p)
	#print "OUT",y_predicted
	if y_predicted[0]==0:
		
		f1=open("/home/ubuntu/Desktop/SVM_Multi/dataset_prediction/test/lol.txt",'w')
		f1.write(text)
		f1.close()
		cn=0
		with open("/home/ubuntu/Desktop/SVM/pande.txt") as f:
			#print "HOLA1",text
			for line in f:
				#print "HOLA2", line
			
				if (text == line.strip("\n")):
					#print "HOLA3"
					#print line
					cn=1
		if (cn==0):
			num=random.randint(0,100000000)
			fl=open("/home/ubuntu/Desktop/SVM/dataset_training/bully/"+str(num)+".txt",'w')
			fl.write(text)
			fl.close()
			f3 = open("/home/ubuntu/Desktop/SVM/pande.txt",'a')
			f3.write("\n"+text)
			f3.close()
			
			fl=open("/home/ubuntu/Desktop/SVM_Multi/dataset_prediction/lol.txt",'w')
			fl.write(text)
			fl.close()
			
			clf = sklearn.svm.LinearSVC()

			training_files = sklearn.datasets.load_files("/home/ubuntu/Desktop/SVM_Multi/dataset_training")

	#print training_files.data

			predict_files = sklearn.datasets.load_files("/home/ubuntu/Desktop/SVM/dataset_prediction")


			vectorizer = TfidfVectorizer(encoding='utf-8')
			X_t = vectorizer.fit_transform((open(f).read() for f in training_files.filenames))
			assert sp.issparse(X_t)
	
	


			X_p = vectorizer.transform((open(f).read() for f in predict_files.filenames))
	
			y= OneVsOneClassifier(LinearSVC(random_state=0)).fit(X_t,training_files.target).predict(X_p)	
			if (y[0]==0):
				num=random.randint(0,100000000)
				fl=open("/home/ubuntu/Desktop/SVM_Multi/dataset_training/1/"+str(num)+".txt",'w')
				fl.write(text)
				fl.close()
		
			elif (y[0]==1):
				num=random.randint(0,100000000)
				fl=open("/home/ubuntu/Desktop/SVM_Multi/dataset_training/2/"+str(num)+".txt",'w')
				fl.write(text)
				fl.close()
			elif (y[0]==2):
				num=random.randint(0,100000000)
				fl=open("/home/ubuntu/Desktop/SVM_Multi/dataset_training/3/"+str(num)+".txt",'w')
				fl.write(text)
				fl.close()


		
		os.system("rm /home/ubuntu/Desktop/SVM_Multi/dataset_prediction/test/lol.txt~")
		clf = sklearn.svm.LinearSVC()

		training_files = sklearn.datasets.load_files("/home/ubuntu/Desktop/SVM_Multi/dataset_training")

		#print training_files.data

		predict_files = sklearn.datasets.load_files("/home/ubuntu/Desktop/SVM_Multi/dataset_prediction")

		#print "Predict",predict_files.data

		vectorizer = TfidfVectorizer(encoding='utf-8')
		X_t = vectorizer.fit_transform((open(f).read() for f in training_files.filenames))
		#print("n_samples: %d, n_features: %d" % X_t.shape)
		assert sp.issparse(X_t)
	
	


		X_p = vectorizer.transform((open(f).read()
		for f in predict_files.filenames))
		y1=OneVsOneClassifier(LinearSVC(random_state=0)).fit(X_t,training_files.target).predict(X_p)
		#print y1
		if y1==0:
			fil=open("/home/ubuntu/Desktop/SVM/optional_data_print",'a')
			fil.write(text)
			fil.write("\n")
			fil.close()
		
			return render(request,'output.html',{'pred':"100 friends will view this post. Our system has detected harmful content which might hurt the users sentiments.Are you sure you want to post this ?",'val':True,'text':text,'l':False})
		elif y1==1:
			return render(request,'output.html',{'pred':"You have been temporarily banned till the moderator checks this post.Our system has detected harmful content which might hurt the users sentiments. You cannot post another message until then. You can still continue to surf. You will be redirected to depression chat room for online help.  ",'val':False,'l':True})
		elif y1==2:
			return render(request,'output.html',{'pred':"Our system has detected some very harmful content in your post which might hurt the users sentiments. Keeping this in mind your posting privileges have been suspended for a week . You cannot post another message until then. You can still continue to surf. Repeated posting of such highly offensive content will lead to a report being generated and sent to the concerned authorities. You will be redirected to depression chat room for online help.",'val':False,'l':True})
	else:
		tweets = tweet_dict("/home/ubuntu/Desktop/SVM/dataset_prediction/test/lol.txt")
    		sentiment = sentiment_dict("/home/ubuntu/Desktop/SentiNet/AFINN-111.txt")
    
    		for index in range(len(tweets)):
        
    		    tweet_word = tweets[index].split()
    		    sent_score = 0 # sentiment score della frase

        
    		    for word in tweet_word:
            			word = word.rstrip('?:!.,;"!@')
            			word = word.replace("\n", "")
          
            			if not (word.encode('utf-8', 'ignore') == ""):
                			if word.encode('utf-8') in sentiment.keys():
                	    			sent_score = sent_score + float(sentiment[word])
                    


        	#print tweets[index] + " --- "+ str(sent_score)
		#print str(sent_score)
		if (sent_score < 0):
			f1=open("/home/ubuntu/Desktop/SVM_Multi/dataset_prediction/test/lol.txt",'w')
			f1.write(text)
			f1.close()
			cn=0
			with open("/home/ubuntu/Desktop/SVM/pande.txt") as f:
				#print "HOLA1",text
				for line in f:
					#print "HOLA2", line
			
					if (text == line.strip("\n")):
						#print "HOLA3"
						#print line
						cn=1
			if (cn==0):
				num=random.randint(0,100000000)
				fl=open("/home/ubuntu/Desktop/SVM/dataset_training/bully/"+str(num)+".txt",'w')
				fl.write(text)
				fl.close()
				f3 = open("/home/ubuntu/Desktop/SVM/pande.txt",'a')
				f3.write("\n"+text)
				f3.close()
			
				fl=open("/home/ubuntu/Desktop/SVM_Multi/dataset_prediction/lol.txt",'w')
				fl.write(text)
				fl.close()
			
				clf = sklearn.svm.LinearSVC()

				training_files = sklearn.datasets.load_files("/home/ubuntu/Desktop/SVM_Multi/dataset_training")

		#print training_files.data

				predict_files = sklearn.datasets.load_files("/home/ubuntu/Desktop/SVM/dataset_prediction")


				vectorizer = TfidfVectorizer(encoding='utf-8')
				X_t = vectorizer.fit_transform((open(f).read() for f in training_files.filenames))
				assert sp.issparse(X_t)
	
	


				X_p = vectorizer.transform((open(f).read() for f in predict_files.filenames))
	
				y= OneVsOneClassifier(LinearSVC(random_state=0)).fit(X_t,training_files.target).predict(X_p)	
				if (y[0]==0):
					num=random.randint(0,100000000)
					fl=open("/home/ubuntu/Desktop/SVM_Multi/dataset_training/1/"+str(num)+".txt",'w')
					fl.write(text)
					fl.close()
		
				elif (y[0]==1):
					num=random.randint(0,100000000)
					fl=open("/home/ubuntu/Desktop/SVM_Multi/dataset_training/2/"+str(num)+".txt",'w')
					fl.write(text)
					fl.close()
				elif (y[0]==2):
					num=random.randint(0,100000000)
					fl=open("/home/ubuntu/Desktop/SVM_Multi/dataset_training/3/"+str(num)+".txt",'w')
					fl.write(text)
					fl.close()

			os.system("rm /home/ubuntu/Desktop/SVM_Multi/dataset_prediction/test/lol.txt~")
			clf = sklearn.svm.LinearSVC()

			training_files = sklearn.datasets.load_files("/home/ubuntu/Desktop/SVM_Multi/dataset_training")

			#print training_files.data

			predict_files = sklearn.datasets.load_files("/home/ubuntu/Desktop/SVM_Multi/dataset_prediction")

			#print "Predict",predict_files.data

			vectorizer = TfidfVectorizer(encoding='utf-8')
			X_t = vectorizer.fit_transform((open(f).read() for f in training_files.filenames))
			#print("n_samples: %d, n_features: %d" % X_t.shape)
			assert sp.issparse(X_t)
	
	


			X_p = vectorizer.transform((open(f).read()
			for f in predict_files.filenames))
			y1=OneVsOneClassifier(LinearSVC(random_state=0)).fit(X_t,training_files.target).predict(X_p)
			#print y1
			if y1==0:
				fil=open("/home/ubuntu/Desktop/SVM/optional_data_print",'a')
				fil.write(text)
				fil.write("\n")
				fil.close()
			
				return render(request,'output.html',{'pred':"100 friends will view this post. Our system has detected harmful content which might hurt the users sentiments.Are you sure you want to post this ?",'val':True,'text':text,'l':False})
			elif y1==1:
				return render(request,'output.html',{'pred':"You have been temporarily banned till the moderator checks this post.Our system has detected harmful content which might hurt the users sentiments. You cannot post another message until then. You can still continue to surf. You will be redirected to depression chat room for online help.",'val':False,'l':True})
			elif y1==2:
				return render(request,'output.html',{'pred':"Our system has detected some very harmful content in your post which might hurt the users sentiments. Keeping this in mind your posting privileges have been suspended for a week . You cannot post another message until then. You can still continue to surf. Repeated posting of such highly offensive content will lead to a report being generated and sent to the concerned authorities. You will be redirected to depression chat room for online help.",'val':False,'l':True})
		else:
			fil=open("/home/ubuntu/Desktop/SVM/data_print",'a')
			fil.write(text)
			fil.close()
		return HttpResponseRedirect("http://127.0.0.1:8000/home/form/")
		#return render(request,'output.html',{'pred':"Dont be a noob",'val':0})

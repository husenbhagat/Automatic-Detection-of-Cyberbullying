import numpy as np
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.svm import LinearSVC
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.multiclass import OneVsRestClassifier

X_train = np.array(["  Fuck Justin bieber. He&#039;s a fucking fag    UM excuse yuh? HE IS NOT!! Ur a fuckin idiot! Kay? good",
                    "Hahah. Funny how u defend that beiber kid. its also funny how u stalked my whole twitter! Nice goin! BITCH!",
                    "Hey. Why you such a bitch?",
                    "Now how the fuck am i suppose to remember that? Weirdo! maybe it was ur moms dick? lOL!",
                    "you are fake though :D ? that makes no sense lolol why would you keep faking all these formsprings  your stuuupid :p we all know the real ashlee girls formspring already  soo fuck off may you?",
                    "lol how cute u have friends that back u up :] doesnt matter. ur still a fake bitch :] go find a real bf. not someone out of ur league. lol ugly ass    wow yeahh im a fake bitch yuur thee onee thatss scaredd to sayy all thiiss shitt in myy face.bitchh..!scard too gett fuckedd uuppp...!?!?! yurr reall funny skinny ass bitchh",
                    "Do you believe theres intelligent life on other planets?",
                    " Do you have any favorite YouTube star?",
                    "Hey how are you",
                    "How are you doing today",
                    "Is sure is sunny here isnt it",
                    "I like living in london",
                    ])
y_train = [[0],[0],[0],[0],[0],[0],[1],[1],[1],[1],[1],[1]]
X_test = np.array(['the weather is great today',
                   'sammy is a fat cow moo bitch',
                   ])   
target_names = ['Bully', 'Non-bully']

classifier = Pipeline([
    ('vectorizer', CountVectorizer(min_n=1,max_n=2)),
    ('tfidf', TfidfTransformer()),
    ('clf', OneVsRestClassifier(LinearSVC()))])
classifier.fit(X_train, y_train)
predicted = classifier.predict(X_test)
for item, labels in zip(X_test, predicted):
    print '%s => %s' % (item, ', '.join(target_names[x] for x in labels))

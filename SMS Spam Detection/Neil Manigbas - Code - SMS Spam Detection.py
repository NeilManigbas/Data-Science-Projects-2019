import pandas as pd
import nltk
nltk.download()
import re
from nltk.stem import PorterStemmer, WordNetLemmatizer
from nltk.tokenize import WhitespaceTokenizer
from nltk.corpus import stopwords

df=pd.read_table('SMSSpamCollection.tsv',names=['y','x'])

# checking dataset
df.describe()
df.shape
df.isnull().sum()
df.info()
df.y.unique() # ham, spam

# parameters
tokenizer=WhitespaceTokenizer()
ps=PorterStemmer()
wnl=WordNetLemmatizer()

stopwords_set = set(stopwords.words('english'))
corpus=[]

# change to lowercase
for i in range(len(df)):
    review=df.x[i]
    review=review.lower() # change to lower case
    review=re.sub('[^a-z0-9]',' ',review) # replace non-aplhanumeric with whitespace
    tokens=tokenizer.tokenize(review) # breaks texts to list
    filtered_tokens=[ps.stem(wnl.lemmatize(w)) for w in tokens if w not in stopwords_set]
    review=' '.join(filtered_tokens)
    corpus.append(review)

# BoW transformation of corpus to matrix x
from sklearn.feature_extraction.text import CountVectorizer
#from sklearn.feature_extraction.text import TfidfVectorizer
cv=CountVectorizer()
cv.fit(corpus)
cv.vocabulary_
X=cv.transform(corpus).toarray() # dim is len(df), len(cv.vocabulary_)
df.y[df.y=='spam']=1 # spam as 1
df.y[df.y=='ham']=0 # ham as 0
y=df.y.values.astype(int)

# Train-Test data split

from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test=train_test_split(X,y,random_state=0)

# Classifier Algorithm

from sklearn.ensemble import RandomForestClassifier
rfc=RandomForestClassifier()

param_dict = {
        'n_estimators':[10,20,30], 
        'criterion':['gini','entropy'], 
        'max_depth':[None,5,10,15]
        }

from sklearn.model_selection import GridSearchCV
model = GridSearchCV(rfc,param_dict,cv=5)
model.fit(X_train,y_train) # took 2 minutes
model.best_params_
model.best_score_

y_pred_rfc=model.predict(X_test)

from sklearn.metrics import accuracy_score, confusion_matrix
accuracy_score(y_test,y_pred_rfc)
confusion_matrix(y_test,y_pred_rfc)

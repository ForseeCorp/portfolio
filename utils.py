# -*- coding: utf-8 -*-
"""
Created on Tue Jan 26 19:39:40 2021

@author: pathouli
"""
import numpy as np

def clean_text(text_in):
    import re
    clean_text_out = re.sub('[^A-z]+', " ", text_in)
    return clean_text_out

def clean_text_tokenize(text_in):
    import re
    from nltk.corpus import stopwords
    from nltk.stem import PorterStemmer
    ps = PorterStemmer()
    sw = stopwords.words('english')
    clean_text = re.sub('[^A-z]+', " ", text_in).lower().split()
    clean_text = [word for word in clean_text if word not in sw]
    clean_text = [ps.stem(word) for word in clean_text]
    return clean_text


def file_seeker(path_in):
    import enchant
    import os
    import pandas as pd
    import sys
    d = enchant.Dict("en_US")
    the_files = pd.DataFrame()
    for dirName, subdirList, fileList in os.walk(path_in):
        try:
            for word in fileList:
                tmp = dirName.split('/')[-1]
                t_path = dirName + '/' + word
                f = open(t_path, "r", encoding="utf8")
                test_text = clean_text(f.read().lower())
                test_text = [word for word in test_text.split() if d.check(word)]
                test_text = ' '.join(test_text)
                f.close()
                the_files = the_files.append(
                    {"label": tmp,
                     "body": test_text}, ignore_index=True)
        except Exception as e:
            print (e)
            pass
    return the_files

def rem_sw(var):
    from nltk.corpus import stopwords
    sw = stopwords.words('english')
    tmp = var.split() #tokenize
    fin_var = [word for word in tmp if word not in sw]
    fin_var = ' '.join(fin_var)
    return fin_var

def my_stemmer(var):
    from nltk.stem import PorterStemmer  
    ps = PorterStemmer()
    tmp = var.split()
    tmp_out = [ps.stem(word) for word in tmp]
    tmp_out = ' '.join(tmp_out)
    return tmp_out

def my_vec_func(var):
    from sklearn.feature_extraction.text import CountVectorizer
    import pandas as pd
    my_vec = CountVectorizer()
    my_xform_vec = pd.DataFrame(my_vec.fit_transform(var).toarray())
    my_xform_vec.columns = my_vec.get_feature_names()
    return my_xform_vec

def lda_fun(df_in, n_topics_in, num_words_in):
    import gensim
    import gensim.corpora as corpora 
    
    id2word = corpora.Dictionary(df_in)
    corpus = [id2word.doc2bow(text) for text in df_in]
    
    ldamodel = gensim.models.ldamodel.LdaModel(
        corpus, num_topics=n_topics_in, id2word=id2word, passes=15)
    ldamodel.save('model5.gensim')
    topics = ldamodel.print_topics(num_words=num_words_in)
    the_topics = dict()
    cnt = 0
    for topic in topics:
        the_topics[cnt] = topic
        cnt += 1 
    return the_topics 

from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
sentiment = SentimentIntensityAnalyzer()
def sentiment_fun(sentiment, var):
    #pip install vaderSentiment 
    
    out_score = sentiment.polarity_scores(var)
    return out_score['compound']


def train_model(df_in, label_in):    #TRAINING A MODEL    
    from sklearn.ensemble import RandomForestClassifier 
    from sklearn.model_selection import train_test_split    
    from sklearn.metrics import precision_recall_fscore_support    
    from sklearn.ensemble import GradientBoostingClassifier    
    from sklearn.naive_bayes import GaussianNB    
    from sklearn.model_selection import GridSearchCV    
    from sklearn.metrics import confusion_matrix   
    X_train, X_test, y_train, y_test = train_test_split(
         df_in, label_in, test_size=0.20, random_state=42) 
    
    
    rf = RandomForestClassifier(random_state=123) 
    parameters = {'max_depth':[10, 100], 'n_estimators':[10, 100]}  
    clf = GridSearchCV(rf, parameters, cv=5)    
    clf.fit(X_train, y_train)    
    grid_y_pred = clf.best_estimator_.predict(X_test)    
    the_metrics = precision_recall_fscore_support(y_test, grid_y_pred, average='weighted')  
    print (the_metrics)        
    print (clf.best_score_)
    print (clf.best_params_)
     
    rf_opt = RandomForestClassifier(**clf.best_params_, random_state=123)
    rf_opt.fit(X_train, y_train)
     
     
    clf = GradientBoostingClassifier(n_estimators=100, learning_rate=1.0,
                                      max_depth=1, random_state=0)
    #clf.fit(X_train, y_train)
    #clf = GaussianNB() 
    #clf.fit(X_train, y_train)
     
    y_pred = rf_opt.predict(X_test)
    print (confusion_matrix(y_test, y_pred))
 

def gen_senti(pos_list, neg_list, text):
    text_list = text.split(" ")
    pw = []
    nw = []
   
    for word in text_list:
        if word in pos_list:
            pw.append(word)
        elif word in neg_list:
            nw.append(word)
    
    pc = len(pw)
    nc = len(nw)
    if pc == 0 and nc == 0:
        return np.nan,0,0,0,0
    s = (pc - nc)/ (len(pw) + len(nw))
    return (s, pw, nw, pc, -nc)
    
    
     
     
     
     
     
     
     
     
     
     
     
     
     
     
     
     
     

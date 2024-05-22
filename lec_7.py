# -*- coding: utf-8 -*-
"""Update version of Lect5
Created on Tue Jan 26 18:17:15 2021


"""


import pickle
from utilclass import *
import utils

the_path = "/Users/randforrester/Desktop/topics"
export_path = "/Users/randforrester/Desktop/work/"

    
#by_test = file_seeker(the_path)

#mynew_data['body_sw'] = mynew_data.body.apply(rem_sw)
#onless the data changes run it again
#mynew_data['body_sw_stem'] = mynew_data.body_sw.apply(my_stemmer)
#pickle.dump(mynew_data, open( export_path+ "body.pkl","wb"))

mynew_data = pickle.load(open(export_path+ "body.pkl","rb"))

#mynew_data['sentiment'] = mynew_data.body.apply(sentiment_fun)# adds sentiment colomn to DF

the_column = "body_sw_stem"

my_vec_func_final = my_vec_func(mynew_data[the_column], export_path)
 
my_xform_tf_idf_final = my_tf_idf(mynew_data[the_column], export_path)

#print(jaccard_fun( "fly fishing is fun", " bass fishing is fun too")) #call function , inset parameters


tmp_data, model_out  = extract_embeddings(mynew_data.body_sw_stem, 50)
#my_vec_func_final = pickle.load(open(export_path+ "body.pkl","rb"))



def train_model(df_in):
  #Training A model   
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.model_selection import train_test_split
    from sklearn.metrics import precision_recall_fscore_support
    from sklearn.ensemble import GradientBoostingClassifier
    from sklearn.naive_bayes import GaussianNB
    from sklearn.model_selection import GridSearchCV
    
    X_train, X_test, y_train, y_test = train_test_split(
      my_xform_tf_idf_final ,mynew_data.label, test_size=0.20, random_state=42) #.20 = 80 /20 rule
    
    #model 1
    #clf = RandomForestClassifier(max_depth=2, random_state = 123)
    rf = RandomForestClassifier(random_state = 123)
    parameters = {'max_depth':[10,100], 'n_estimators':[10,100]}
    # x is tdif or vec or...x is dataframe and y is what we are trying to predcit
    
    
    clf = GridSearchCV(rf, parameters)
    clf.fit(X_train, y_train)
    
    print(clf.best_score_)#best score 
    
    print(clf.best_params_)# optimal prameters for random forest  
    
    rf_opt = RandomForestClassifier(**clf.best_params_,random_state = 123) #** automicallly include best parameter/score
    rf_opt.fit(X_train, y_train)
    
    
    #clf.fit(X_train, y_train)
    
    #model#2
    #clf = GradientBoostingClassifier(n_estimators=100, learning_rate=1.0,
                                     #max_depth=1, random_state=0).fit(X_train, y_train)
    #clf.fit(X_train, y_train)
    
    #model#3
    #lf = GaussianNB()
    #clf.fit(X_train, y_train)
    
    
    
    # 69 & 71 run with  (clf and clf.fit )
    y_pred = rf_opt.predict(X_test) #comparing the model prescio ,recall, fscore 
    
    the_metrics = precision_recall_fscore_support(y_test, y_pred, average = 'weighted')
    print(the_metrics)







#print(clf.predict(my_vec_func_final[:10]))

#traing the model

from sklearn.ensemble import RandomForestClassifier

clf = RandomForestClassifier(max_depth= 2, random_state = 123)
# x is tdif or vec or...x is dataframe and y is what we are trying to predcit

clf.fit(my_xform_tf_idf_final[10:], mynew_data.label[10:])

print(clf.predict(my_xform_tf_idf_final[:10]))

# Train model 

from sklearn.ensemble import RandomForestClassifier

clf = RandomForestClassifier(max_depth= 10, random_state = 123)
# x is tdif or vec or...x is dataframe and y is what we are trying to predcit

clf.fit(tmp_data[10:], mynew_data.label[10:])

print(clf.predict(tmp_data[:10]))






# import pickle 
# import pandas as pd 
# from utils import  *

# my_unlabled_data = pd.DataFrame(pickle.load(open("fun.pkl","rb")))
# #work 

# my_unlabled_data["body_clean"] = my_unlabled_data.body_basic.apply(
# clean_text_tokenize)
    
# my_test = lda_fun(my_unlabled_data.body_clean, 5,4)



#def gen_senti 
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import nltk
#pos_file = "/Users/randforrester/Desktop/work/positive-words.txt"
#neg_file = "/Users/randforrester/Desktop/work/negative-words.txt"
file_content_pos = open("/Users/randforrester/Desktop/work/positive-words.txt").read()
new_pos_list = file_content_pos.split()
file_content_n = open("/Users/randforrester/Desktop/work/negative-words.txt", encoding = "ISO-8859-1").read()
new_neg_list = file_content_n.split()


sid = SentimentIntensityAnalyzer()
#sentiment_score  = utils.gen_senti(pos_file, neg_file, sid)
pos_word_list=[]
neu_word_list=[]
neg_word_list=[]
new_dict = {}
for word in new_pos_list:
    if (sid.polarity_scores(word)['compound']) >= 0.5:
        pos_word_list.append(word)
        s_pos =+ (sid.polarity_scores(word)['pos'])
        new_dict[word] = sid.polarity_scores(word)['compound']
        #print (word ,sid.polarity_scores(word))
        
    else:
        neu_word_list.append(word)   
             
print(s_pos)

for word in new_neg_list:
    if (sid.polarity_scores(word)['compound']) <= -0.5:
        neg_word_list.append(word)
        new_dict[word] = sid.polarity_scores(word)['compound']
        #print (word ,sid.polarity_scores(word))
    else:
        neu_word_list.append(word)  

print("end")


print(mynew_data)

lis = []
compound_lis = []
for index,rows in mynew_data.iterrows():
    ret_tuple = utils.gen_senti(pos_word_list, neg_word_list, rows["body"])
    #print(ret_tuple)
    lis.append(ret_tuple[0])
    compound_lis.append(utils.sentiment_fun(sid, rows["body"]))
mynew_data["simple_senti"] = lis
mynew_data["vader"] = compound_lis

mean_senti = mynew_data["simple_senti"].mean()
mean_vader = mynew_data["vader"].mean()
median_senti = mynew_data["simple_senti"].median()
median_vader = mynew_data["vader"].median()
std_senti = mynew_data["simple_senti"].std()
std_vader = mynew_data["vader"].std()

print("senti mean is", mean_senti)
print("vader mean is", mean_vader)

print("senti median is", median_senti)
print("vader median is", median_vader)

print("std mean is", std_senti)
print("std mean is", std_vader)







#print('Positive :',pos_word_list,)        
#print('Neutral :',neu_word_list)    
#print('Negative :',neg_word_list)    



















#print (new_pos_list)

#sentiment_pos = SentimentIntensityAnalyzer(new_pos_list)






file_content_n = open("/Users/randforrester/Desktop/work/negative-words.txt", encoding = "ISO-8859-1").read()
tokens_1 = nltk.word_tokenize(file_content_n)
#print (tokens_1)


sentiment = SentimentIntensityAnalyzer()

test = sentiment.polarity_scores("OH THIS IS GREAT")














    



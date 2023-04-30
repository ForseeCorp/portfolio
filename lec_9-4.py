#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 21 19:52:15 2020
@author: pathou
"""

#import praw
import pandas as pd
import pytz
from collections import deque
#import pymongo
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from datetime import datetime
#
# subreddit_channel = 'politics'
# the_path = 'C:/Users/pathouli/myStuff/academia/columbia/socialSciences/GR5067/2021_spring/code_new/'
#
# the_look_back = 30
#
# fetch_creds = pd.read_csv(the_path + "creds.csv")
#
# reddit = praw.Reddit(
#      client_id=fetch_creds.client_id[0],
#      client_secret=fetch_creds.client_secret[0],
#      user_agent="testscript by u/fakebot3",
#      username=fetch_creds.username[0],
#      password=fetch_creds.password[0]
#  )
#
# def conv_time(var):
#     tmp_df = pd.DataFrame()
#     tmp_df = tmp_df.append(
#         {'created_at': var},ignore_index=True)
#     tmp_df.created_at = pd.to_datetime(
#         tmp_df.created_at, unit='s').dt.tz_localize(
#             'utc').dt.tz_convert('US/Eastern')
#     return datetime.fromtimestamp(var).astimezone(pytz.utc)
#
# global the_sentiment_dict
# senti_score = [0] * the_look_back
# the_sentiment_dict = {'sentiment':deque(senti_score)}
# global sentiment_score_var
# sentiment_score_var = SentimentIntensityAnalyzer()
#
# def score_sentiment(var):
#     import re
#     tmp = re.sub("[^a-zA-Z]+", ' ', var.upper()).split()
#     senti_score = round(
#         sentiment_score_var.polarity_scores(var)['compound'], 4)
#     the_sentiment_dict['sentiment'].pop()
#     the_sentiment_dict['sentiment'].appendleft(senti_score)
#     return the_sentiment_dict
#
# def get_reddit_data(var_in):
#     import pandas as pd
#     import numpy as np
#     tmp_dict = pd.DataFrame()
#     tmp_time = None
#     try:
#         tmp_dict = tmp_dict.append({"created_at": conv_time(
#                                         var_in.created_utc)},
#                                     ignore_index=True)
#         tmp_time = tmp_dict.created_at[0]
#     except:
#         print ("ERROR")
#         pass
#     tmp_dict = {'msg_id': str(var_in.id),
#                 'author': str(var_in.author),
#                 'body': var_in.body, 'datetime': tmp_time,
#                 'sentiment': score_sentiment(var_in.body)['sentiment'],
#                 'trailing_sentiment': np.average(
#                     score_sentiment(var_in.body)['sentiment'])}
#     return tmp_dict
#
# for comment in reddit.subreddit(subreddit_channel).stream.comments():
#     tmp_df = get_reddit_data(comment)
#     tmp = comment.body
#     print (tmp_df['body'], tmp_df['sentiment'], tmp_df['trailing_sentiment'])
#
from utils_2 import *

import pickle
import enchant
file = open('fun_test.pkl', 'rb')
data = pickle.load(file)

#print(data)
export_path = "/Users/randforrester/desktop/work/"
my_xform_vec_final = my_vec_func(data["label"], export_path)
import nltk
#nltk.download('stopwords')
train_model(my_xform_vec_final, data["label"], export_path)
test_text = pre_process_classify_stem(str(data["body_basic"]))
my_vec = pickle.load(open("vec.pkl", "rb"))
my_sample = my_vec.transform([test_text]).toarray()
my_model = pickle.load(open("model.pkl", "rb"))
the_pred = my_model.predict(my_sample)
classes = pd.DataFrame(my_model.classes_)
probs = pd.DataFrame(my_model.predict_proba(my_sample)).T
the_scores = pd.concat([classes,probs], axis=1)
the_scores.columns = {"class_lables", "likelihood"}
print(the_pred)

print(the_scores)

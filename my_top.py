# -*- coding: utf-8 -*-
"""
Created on Tue March  10 07:35:36 2020

@author: pathouli
"""

from crawler import write_crawl_results, word_freq

the_query = ['2016 hillary clinton speech transcript',
             '2016 donald trump speech transcript']
num_docs = 10

final_data, missing_words = write_crawl_results(the_query, num_docs)

#from crawler import word_freq

#make a dictionary for each query regex, key= unique word and value = frequency of word

#print(final_data)
       

df = word_freq(final_data)  

#print(df)


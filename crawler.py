# -*- coding: utf-8 -*-
"""
Created on Sat Oct  5 13:05:36 2019

@author: pathouli
"""
from bs4 import BeautifulSoup
import requests
import re
import requests
from fake_useragent import UserAgent
import pandas as pd
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
import enchant


def my_scraper(tmp_url_in): #tmp_url_in
    
    tmp_text = ''
    try:
        content = requests.get(tmp_url_in, timeout=30)
        soup = BeautifulSoup(content.text, 'html.parser')

        tmp_text = soup.findAll('p') 

        tmp_text = [word.text for word in tmp_text]
        tmp_text = ' '.join(tmp_text)
        tmp_text = re.sub('\W+', ' ', re.sub('xa0', ' ', tmp_text))
    except:
        pass

    return tmp_text

def fetch_urls(query_tmp, cnt): #query_tmp, cnt
    #now lets use the following function that returns
    #URLs from an arbitrary regex crawl form google

    #pip install pyyaml ua-parser user-agents fake-useragent
    
    ua = UserAgent()

    query = '+'.join(query_tmp.split())
    google_url = "https://www.google.com/search?q=" + query + "&num=" + str(cnt)
    print (google_url)
    response = requests.get(google_url, {"User-Agent": ua.random})
    soup = BeautifulSoup(response.text, "html.parser")

    result_div = soup.find_all('div', attrs = {'class': 'ZINbbc'})

    links = []
    titles = []
    descriptions = []
    for r in result_div:
        # Checks if each element is present, else, raise exception
        try:
            link = r.find('a', href = True)
            title = r.find('div', attrs={'class':'vvjwJb'}).get_text()
            description = r.find('div', attrs={'class':'s3v9rd'}).get_text()

            # Check to make sure everything is present before appending
            if link != '' and title != '' and description != '': 
                links.append(link['href'])
                titles.append(title)
                descriptions.append(description)
        # Next loop if one element is not present
        except:
            continue  

    to_remove = []
    clean_links = []
    for i, l in enumerate(links):
        clean = re.search('\/url\?q\=(.*)\&sa',l)

        # Anything that doesn't fit the above pattern will be removed
        if clean is None:
            to_remove.append(i)
            continue
        clean_links.append(clean.group(1))

    return clean_links
 
def write_crawl_results(my_query, the_cnt_in): #my_query, the_cnt_in)
    #let use fetch_urls to get URLs then pass to the my_scraper function 
    d = enchant.Dict("en_US")
    missing_us_words_list = []
    tmp_pd = pd.DataFrame()       
    for q_blah in my_query:
        the_urls_list = fetch_urls(q_blah, the_cnt_in)

        for word in the_urls_list:
            tmp_txt = my_scraper(word)
            stop_word = rem_sw(tmp_txt)
            stem_txt = my_stemmer(stop_word)
            
            for elem in tmp_txt.split(" "):
                if elem.strip() != "" and not elem.isdigit():
                    if not d.check(elem):
                        #print("*******", elem)
                        missing_us_words_list.append(elem)
                
            if len(tmp_txt) != 0:
                try:
                        
                    tmp_pd = tmp_pd.append({'body_basic': tmp_txt,
                                            'label': re.sub(' ', '_', q_blah),
                                            'stop': stop_word,
                                            "stem": stem_txt
                                            }, ignore_index=True)
                    print (word)
                except:
                    pass
    return tmp_pd, list(set(missing_us_words_list))




def rem_sw(var):
    
    sw = stopwords.words('english')
    tmp = var.split() #tokenizing 
    fin_var = [word for word in tmp if word not in sw]
    fin_var= ' '.join(fin_var)
    return fin_var 

def my_stemmer(var):
    
    ps = PorterStemmer()
    tmp = var.split()
    tmp_out = [ps.stem(word) for word in tmp ]
    tmp_out = ' '.join(tmp_out)
    return tmp_out




def word_freq(final_data):
    the_answer = dict() # creating Dictinary of everthing
    for word in final_data.label.unique():
        tmp_dict = dict() # temp dict for each loop
        tmp = final_data[final_data.label == word] # tmp varible matching labels 
        tmp = tmp.body_basic.str.cat().lower() # string concatenating and lowercase
        tmp = re.sub("[^A-z]+", ' ', tmp)
        tmp = tmp.split() # tokenizing 
        for wrd in set(tmp):
            tmp_dict[wrd] = tmp.count(wrd) #how many unique words exist
        #print(tmp_dict)
        the_answer[word] = pd.DataFrame.from_dict(tmp_dict, orient= 'index')
    return the_answer



#!/usr/bin/env python
# coding: utf-8

# In[32]:


"""
1a. Modify the code below to count 'down' in increments of -1 (5 points)
"""
for word in range(100, 0,-1):
    print (word)


# In[13]:


"""
1b. Change the code above to count down in increments of -0.5 (5 points)
"""
count = 100
while count > 0 :
    print(count)
    count = count - .5


# In[32]:


"""
2. Using list comprehension (HINT: []) populate an array whose individual word 
character lengths are >= 4 (10 points)
"""
the_sentence = 'the student went above and beyond the call of duty on the homework'

my_ar = []
for word in the_sentence.split():
    if len(word) >= 4:
        my_ar.append(word)
        print(my_ar)
        
        
        
        
        


# In[27]:


"""
3. Fix the errors in the code below and replace the word dog with turtle (10 points)
"""
import re
the_sentence = 'the orange cat jumped over the dog, but the orange cat landed on another orange cat'

#my_ar = my_ar = re.subway('dog', 'turtle', the_sentenced)
my_ar = my_ar = re.sub('dog', 'turtle', the_sentence)
print(my_ar)


# In[48]:


"""
4. Remove all special characters from the sentence except for @ (10 points)
"""
the_sentence = 'woah!!! the @student really^ #impressed me, and& so did ??you!!!'

my_ar1= re.sub('[^A-Za-z0-9@]+', ' ', the_sentence)
print(my_ar1)




# In[73]:


"""
5. create a sentence, each word seperated by one space, out of the following array 
and replace any special characters with a no space, except '!', with '' (10 points)
"""

the_ar = ['woah!!!','the','@student',' really^','# impressed','me,','and&','so','did','??you!!!']
one_sent = ' '.join(the_ar)
my_ar2 = re.sub('[^A-Za-z0-9!]+', '', one_sent)
#print(my_ar2)
print(my_ar2.replace('!',' '))




# In[9]:


"""
6. Create a program that loops 10 times and for each loop generate a random integer between 1 and 10, 
and print 'even' if the number is even and 'odd' if the number is odd (HINT: import random)
if the number is odd (10 points)
"""
import random
evens = 0
odds = 0
i = 0
while i < 10:
    number = random.randint(0, 100)
    if number % 2 == 0:
        evens += 1
        print("even number", number)
    else:
        odds += 1
    i += 1
    print("odd number", number)
print("The number of even numbers is: " , evens)
print("The number of odd numbers is: " , odds)


# In[20]:


"""  
7. Create a program that counts the length of each word in an arbitrary sentence and stores 
each word and count pair in a pandas dataframe where one column is the word and one column is the 
word length (number of characters) (10 points)
"""
import pandas as pd

test_ar_a = ("this is my sentence to work on for today")
new_list = test_ar_a.split()

my_df = pd.DataFrame()

"""for word in test_ar_a:
    my_df = my_df.append({'num_a': word, 'num_b': len(word)}, ignore_index=True)"""
    
for word in new_list:
        my_df = my_df.append({'Word': word, 'Lenght': len(word)}, ignore_index=True)


# In[23]:


my_df.head()


# In[24]:


"""
8. Replace the word cat with mouse (10 points)
"""

import re
the_sentence = 'the cat jumped over the dog, but the cat landed on another cat!'


my_ar = my_ar = re.sub('cat', 'mouse', the_sentence)
print(my_ar)



# In[26]:


"""
9. Cleanse the following sentence by removing all special characters 
except when the hyphen joins to two words and exclamation points (10 points)
"""

the_sentence = 'The impact*of data-driven$^%&marketing approaches!!'
my_ar2 = re.sub('[^A-Za-z0-9!-]+', ' ', the_sentence)
print(my_ar2)
#print(my_ar2.replace('!',' '))


# In[28]:


"""
10. Write a python program that inputs the sentence below and returns a dictionary
that has each unique character as a key and count of that character as the value.
(10 points)
"""

the_sentence = 'Everything flows, and nothing abides, everything gives way, and nothing stays fixed'

my_tokens = the_sentence.split()

my_word_dict = {word:my_tokens.count(word) for word in set(my_tokens)}

print (my_word_dict)


# In[ ]:





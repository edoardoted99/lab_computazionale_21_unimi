import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import wikipediaapi
import random, time

import pandas as pd  # To read data

from scipy.optimize import curve_fit
import math 

N_en = []
n_en = []

N_it = []
n_it = []

wiki_en = wikipediaapi.Wikipedia('en')  #setting language api (wikipedia pages language)
wiki_it = wikipediaapi.Wikipedia('it')

italian_words = []
english_words = []

alphanumeric = ""

#cleaning data

f_ita = open("it.txt", "r+")
it_words = [line for line in f_ita.readlines()]
for word in it_words:
    word = word.replace("\n","")
    word = word.replace("/\n","")
    for character in word:
        if character.isalnum():
            alphanumeric += character
    italian_words.append(word)

f_eng = open("en.txt", "r")
en_words = [line for line in f_eng.readlines()]
for word in en_words:
    word = word.replace("\n","")
    word = word.replace("/\n","")
    for character in word:
        if character.isalnum():
            alphanumeric += character
    english_words.append(word)


TOT = 20 #tot number of wikipedia pages to scrape
min_words=0 #min number of text words
sleep_time = 0 #to not your session be killed by wikipedia's servers (set about 0.5 for 2000 api calls)

words = []
for i in range(TOT):
    words.append(random.choice(english_words))
  
print(words)
#english 

#print(english_words)
#print(italian_words)

tot = 0
discard = 0

for word in words:
    count_words = []
    page = wiki_en.page(word)

    text = page.text
    time.sleep(sleep_time)
    wiki_words = text.split()

    if len(wiki_words) > min_words:
        print(text)
        for word in wiki_words:
            if not word in count_words:
                count_words.append(word)

        if len(wiki_words)!= 0:
            N_en.append(len(wiki_words))
            
        if len(count_words) !=0:
            n_en.append(len(count_words))

        if tot%20==0 and tot !=0:
            print("N = ", len(wiki_words))
            print("n = ", len(count_words))
            
    else:
        discard += 1
    tot += 1
    
  
    


#italian
deltas = []   
speeds = []
tot = 0
discard = 0

words = []
for i in range(TOT):
    words.append(random.choice(italian_words))
print(words)
for word in words:
    
    count_words = []
    page = wiki_en.page(word)
    time.sleep(sleep_time)
    text = page.text
    
    wiki_words = text.split()
    if len(wiki_words) > min_words:
        print(text)
        for word in wiki_words:
            if not word in count_words:
                count_words.append(word)

        if len(words)!= 0:
            N_it.append(len(wiki_words))
       
        if len(count_words)!= 0:
            n_it.append(len(count_words))

        if tot%20==0 and tot !=0:
            print("N = ", len(word))
            print("n = ", len(count_words))
    else:
        discard += 1
    tot += 1
    


fig, ax = plt.subplots()
ax.scatter(N_en, n_en,color = 'red', label = "en")
ax.scatter(N_it, n_it,color = 'blue', label = "it")


ax.set(xlabel='N words in text', ylabel='n different words',
       title='Analysis differents words in Wikipedia Pages')
ax.grid()
k_en = np.polyfit(np.log(N_en), n_en, 1)
k_it = np.polyfit(np.log(N_it), n_it, 1)

print('en: ', k_en)
print('it: ', k_it)


label_it = "It: y = " + str("%.2f" % k_it[0]) + " log(x) + " + str("%.2f" % k_it[1])
label_en = "En: y = " + str("%.2f" % k_en[0]) + " log(x) + " + str("%.2f" % k_en[1])

values_x = N_en + N_it

x = np.linspace(min_words,np.amax(values_x),1000)
plt.plot(x,k_en[0]*np.log(x)+k_en[1], 'r', label=label_en)
plt.plot(x,k_it[0]*np.log(x)+k_it[1], 'b', label=label_it)


plt.legend()
fig.savefig("words.png")
plt.show()

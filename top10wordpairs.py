#importing required libraries and staring spark
import operator
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import nltk
from os import path
from PIL import Image
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
from nltk.corpus import stopwords 
from collections import Counter
import matplotlib.pyplot as plt
import pandas as pd
from pyspark import SparkContext, SparkConf
os.environ["PYSPARK_PYTHON"] = "/Library/Frameworks/Python.framework/Versions/3.7/bin/python3"
os.environ["PYSPARK_DRIVER_PYTHON"] = "/Library/Frameworks/Python.framework/Versions/3.7/bin/python3"
sc = SparkContext("local","PySpark")
contentRDD = sc.textFile("/Users/teja/Downloads/nytimes_news_articles.txt")

#preprocessing data 
contentRDD = contentRDD.filter(lambda x: len(x) > 0)
content = contentRDD.collect() # data is stored in a list
l = len(content)
for i in range(l):#removing unwanted symbols in strings
    if not content[i].startswith('URL'):
        content[i] = content[i].replace("-", "").replace("—","").replace("“","").replace(",","").replace("’","").replace("'","").replace("”","").replace(";","").replace(":","").replace("(","").replace(")","").replace("‘","")
        if content[i].endswith("."):
            content[i] = content[i].replace(".","")

#get data for sports category 
def get_sports_data(content):#collecting only sports related data from full text
    sports_category_data = []
    url = ""
    for row in content:
        if row.startswith("URL"):
            url = row
        elif "sports" in url:
            sports_category_data.append(row)
    return sports_category_data
sports_data = get_sports_data(content)   #sports data

#split the each paragrapgh in sports_data
#ignore empty strings and removing stopwords and removing whitespaces in a string using strip function
def preprocess_sports_data(sports_data):
    sports_data_after_split = [i.split(" ") for i in sports_data]
    sw = stopwords.words('english')#stopwords using nltk
    sports_data_without_stopwords = []
    for lst in sports_data_after_split:
        new_lst = []
        for wrd in lst:
            wrd_lower = wrd.strip().lower()
            if (len(wrd) > 0) and (wrd_lower not in sw):
                new_lst.append(wrd_lower)

        sports_data_without_stopwords.append(new_lst)
    return sports_data_without_stopwords
processes_sports_data = preprocess_sports_data(sports_data)#processed data of sports category

wordspairs = {}
for par in range(len(processes_sports_data)):
    for wrd in range(len(processes_sports_data[par])-1):
        biagram = processes_sports_data[par][wrd] + " " + processes_sports_data[par][wrd+1]
        if biagram not in wordspairs:
            wordspairs[biagram] = 1
        else:
            wordspairs[biagram] += 1

#top 10 word pairs
k = Counter(wordspairs) 
# Finding top10 word pairs 
top10_wordpairs = k.most_common(10)
word_pairs = dict(top10_wordpairs)
#visualizing the top 10 word_pairs graphically
plt.figure(figsize=(20, 8))
plt.bar(list(word_pairs.keys()), list(word_pairs.values()))
plt.xlabel("Word Pairs")
plt.ylabel("Count")
plt.title("Top 10 word pairs in Sports cartegory")
plt.show()
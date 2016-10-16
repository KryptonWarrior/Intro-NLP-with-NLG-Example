AskIrina was my first project in python. I wanted to learn python by working on a cool NLP project. Since I was impressed with NextIT virtual online assistance product “Ask Jenn”, I decided to make a simple version of that.  If you are newbie, please take a look at my presentation, [“Intro NLP”]( https://goo.gl/JFwyTJ). It gives you a general idea about NLP process. AskIrina is a web interface developed with HTML, CSS, JavaScript and connected to python and MySQL database. 

Step 1:  I need to clean up my sentence from any punctuation. I use regular expression to find and remove all of the punctuation from my input.

```python
import re, string

s = "string. With. Punctuation"
regex = re.compile('[%s]' % re.escape(string.punctuation))

print regex.sub('', s)
```

Step2: I am going to clean up my sentence a little more and remove all the stop words. The remaining will be the important words in the input. I use stop_words library here. You use nltk to remove the stop words. I will repeat the step 1 process in the end to remove punctuation from Question.txt

```python

from stop_words import get_stop_words
import os
import re, string

# change your directory
os.chdir('~/Desktop/')
# read the text file
text = open('../Desktop/AskIrina/Question.txt', "r")

# removing stopwords from the text
stops = get_stop_words('english')

newText = ""
for line in text:
    newLine = []
    for w in line.split(" "):
        if w.lower() not in stops:
            #print w
            newLine.append(w)
    #print newLine
    newText = newText + " ".join(newLine)

regex = re.compile('[%s]' % re.escape(string.punctuation))

print regex.sub('', newText)
```

Step 3: Then, I am going to tokenize the sentence in 3 parts: unigram, bigrams and trigrams.

```python

import nltk, os, re
from operator import itemgetter
from nltk import bigrams, trigrams
from stop_words import get_stop_words
import os

os.chdir('C:/Users/Moeen/Desktop/')
text = open('../Desktop/AskIrina/Question.txt', "r")

# removing stopwords from the text
stops = get_stop_words('english')
newText = ""
newLine = []
for w in text.split(" "):
	if w.lower() not in stops:
		newLine.append(w)
newText = newText + " ".join(newLine)

regex = re.compile('[%s]' % re.escape(string.punctuation))
regexText = regex.sub('', newText)

# split the text into tokens
tokens = nltk.word_tokenize(regexText)
uni_toekns = [token.lower() for token in tokens if len(token) > 1] #same as unigrams
bi_tokens = bigrams (tokens)
tri_tokens = trigrams (tokens)

uni_tokenList = [(item, uni_toekns.count(item)) for item in sorted(set(uni_toekns))] 
bi_tokenList = [(item, tokens.count(item)) for item in sorted(set(bi_tokens))] 
tri_tokenList = [(item, tokens.count(item)) for item in sorted(set(tri_tokens))]
```
Now, I am going to match the unigrams, bigrams and trigrams tokens to the key words column row by row in the MySQL database. The python code will grab the best match answer in that row and print it out in the UI. 

In did not cover the material from connecting the python to MySQL and UI. You may find the complete code here: AskIrina_webservices.py

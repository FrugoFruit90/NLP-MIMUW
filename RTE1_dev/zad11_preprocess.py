# -*- coding: utf-8 -*-

from nltk.corpus import wordnet as wn
import nltk
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
from nltk.tree import Tree

with open('dev.xml', 'r') as myfile:
    content_html = myfile.read()

soup = BeautifulSoup(content_html, 'lxml')

# nltk.download('maxent_ne_chunker')
# nltk.download('punkt')
# nltk.download('averaged_perceptron_tagger')

texts = soup.findAll('t', text=True)
hypotheses = soup.findAll('h', text=True)
labels = soup.findAll('pair')

# TODO krok 1: wyciągnąć teksty i hipotezy bez htmla + labele
# TODO krok 2: to samo, tylko z podmianą named entities na pojedynczy token

with open('texts.txt', 'w') as file:
    for i in range(len(texts)):
        file.write(str(texts[i].contents[0]) + '\n')

with open('hypotheses.txt', 'w') as file:
    for i in range(len(hypotheses)):
        file.write(str(hypotheses[i].contents[0]) + '\n')

with open('values.txt', 'w') as file:
    for i in range(len(hypotheses)):
        file.write(labels[i]['value'] + '\n')

# for i in range(len(texts)):
#     text = nltk.word_tokenize(str(texts[i].contents[0]))
#     tagged_text = nltk.pos_tag(text)
#     hyp = nltk.word_tokenize(str(hypotheses[i].contents[0]))
#     tagged_hyp = nltk.pos_tag(hyp)
#     print(tagged_text, tagged_hyp)
#
#     print(nltk.ne_chunk(tagged_text, binary=True))


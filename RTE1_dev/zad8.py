from nltk.corpus import wordnet as wn
import nltk
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
from nltk.tree import Tree

with open('dev.xml', 'r') as myfile:
    content_html = myfile.read()

soup = BeautifulSoup(content_html, 'lxml')

# nltk.download('wordnet')
# nltk.download('words')
# nltk.download('maxent_ne_chunker')
# nltk.download('punkt')
# nltk.download('averaged_perceptron_tagger')

for node in soup.findAll('t', text=True) + soup.findAll('h', text=True):
    print(str(node.contents[0]))
    text = nltk.word_tokenize(str(node.contents[0]))
    tagged_text = nltk.pos_tag(text)
    for el in nltk.ne_chunk(tagged_text, binary=True):
        print(wn.synsets(el[0][0]))

        # if len(el) == 1:
        #     print(el, wn.synsets(el)[0])
        # else:
        #     print("trololo")

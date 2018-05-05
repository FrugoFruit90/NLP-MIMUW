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
    text = nltk.word_tokenize(str(node.contents))
    tagged_sentence = nltk.pos_tag(text)
    ne_rec = nltk.ne_chunk(tagged_sentence, binary=True)
    for tagged_word in ne_rec:
        if hasattr(tagged_word, "_label"):
            if getattr(tagged_word, '_label') == 'NE':
                print(tagged_word)
            else:
                raise ValueError
        else:
            print(tagged_word, wn.synsets(tagged_word[0]))


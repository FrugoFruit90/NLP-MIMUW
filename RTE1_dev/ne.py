import nltk
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
from nltk.tree import Tree

def get_continuous_chunks(text):
	chunked = ne_chunk(pos_tag(word_tokenize(text)))
	prev = None
	continuous_chunk = []
	current_chunk = []
	for i in chunked: 
		if type(i) == Tree:
			current_chunk.append(" ".join([token for token, pos in i.leaves()]))
		elif current_chunk:
			named_entity = " ".join(current_chunk)
			if named_entity not in continuous_chunk:
				continuous_chunk.append(named_entity)
				current_chunk = []
			else:
				continue
	return continuous_chunk

with open('dev.xml', 'r') as myfile:
  content_html = myfile.read()

soup = BeautifulSoup(content_html, 'lxml')
nltk.download('maxent_ne_chunker')
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')

for node in soup.findAll('t',text=True) + soup.findAll('h',text=True):
	print(str(node.contents[0]))
	text = nltk.word_tokenize(str(node.contents[0]))
	tagged_text = nltk.pos_tag(text)
	print(nltk.ne_chunk(tagged_text, binary=True))

from nltk.corpus import wordnet as wn
import nltk
from bs4 import BeautifulSoup

with open('dev.xml', 'r') as myfile:
    content_html = myfile.read()

soup = BeautifulSoup(content_html, 'lxml')

# nltk.download('wordnet')
# nltk.download('words')
# nltk.download('maxent_ne_chunker')
# nltk.download('punkt')
# nltk.download('averaged_perceptron_tagger')

nouns = 0
nouns_found = 0

verbs = 0
verbs_found = 0

adjs = 0
adjs_found = 0

advs = 0
advs_found = 0

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
            try:
                if tagged_word[1].startswith('NN'):
                    nouns += 1
                    if len(wn.synsets(tagged_word[0])) > 0:
                        nouns_found += 1
                elif tagged_word[1].startswith('VB'):
                    verbs += 1
                    if len(wn.synsets(tagged_word[0])) > 0:
                        verbs_found += 1
                elif tagged_word[1].startswith('JJ'):
                    adjs += 1
                    if len(wn.synsets(tagged_word[0])) > 0:
                        adjs_found += 1
                elif tagged_word[1].startswith('RB') or tagged_word[1] == 'WRB':
                    advs += 1
                    if len(wn.synsets(tagged_word[0])) > 0:
                        advs_found += 1
            except IndexError:
                pass
            try:
                print(tagged_word, wn.synsets(tagged_word[0])[0].lemma_names(),
                      wn.synsets(tagged_word[0])[0].hypernyms())
            except IndexError:
                print(tagged_word)

print('\nNouns:')
print(nouns)
print(nouns_found)
print(nouns_found/nouns)

print('\nVerbs:')
print(verbs)
print(verbs_found)
print(verbs_found/verbs)

print('\nAdjectives:')
print(adjs)
print(adjs_found)
print(adjs_found/adjs)

print('\nAdverbs:')
print(advs)
print(advs_found)
print(advs_found/advs)
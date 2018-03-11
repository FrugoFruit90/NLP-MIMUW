# -*- coding: utf-8 -*-
# ćwiczenia w dniu 5 marca 2018
import pandas as pd
import csv


def remove_colon(dict_entry):
    """
    :param dict_entry: 
    :return: 
    """
    return str(dict_entry).split(':')[0]


def vocabulary_inclusion(source_a, source_b, morph='lemat', lower=False):
    """
    :param source_a: 
    :param source_b: 
    :param morph: either 'lemat' or 'forma'
    :param lower: whether or not we simplfy the vocabularies by making all the forms lower case
    :return: the share of some type of form in source a that can be found in source b
    """
    morph_a = source_a[morph]
    morph_b = source_b[morph]

    if lower:
        morph_a = morph_a.str.lower()
        morph_b = morph_b.str.lower()

    morph_a = set(morph_a.apply(remove_colon).unique())
    morph_b = set(morph_b.apply(remove_colon).unique())

    intersection = morph_a.intersection(morph_b)

    return round(len(intersection) / len(morph_a)*100, 1)


def find_lemma_in_vocabulary(form, vocab):
    return vocab.get(form)


N_ROWS = None

print("\nZadanie 1. Pokrycie SGJP na formach i lematach NKJP1M.")
# Jaki odsetek form i lematów z NKJP1M (oraz z listy frekwencyjnej NKJP1m) znajduje się w SGJP i vice versa.
# Co się zmieni po sprowadzeniu form do małych liter?
#
# Formalnie:
# Dla i \in {F,f,L,l} należy obliczyć wartości:
#
# |X_i \cap Y_i| / |X_i|,
# |X_i \cap Y_i| / |Y_i|,
# \sum_{s \in X_i \cap Y_i} f_i(s) / \sum_{s \in Y_i} f_i(s)

print("\tUwaga - usunąłem części lematów po dwukropkach")

# load sgjp dict
sgjp_dict = pd.read_csv("sgjp-20180304.tab", skiprows=29, sep='	', nrows=N_ROWS,
                        names=['forma', 'lemat', 'interpretacja', 'inne1', 'inne2'])

# load nkjp freq list
nkjp_freq = pd.read_csv("1_NKJP1M-frequency.tab", sep='	', nrows=N_ROWS, engine='python', quoting=csv.QUOTE_NONE,
                        names=['forma', 'lemat', 'interpretacja', 'freq'], encoding='utf-8')

# pandas tries to read NaN as a numpy type, we need to explain to him that it's in fact a string ;)
nkjp_freq['forma'] = nkjp_freq['forma'].fillna('NaN')

print("\tSłownik SGJP zawiera ok. {} mln wierszy".format(round(sgjp_dict.shape[0]/1000000, 2)))
print("\tTabela frekwencji NKJP zawiera ok. {} mln wierszy".format(round(nkjp_freq.shape[0]/1000000, 2)))

print("\n\tProcent słów z korpusu zawartych w słowniku:")
print('\t\tformy - {}%'.format(vocabulary_inclusion(nkjp_freq, sgjp_dict, 'forma')))
print('\t\tformy (małe litery) - {}%'.format(vocabulary_inclusion(nkjp_freq, sgjp_dict, 'forma', lower=True)))
print('\t\tlematy {}%'.format(vocabulary_inclusion(nkjp_freq, sgjp_dict, 'lemat')))
print('\t\tlematy (małe litery) - {}%'.format(vocabulary_inclusion(nkjp_freq, sgjp_dict, 'lemat', lower=True)))

print("\n\tProcent słów ze słownika zawartych w korpusie:")
print('\t\tformy - {}%'.format(vocabulary_inclusion(sgjp_dict, nkjp_freq, 'forma')))
print('\t\tformy (małe litery) -  {}%'.format(vocabulary_inclusion(sgjp_dict, nkjp_freq, 'forma', lower=True)))
print('\t\tlematy - {}%'.format(vocabulary_inclusion(sgjp_dict, nkjp_freq, 'lemat')))
print('\t\tlematy (małe litery) - {}%'.format(vocabulary_inclusion(sgjp_dict, nkjp_freq, 'lemat', lower=True)))

print("\n\nZadanie 2. Niejednoznaczność lematyzacji")
# Forma 'lub' lematyzuje się do 'lub' i 'lubić'.
# Ile jest form w SGJP, które mają niejednoznaczną lematyzację.
# Co się stanie, gdy utniemy części lematów, które są po ':' ?

sgjp_groupby_form = sgjp_dict.groupby('forma')['lemat'].apply(list)
number_of_lemmas_counts = sgjp_groupby_form.apply(len).value_counts()

print('\n\tW SGJP niejednoznaczną lematyzację ma ok. {} mln słów'.
      format(round((number_of_lemmas_counts.sum() - number_of_lemmas_counts[1])/1000000, 2)))

sgjp_groupby_form_cut_lemma = sgjp_groupby_form.apply(
    lambda lemma_list: set([remove_colon(lemma) for lemma in lemma_list]))
number_of_cut_lemmas_counts = sgjp_groupby_form_cut_lemma.apply(len).value_counts()

print("\tPo ucięciu części lematów po ':' pozostało tylko ok. {} mln słów z niejednoznacznymi lematami".
      format(round((number_of_cut_lemmas_counts.sum() - number_of_cut_lemmas_counts[1])/1000000, 2)))

print("\n\nZadanie 3. Niejednoznaczność lematyzacji")
# Jaki procent form z NKJP1M lematyzowalnych za pomocą SGJP lematyzuje się jednoznacznie?
# Co się zmieni po sprowadzeniu form do małych liter?

# First drop duplicate forms
nkjp_freq_unq = nkjp_freq.drop_duplicates('forma')

# Then assign lemmas from sgjp to nkjp forms
nkjp_freq_unq['sgjp_lemma'] = nkjp_freq_unq['forma'].apply(lambda x: sgjp_groupby_form.get(x))

# Then select only those forms that we have lemmas for
nkjp_freq_lemma_exists = nkjp_freq_unq[nkjp_freq_unq['sgjp_lemma'].notnull()]

number_of_lemmas_counts = nkjp_freq_lemma_exists['sgjp_lemma'].apply(len).value_counts()
print('\n\tWśród słów z korpusu NKJP jednoznaczną lematyzację w SGJP ma ok. {}% słów'.
      format(round(100*(number_of_lemmas_counts[1]/number_of_lemmas_counts.sum()), 1)))

# now the same but for lower case
nkjp_freq_unq_lower = nkjp_freq.copy()
nkjp_freq_unq_lower['forma'].str.lower()
nkjp_freq_unq_lower.drop_duplicates('forma')
nkjp_freq_lower_lemma_exists = nkjp_freq_unq_lower[nkjp_freq_unq_lower['sgjp_lemma'].notnull()]

number_of_lemmas_counts = nkjp_freq_lower_lemma_exists['sgjp_lemma'].apply(len).value_counts()
print('\tWśród słów z korpusu NKJP (małe litery) jednoznaczną lematyzację w SGJP ma ok. {}% słów'.
      format(round(100*(number_of_lemmas_counts[1]/number_of_lemmas_counts.sum()), 1)))

# Zadania dodatkowe:
#
# 1. znalezienie za pomocą Poliqarp'a znań mających sekwencję "każdy" - "pewien".
#
# 2. oszacuj średnią długość zdania w języku polskim na podstawie NKJP1M.
#
# 3. narysuj rozkład długości zdań na podstawie NKJP1M.

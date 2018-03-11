# -*- coding: utf-8 -*-
# ćwiczenia w dniu 5 marca 2018
import pandas as pd
import csv


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

    morph_a = set(morph_a.unique())
    morph_b = set(morph_b.unique())

    intersection = morph_a.intersection(morph_b)

    return len(intersection) / len(morph_a)


N_ROWS = None

# Zadanie 1. Pokrycie SGJP na formach i lematach NKJP1M.
# Uwagi:
# 1. Używać "lower", żeby brać tylko małe litery
# 2. TODO: nie usłyszałem ;_; O KTOŚ WIE: wywalić z lematów po dwukropkach v1 i v2
# 3. TODO: rozróżnienie między małym a dużym M
# load sgjp dict
sgjp_dict = pd.read_csv("sgjp-20180304.tab", skiprows=29, sep='	', nrows=N_ROWS,
                        names=['forma', 'lemat', 'interpretacja', 'inne1', 'inne2'])

# load nkjp freq list
nkjp_freq = pd.read_csv("1_NKJP1M-frequency.tab", sep='	', nrows=N_ROWS, engine='python', quoting=csv.QUOTE_NONE,
                        names=['forma', 'lemat', 'interpretacja', 'freq'])

sgjp_unq_form_set = set(sgjp_dict['forma'].unique())
sgjp_unq_lemma_set = set(sgjp_dict['lemat'].unique())
nkjp_unq_form_set = set(nkjp_freq['forma'].unique())
nkjp_unq_lemma_set = set(nkjp_freq['lemat'].unique())

basic_form_intersection = sgjp_unq_form_set.intersection(nkjp_unq_form_set)
basic_lemma_intersection = sgjp_unq_lemma_set.intersection(nkjp_unq_lemma_set)

basic_form_corp_in_dict = len(basic_form_intersection) / len(sgjp_unq_form_set)
basic_form_dict_in_corp = len(basic_form_intersection) / len(nkjp_unq_form_set)

basic_lemma_corp_in_dict = len(basic_lemma_intersection) / len(sgjp_unq_lemma_set)
basic_lemma_dict_in_corp = len(basic_lemma_intersection) / len(nkjp_unq_lemma_set)

print('Procent form z korpusu zawartych w słowniku wynosi {}'.format(basic_form_dict_in_corp))
print('Procent form ze słownika zawartych w korpusie wynosi {}'.format(basic_form_corp_in_dict))
print('Procent lematów z korpusu zawartych w słowniku wynosi {}'.format(basic_lemma_dict_in_corp))
print('Procent lematów ze słownika zawartych w korpusie wynosi {}'.format(basic_lemma_corp_in_dict))

nkjp_unq_low_form_set = set(nkjp_freq['forma'].str.lower().unique())
nkjp_unq_low_lemma_set = set(nkjp_freq['lemat'].str.lower().unique())
sgjp_unq_low_form_set = set(sgjp_dict['forma'].str.lower().unique())
sgjp_unq_low_lemma_set = set(sgjp_dict['lemat'].str.lower().unique())

lower_form_intersection = nkjp_unq_low_form_set.intersection(sgjp_unq_low_form_set)
lower_lemma_intersection = nkjp_unq_low_lemma_set.intersection(sgjp_unq_low_lemma_set)

lower_form_dict_in_corp = len(lower_form_intersection) / len(nkjp_unq_low_form_set)
lower_form_corp_in_dict = len(lower_form_intersection) / len(sgjp_unq_low_form_set)

lower_lemma_dict_in_corp = len(lower_lemma_intersection) / len(nkjp_unq_low_lemma_set)
lower_lemma_corp_in_dict = len(lower_lemma_intersection) / len(sgjp_unq_low_lemma_set)

print('Procent form z korpusu zawartych w słowniku wynosi {}'.format(lower_form_corp_in_dict))
print('Procent form ze słownika zawartych w korpusie wynosi {}'.format(lower_form_dict_in_corp))
print('Procent lematów z korpusu zawartych w słowniku wynosi {}'.format(lower_lemma_corp_in_dict))
print('Procent lematów ze słownika zawartych w korpusie wynosi {}'.format(lower_lemma_dict_in_corp))

print("##############################################################")
print("W jakim stopniu")
print('Procent form z korpusu zawartych w słowniku wynosi {}'.format(vocabulary_inclusion(nkjp_freq, sgjp_dict, 'forma')))
print('Procent form ze słownika zawartych w korpusie wynosi {}'.format(vocabulary_inclusion(sgjp_dict, nkjp_freq, 'forma')))
print('Procent lematów z korpusu zawartych w słowniku wynosi {}'.format(vocabulary_inclusion(nkjp_freq, sgjp_dict, 'lemat')))
print('Procent lematów ze słownika zawartych w korpusie wynosi {}'.format(vocabulary_inclusion(sgjp_dict, nkjp_freq, 'lemat')))

print('Procent form (małe litery) z korpusu zawartych w słowniku wynosi {}'.format(vocabulary_inclusion(nkjp_freq, sgjp_dict, 'forma', lower=True)))
print('Procent form (małe litery) ze słownika zawartych w korpusie wynosi {}'.format(vocabulary_inclusion(sgjp_dict, nkjp_freq, 'forma', lower=True)))
print('Procent lematów (małe litery) z korpusu zawartych w słowniku wynosi {}'.format(vocabulary_inclusion(nkjp_freq, sgjp_dict, 'lemat', lower=True)))
print('Procent lematów (małe litery) ze słownika zawartych w korpusie wynosi {}'.format(vocabulary_inclusion(sgjp_dict, nkjp_freq, 'lemat', lower=True)))

# Zadanie 2. Niejednoznaczność lematyzacji
# Forma 'lub' lematyzuje się do 'lub' i 'lubić'.
# Ile jest form w SGJP, które mają niejednoznaczną lematyzację.
# Co się stanie, gdy utniemy części lematów, które są po ':' ?

# brać unique a potem sprawdzać mnogość

# Zadanie 3. Niejednoznaczność lematyzacji

# Jaki procent form z NKJP1M lematyzowalnych za pomocą SGJP lematyzuje się jednoznacznie? Co się zmieni po sprowadzeniu form do małych liter?



# Zadania dodatkowe:
#
# 1. znalezienie za pomocą Poliqarp'a znań mających sekwencję "każdy" - "pewien".
#
# 2. oszacuj średnią długość zdania w języku polskim na podstawie NKJP1M.
#
# 3. narysuj rozkład długości zdań na podstawie NKJP1M.

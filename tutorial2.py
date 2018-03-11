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

    return int((len(intersection) / len(morph_a))*1000)/10.0


N_ROWS = None

print("\nZadanie 1. Pokrycie SGJP na formach i lematach NKJP1M.")
print("\tUwaga - usunąłem części lematów po dwukropkach")

# load sgjp dict
sgjp_dict = pd.read_csv("sgjp-20180304.tab", skiprows=29, sep='	', nrows=N_ROWS,
                        names=['forma', 'lemat', 'interpretacja', 'inne1', 'inne2'])

# load nkjp freq list
nkjp_freq = pd.read_csv("1_NKJP1M-frequency.tab", sep='	', nrows=N_ROWS, engine='python', quoting=csv.QUOTE_NONE,
                        names=['forma', 'lemat', 'interpretacja', 'freq'])

print("\tSłownik SGJP zawiera {} wierszy".format(sgjp_dict.shape[0]))
print("\tTabela frekwencji NKJP zawiera {} wierszy".format(nkjp_freq.shape[0]))

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

texts = open('data/texts_parsed.txt', 'r').readlines()
values = open('data/values_1_sent.txt', 'r').readlines()
hypotheses = open('data/hypotheses_parsed.txt', 'r').readlines()

values = ['1' if x == 'TRUE\n' else '0' for x in values]


with open('data/learning.txt', 'w') as file:
    for i in range(len(texts)):
        line = values[i] + ' \t|BT| ' + texts[i][:-1] + ' |BT| ' + hypotheses[i][:-1] + ' |ET|\n'
        file.write(line)

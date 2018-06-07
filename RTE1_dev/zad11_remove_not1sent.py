
values_file = open('data/values.txt', 'r')
texts_file = open('data/texts.txt', 'r')
texts_1_sent_file = open('data/texts_1_sent.txt', 'r')
values_1_sent_file = open('data/values_1_sent.txt', 'w')


while True:
    curr_text = texts_file.readline()
    curr_text_1_sent = texts_1_sent_file.readline()
    curr_value = values_file.readline()

    if curr_text == '':
        break

    while True:
        if curr_text == curr_text_1_sent:
            values_1_sent_file.write(curr_value)
            break
        else:
            curr_text = texts_file.readline()
            curr_value = values_file.readline()

values_file.close()
texts_file.close()
texts_1_sent_file.close()
values_1_sent_file.close()
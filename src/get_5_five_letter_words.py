import re
import time
import json
import numpy as np
from collections import Counter
from utilities.utilities import VOWELS, LETTERS, get_vowel_count, get_available_words, log_list

start = time.time()

# 正解単語リストを開く
with open('data/answer-word-list.txt', mode='r') as f:
    answer_word_list = f.read().split('\n')

# 入力可能単語リストを開く
with open('data/valid-word-list.txt', mode='r') as f:
    valid_word_list = f.read().split('\n')
    valid_word_list += answer_word_list

# can only use each letter once
word_list = [word for word in valid_word_list if len(set(word)) == 5]

log_list(word_list, "word_list")

result = []
for word_1 in word_list:
    word_list_for_word_2 = get_available_words(
        word_list, list(word_1))

    for i_2, word_2 in enumerate(word_list_for_word_2):
        word_list_for_word_3 = get_available_words(
            word_list_for_word_2[i_2+1:], list(word_2))

        for i_3, word_3 in enumerate(word_list_for_word_3):
            word_list_for_word_4 = get_available_words(
                word_list_for_word_3[i_3+1:], list(word_3))

            for i_4, word_4 in enumerate(word_list_for_word_4):
                word_list_for_word_5 = get_available_words(
                    word_list_for_word_4[i_4+1:], list(word_4))
                print([word_1, word_2, word_3, word_4])

                for word_5 in enumerate(word_list_for_word_5):
                    words = [word_1, word_2, word_3, word_4, word_5]
                    result.append(sorted(words))


log_list(result, "results are")

elapsed_time = time.time() - start
print("elapsed_time: {0}".format(elapsed_time))

with open('power_quintet.txt', 'w') as f:
    f.write(json.dumps(result))

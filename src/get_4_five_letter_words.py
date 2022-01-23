import re
import time
import json
import numpy as np
from collections import Counter
from utilities.utilities import VOWELS, LETTERS, get_vowel_count, get_available_words, get_unused_letters, log_list

start = time.time()

log_list(LETTERS, "LETTERS")


# 正解単語リストを開く
with open('data/answer-word-list.txt', mode='r') as f:
    answer_word_list = f.read().split('\n')

# 入力可能単語リストを開いて正解単語とマージする
with open('data/valid-word-list.txt', mode='r') as f:
    valid_word_list = f.read().split('\n')
    valid_word_list += answer_word_list

# can only use each letter once
word_list = [word for word in valid_word_list if len(set(word)) == 5]

log_list(word_list, "word_list")

# Are there some words that do not contains any vowels?
# vowel_free_word_list = get_available_words(word_list, VOWELS)
# log_list(vowel_free_word_list, "vowel_free_word_list")

# vowel_free_answer_word_list = get_available_words(answer_word_list, VOWELS)
# log_list(vowel_free_answer_word_list, "vowel_free_answer_word_list")

# 変な単語が多かったため、common wordに絞る
with open('data/google-10000-english-no-swears.txt', mode='r') as f:
    google_word_list = f.read().split('\n')
    word_list = [
        word for word in word_list if word in google_word_list]
    log_list(word_list, "common_word_list")

# 探索の効率化のため、母音を使わない単語は無視し、探索を「母音を2つ含む単語から始められる様にする」
# double_vowel_word_list = [
#     word for word in common_word_list if get_vowel_count(word) == 2]
# log_list(double_vowel_word_list, "double-vowel word list")

# single_vowel_word_list = [
#     word for word in common_word_list if get_vowel_count(word) == 1]
# log_list(single_vowel_word_list, "single-vowel word list")

# BAD CODE EXAMPLE
# result = [
#     (word1, word2, word3, word4)
#     for word1 in double_vowel_word_list
#     for word2 in single_vowel_word_list
#     for word3 in single_vowel_word_list
#     for word4 in single_vowel_word_list
#     if len(set(word1+word2+word3+word4)) == 20
# ]

# 4重ループは心苦しいが、途中でループする配列が空になることが多いため現状は問題なさそう
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

            for word_4 in word_list_for_word_4:
                words = [word_1, word_2, word_3, word_4]
                result.append(sorted(words))


log_list(result, "results are")


def get_letters_in_frequency():
    # 答え単語で使われる順で並び替える
    answer_letters = ''.join(answer_word_list)

    frequency_dict = {
        letter: answer_letters.count(letter) for letter in LETTERS
    }

    return sorted(
        LETTERS,
        key=lambda letter: frequency_dict[letter],
        reverse=True
    )


LETTERS_IN_FREQENCY = get_letters_in_frequency()
log_list(LETTERS_IN_FREQENCY, 'LETTERS_IN_FREQENCY')


def get_freqency_score(words):
    unused_letters = get_unused_letters(words)
    return sum([LETTERS_IN_FREQENCY.index(letter) ** 2 for letter in ''.join(words)])


result_sorted_by_frequency = sorted(
    result,
    key=lambda words: get_freqency_score(words),
)

elapsed_time = time.time() - start
print("elapsed_time: {0}".format(elapsed_time))

with open('power_quartet.json', 'w') as f:
    f.write(json.dumps(result))

with open('power_quartet_in_frequency.json', 'w') as f:
    f.write(json.dumps(result_sorted_by_frequency))

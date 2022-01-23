import numpy as np
import pandas as pd
import json
from utilities.utilities import LETTERS

with open('data/answer-word-list.txt', mode='r') as f:
    answer_word_list = f.read().split('\n')
    answer_len = len(answer_word_list)

with open('power_quartet.json', mode='r') as f:
    power_quartet = json.load(f)


def get_feedback(answer: str, inputs: list[str]):
    # inputは同じ文字を含まない単語と仮定している
    # 例えばknollのような入力には対応していない
    green = [''] * 5
    yellow = [[], [], [], [], []]
    gray = []

    for input in inputs:
        answer_list = list(answer)
        for i, letter in enumerate(input):
            if letter == answer[i]:
                green[i] = letter

            elif letter in answer:
                answer_list.remove
                yellow[i].append(letter)

            else:
                gray.append(letter)

    return {
        'green': green,
        'yellow': yellow,
        'gray': gray,
    }


def get_remained_words(word_list: list[str], feedback):
    green = feedback['green']
    yellow = feedback['yellow']
    gray = feedback['gray']

    result = []
    for word in word_list:
        if all(
            green[i] == word[i] or green[i] == ''
            for i in range(5)
        ) and all(
            letter in word and letter != word[i]
            for i in range(5)
            for letter in yellow[i]
        ) and all(
            letter not in word
            for letter in gray
        ):
            result.append(word)

    return result


def get_win_rate(quartet):
    remained_words_list = [
        get_remained_words(answer_word_list, get_feedback(answer, quartet))
        for answer in answer_word_list
    ]
    len_list = list(map(lambda words: len(words), remained_words_list))

    less_than_2 = list(filter(lambda length: length <= 2, len_list))
    less_than_1 = list(filter(lambda length: length <= 1, less_than_2))
    mean = np.mean([
        len(remained_words) for remained_words in remained_words_list
    ])

    return {
        '<= 2': len(less_than_2) / answer_len,
        '<= 1': len(less_than_1) / answer_len,
        'mean': mean
    }


def main():
    # 各カルテットに対し、remained_wordsの平均と、2個以下である確率を計算
    win_rate_list = {
        ', '.join(quartet): get_win_rate(quartet) for quartet in power_quartet
    }

    sorted_by_less_than_2 = sorted(
        win_rate_list.items(),
        key=lambda quartet: quartet[1]['<= 2'],
        reverse=True
    )

    with open('win_rate.json', 'w') as f:
        f.write(json.dumps(sorted_by_less_than_2))

    sorted_by_mean = sorted(
        win_rate_list.items(),
        key=lambda quartet: quartet[1]['mean'],
    )

    with open('mean_score.json', 'w') as f:
        f.write(json.dumps(sorted_by_mean))

    #########################################
    # averageが良かった組に対し、どんなワードが残るか計算
    # with open('win_rate.json', mode='r') as f:
    #     win_rate = json.load(f)

    # target = win_rate[0][0]
    # print(target)

    # remained_words = [
    #     get_remained_words(answer_word_list, get_feedback(
    #         answer, target.split(', ')
    #     )) for answer in answer_word_list
    # ]
    # average_length = list(
    #     map(lambda words: len(words), remained_words))
    # df = pd.DataFrame(average_length, columns=["The num of remained words"])
    # print(df.describe())

    # less_than_2 = list(filter(lambda length: length <= 2, average_length))
    # less_than_1 = list(filter(lambda length: length <= 1, average_length))
    # more_than_3 = list(filter(lambda words: len(words)
    #                    >= 3, remained_words))

    # print('<= 2 words: ', len(less_than_2) / len(average_length))
    # print('just one words: ', len(less_than_1) / len(average_length))

    # print('more than 3: ',  len(more_than_3), more_than_3)

    ###########################################
    # 各ワードに対し、remained_wordsの長さの期待値を計算する
    # 入力可能単語リストを開く
    # with open('data/valid-word-list.txt', mode='r') as f:
    #     valid_word_list = f.read().split('\n')
    #     valid_word_list += answer_word_list
    #     word_list = [word for word in valid_word_list if len(set(word)) == 5]

    # # 変な単語が多かったため、common wordに絞る
    # with open('data/google-10000-english-no-swears.txt', mode='r') as f:
    #     google_word_list = f.read().split('\n')
    #     ord_list = [word for word in word_list if word in google_word_list]

    # average_remained_words = {
    #     word: get_average_remaind_words([word]) for word in word_list
    # }

    # sorted_by_key = sorted(
    #     average_remained_words.items(),
    #     key=lambda quartet: quartet[1],
    # )

    # with open('average.json', 'w') as f:


if __name__ == "__main__":
    main()

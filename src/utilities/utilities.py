import string

VOWELS = ["a", "e", "i", "o", "u"]

# List of all characters from a to z.
LETTERS = list(string.ascii_lowercase)


def get_vowel_count(word: str):
    return sum([word.count(vowel) for vowel in VOWELS])


def get_available_words(word_list: list[str], unavailable_letters: list[str]):
    # word_listからunavailable_lettersで使っている文字を含む単語を除いたリストを返す
    return [word for word in word_list if all(letter not in word for letter in unavailable_letters)]


def log_list(lst, caption: str):
    print("{0}: {1}, len: {2}\n".format(caption, lst[:10], len(lst)))


def get_unused_letters(words):
    return [letter for letter in LETTERS if letter not in ''.join(words)]

My attempt for searching useful words for the game [Wordle](https://www.powerlanguage.co.uk/wordle/). 

**This repo is only for reference purposes.**

# Usage
1. Put [this file](https://github.com/first20hours/google-10000-english/blob/master/google-10000-english-no-swears.txt) in data dir as `google-10000-english-no-swears.txt`
2. Put a dictionary files of your choice in data dir as `answer-word-list.txt` and `valid-word-list.txt`. Each word in them must be delimited by newlines.
3. Run `src/get_4_five_letter_words.py` to get the useful set of words(it will take some time).
4. Then run `calculate_expected_remained_answer.py` to calculate scores of the words(it will take a long long time).

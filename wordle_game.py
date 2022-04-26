import wordle as w
import re

class WordleGame:
    def __init__(self, word):
        if not len(word) == w.Wordle.WORD_LENGTH:
            raise Exception(f'word {word} should be {w.Wordle.WORD_LENGTH} characters.')
        if not bool(re.fullmatch('^[a-z]{5}',word)):  # 5 lowercase characters only
            raise Exception(f'word {word} had unexpected characters.')
        self.word = word

    def get_result(self,guess):
        is_win = guess == self.word
        result = [w.LetterResultCode.GRAY] * w.Wordle.WORD_LENGTH  # default to gray, if not changed below.
        word_copy = list(self.word)
        guess_copy = list(guess)
        for i in range(w.Wordle.WORD_LENGTH):
            if guess[i] == word_copy[i]:
                result[i] = w.LetterResultCode.GREEN
                word_copy[i] = None
                guess_copy[i] = None
        for i in range(w.Wordle.WORD_LENGTH):
            if not guess_copy[i] is None:
                if guess_copy[i] in word_copy:
                    result[i] = w.LetterResultCode.YELLOW
                    first_index = word_copy.index(guess[i])
                    word_copy[first_index] = None
                    guess_copy[i] = None  # to make debugging clearer
        return is_win, result



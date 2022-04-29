import letters_included as li
import word_list as wl

class LetterResultCode:
    GRAY = 0
    YELLOW = 1
    GREEN = 2

class SuggestedGuessType:
    RANDOM = 0
    EXPECTED_VALUE_GREEN_LOW = 1
    EXPECTED_VALUE_GREEN = 2
    EXPECTED_VALUE_GREEN_AND_YELLOW_25 = 3
    EXPECTED_VALUE_GREEN_AND_YELLOW_50 = 4
    EXPECTED_VALUE_GREEN_AND_YELLOW_75 = 5
    EXPECTED_VALUE_YELLOW = 6


class Wordle:
    WORD_LENGTH = 5
    NUM_LETTERS = 26
    NUM_TURNS_ALLOWED = 6

    @staticmethod
    def character_index(char):
        letter_index = ord(char.lower()) - ord('a')  # a is zero, b is 1 etc
        if letter_index > (Wordle.NUM_LETTERS - 1) or letter_index < 0:
            raise Exception(f'character {char} was out of the expected range.')
        else:
            return letter_index

    def __init__(self, words, suggested_guess_type=SuggestedGuessType.EXPECTED_VALUE_GREEN):
        self.word_list = wl.WordList(len(words))
        for word in words:
            self.word_list.add_word(word)
        self.reset(suggested_guess_type)

    def reset(self, suggested_guess_type=SuggestedGuessType.EXPECTED_VALUE_GREEN):
        #self.guesses = []
        #self.results = []
        self.letters_included = li.LettersIncluded()
        self.word_list.reset()
        self.suggested_guess_type = suggested_guess_type
        self.filters_applied = False

    def record_guess(self, guess, result_array):
        #self.guesses.append(guess)
        #self.results.append(result_array)
        self.letters_included.record_guess(guess, result_array)
        self.filters_applied = False

    def apply_filters(self):
        if not self.filters_applied:
            self.word_list.apply_filters(self.letters_included)
            self.filters_applied = True

    def get_matching_words(self):
        self.apply_filters()
        return self.word_list.get_matching_words()

    def get_suggested_guesses(self, num_guesses):
        self.apply_filters()
        return self.word_list.get_suggested_guesses(self.suggested_guess_type, num_guesses)
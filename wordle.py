import letters_included as li
import word_list as wl

class LetterResultCode:
    GRAY = 0
    YELLOW = 1
    GREEN = 2

class SuggestedGuessType:
    RANDOM = 0
    HIGHEST_FREQUENCY = 1
    LOWEST_FREQUENCY = 2

class Wordle:
    WORD_LENGTH = 5
    NUM_LETTERS = 26

    @staticmethod
    def character_index(char):
        letter_index = ord(char.lower()) - ord('a')  # a is zero, b is 1 etc
        if letter_index > (Wordle.NUM_LETTERS - 1) or letter_index < 0:
            raise Exception(f'character {char} was out of the expected range.')
        else:
            return letter_index

    def __init__(self, words, suggested_guess_type=SuggestedGuessType.HIGHEST_FREQUENCY):
        self.word_list = wl.WordList(len(words))
        for word in words:
            self.word_list.add_word(word)
        self.reset(suggested_guess_type)

    def reset(self, suggested_guess_type=SuggestedGuessType.HIGHEST_FREQUENCY):
        self.guesses = []
        self.results = []
        #self.letters_not_included = set()
        self.letters_included = li.LettersIncluded()
        #self.pattern = list('*****')
        self.word_list.reset()
        self.suggested_guess_type = suggested_guess_type
        self.filters_applied = False

    def record_guess(self, guess, result_array):
        self.guesses.append(guess)
        self.results.append(result_array)
        self.letters_included.record_guess(guess, result_array)
        # for i in range(self.WORD_LENGTH):
        #     if result_each_letter[i] == LetterResultCode.GREEN:
        #         self.letters_included.add(guess_str[i], i, LetterResultCode.GREEN)
        # for i in range(self.WORD_LENGTH):
        #     if result_each_letter[i] == LetterResultCode.YELLOW:
        #         self.letters_included.add(guess_str[i], i, LetterResultCode.YELLOW)
        # for i in range(self.WORD_LENGTH):
        #     if result_each_letter[i] == LetterResultCode.GRAY:
        #         self.letters_included.add(guess_str[i], i, LetterResultCode.GRAY)
            #
            # letter = guess_str[i]
            # result = result_each_letter[i]
            # if result == LetterResultCode.GREEN:
            #     self.pattern[i] = letter
            # elif result == LetterResultCode.YELLOW:
            #     self.letters_included.add(letter, i)
            # elif result == LetterResultCode.GRAY:
            #     if not letter in self.letters_included.letters:
            #         #if a letter is repeated in the guess but only in the real word once,
            #         # it will be yellow/green in the leftmost position, and gray in the other position.
            #         # this isn't handled yet.
            #         self.letters_not_included.add(letter)
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
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

    def __init__(self, words, suggested_guess_type=SuggestedGuessType.HIGHEST_FREQUENCY):
        self.word_list = wl.WordList(len(words), Wordle.WORD_LENGTH)
        for word in words:
            self.word_list.add_word(word)
        self.reset(suggested_guess_type)

    def reset(self, suggested_guess_type=SuggestedGuessType.HIGHEST_FREQUENCY):
        self.guesses = []
        self.results = []
        self.letters_not_included = set()
        self.letters_included = li.LettersIncluded()
        self.pattern = list('*****')
        self.word_list.reset()
        self.suggested_guess_type = suggested_guess_type

    def record_guess(self, guess, result_each_letter):
        guess_str = guess
        self.guesses.append(guess_str)
        self.results.append(result_each_letter)
        for i in range(5):
            letter = guess_str[i]
            result = result_each_letter[i]
            if result == LetterResultCode.GREEN:
                self.pattern[i] = letter
            elif result == LetterResultCode.YELLOW:
                self.letters_included.add(letter, i)
            elif result == LetterResultCode.GRAY:
                self.letters_not_included.add(letter)

    def get_matching_words(self):
        self.word_list.apply_filters(self.pattern, self.letters_included, self.letters_not_included)
        matching_words = self.word_list.get_matching_words()
        if len(matching_words) == 0:
            raise Exception(f'No words matched pattern {self.pattern} and matched the other criteria.')
        print(f'{len(matching_words)} words matched pattern {self.pattern}. The first word was {matching_words[0]}')
        self.matching_words = matching_words
        suggested_guess = self.get_suggested_guess()
        return suggested_guess, matching_words

    def get_suggested_guess(self):
        return self.word_list.get_suggested_word(self.suggested_guess_type)
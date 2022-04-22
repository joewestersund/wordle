import letters_included as li
import word_list

class Wordle:
    WORD_LENGTH = 5

    LETTER_RESULT_GRAY = 0
    LETTER_RESULT_YELLOW = 1
    LETTER_RESULT_GREEN = 2

    def __init__(self, words):
        self.reset()
        self.word_list = word_list.WordList(len(words), Wordle.WORD_LENGTH)
        for word in words:
            self.word_list.add_word(word)

    def reset(self):
        self.guesses = []
        self.results = []
        self.letters_not_included = set()
        self.letters_included = li.LettersIncluded()
        self.pattern = list('*****')

    def record_guess(self, guess, result_each_letter):
        guess_str = guess
        self.guesses.append(guess_str)
        self.results.append(result_each_letter)
        for i in range(5):
            letter = guess_str[i]
            result = result_each_letter[i]
            if result == Wordle.LETTER_RESULT_GREEN:
                self.pattern[i] = letter
            elif result == Wordle.LETTER_RESULT_YELLOW:
                self.letters_included.add(letter, i)
            elif result == Wordle.LETTER_RESULT_GRAY:
                self.letters_not_included.add(letter)

    def get_remaining_words(self):
        matching_words = self.word_list.words_matching_pattern(self.pattern, self.letters_included, self.letters_not_included)
        if len(matching_words) == 0:
            raise Exception(f'No words matched pattern {self.pattern} and matched the other criteria.')
        print(f'{len(matching_words)} words matched pattern {self.pattern}. The first word was {matching_words[0]}')
        suggested_guess = matching_words[0]
        return suggested_guess, matching_words
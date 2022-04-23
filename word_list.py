import numpy as np
import wordle as w
import random

class WordList:

    @staticmethod
    def character_index(char):
        letter_index = ord(char.lower()) - ord('a') # a is zero, b is 1 etc
        if letter_index > 25 or letter_index < 0:
            raise Exception(f'character {char} was out of the expected range.')
        else:
            return letter_index

    def __init__(self, num_words, num_characters):
        self.num_characters = num_characters
        self.word_array = np.zeros((5, 26, num_words), dtype=np.bool)
        self.words = np.empty(num_words, dtype=np.dtype(f'S{num_characters}'))
        self.reset()

    def reset(self):
        self.current_word_index = 0
        self.matching_indices = []

    def add_word(self, word):
        if len(word) == self.num_characters:
            for i in range(self.num_characters):
                letter = word[i]
                self.word_array[i, WordList.character_index(letter), self.current_word_index] = 1
            self.words[self.current_word_index] = word
            self.current_word_index += 1
        else:
            raise Exception(f'word {word} did not have 5 characters.')

    def apply_filters(self, pattern, letters_included, letters_not_included):
        if len(pattern) != self.num_characters:
            raise Exception(f'pattern {pattern} did not have {self.num_characters} characters.')

        num_criteria = 2
        criteria_array = np.ones((self.num_characters, 26, num_criteria), dtype=np.bool)

        # first criteria is to check for words that match pattern
        criteria_index = 0
        for i in range(self.num_characters):
            letter = pattern[i]
            if letter == "*":
                criteria_array[i, :, criteria_index] = np.zeros(26, dtype=np.bool)  # all zeros, so no letter would be an error
            else:
                letter_index = WordList.character_index(letter)
                criteria_array[i, letter_index, criteria_index] = 0  # only matching letter would not trigger an error

        # next criteria are to check for letters that should not be in certain positions, or included at all
        # next criteria are to check for letters that should not be in certain positions
        criteria_index = 1
        criteria_array[:, :, criteria_index] = np.zeros((self.num_characters, 26),
                                                        dtype=np.bool)  # all zeros, so no letters would be an error
        for letter, not_in_this_position_set in letters_included.letters.items():
            letter_index = WordList.character_index(letter)
            for not_in_this_position in not_in_this_position_set:
                criteria_array[not_in_this_position, letter_index, criteria_index] = 1  # this letter should not be in this position

        # check for letters that should not be included at all
        for letter in letters_not_included:
            letter_index = WordList.character_index(letter)
            criteria_array[:, letter_index, criteria_index] = 1 # this letter should not be in any position

        criteria_match = np.einsum('ijk,ijm->m', criteria_array, self.word_array)

        # check for letters that must be included somewhere
        criteria_array2 = np.zeros((self.num_characters, 26), dtype=np.int)
        num_letters_must_be_included = len(letters_included.letters)
        for letter in letters_included.letters:
            letter_index = WordList.character_index(letter)
            criteria_array2[:, letter_index] = 1  # this letter should not be in this position

        criteria_match2 = np.einsum('ij,ijm->m', criteria_array2, self.word_array)

        matching_indices = (criteria_match == 0) & (criteria_match2 >= num_letters_must_be_included)
        self.matching_indices = matching_indices # save this for future questions about this list

    def get_matching_words(self):
        matching_words = self.words[self.matching_indices]
        return matching_words.astype('U13')  # convert from byte array to strings

    def get_suggested_word(self, suggested_guess_type):
        if suggested_guess_type == w.SuggestedGuessType.RANDOM:
            matching_words = self.words[self.matching_indices]
            num_choices = len(matching_words)
            random_index = random.randint(0, num_choices-1)
            return matching_words[random_index].astype('U13')
        else:
            matching_rows_of_word_array = self.word_array[self.matching_indices]
            frequencies = np.average(matching_rows_of_word_array, axis=2)
            frequency_match = np.einsum('ij,ijm->m', frequencies, self.word_array)
            if suggested_guess_type == w.SuggestedGuessType.LOWEST_FREQUENCY:
                index = np.argmin(frequency_match)
                return self.words[index].astype('U13')
            elif suggested_guess_type == w.SuggestedGuessType.HIGHEST_FREQUENCY:
                index = np.argmax(frequency_match)
                return self.words[index].astype('U13')
            else:
                raise Exception(f'Suggested guess type {self.suggested_guess_type} was not recognized.')
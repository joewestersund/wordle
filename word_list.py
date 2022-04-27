import numpy as np
import wordle as w
import random
import letters_included as li

class WordList:

    def __init__(self, num_words):
        self.word_array = np.zeros((5, 26, num_words), dtype=np.bool)
        self.words = np.empty(num_words, dtype=np.dtype(f'S{w.Wordle.WORD_LENGTH}'))
        self.reset()

    def reset(self):
        self.current_word_index = 0
        self.matching_indices = []

    def add_word(self, word):
        if len(word) == w.Wordle.WORD_LENGTH:
            for i in range(w.Wordle.WORD_LENGTH):
                letter = word[i]
                self.word_array[i, w.Wordle.character_index(letter), self.current_word_index] = 1
            self.words[self.current_word_index] = word
            self.current_word_index += 1
        else:
            raise Exception(f'word {word} did not have 5 characters.')

    def apply_filters(self, letters_included):
        count_each_letter = np.sum(self.word_array, axis = 0)

        criteria_by_letter = (count_each_letter == letters_included.copies_of_this_letter) | \
                             ((count_each_letter >= letters_included.copies_of_this_letter) & letters_included.could_be_more_copies)
        criteria_1 = np.all(criteria_by_letter, axis=0)

        criteria_by_position_and_letter = (self.word_array == letters_included.in_this_position) | (letters_included.in_this_position == li.LettersIncluded.VALUE_IF_UNKNOWN)
        criteria_2 = np.all(criteria_by_position_and_letter, axis=(0,1))
        matching_indices = (criteria_1 & criteria_2)
        self.matching_indices = matching_indices  # save this for future questions about this list

    def get_matching_words(self):
        matching_words = self.words[self.matching_indices]
        return matching_words.astype('U13')  # convert from byte array to strings

    def get_suggested_guesses(self, suggested_guess_type, num_guesses):
        matching_words = self.words[self.matching_indices]
        if suggested_guess_type == w.SuggestedGuessType.RANDOM:
            num_guesses_to_return = min(len(matching_words), num_guesses)
            random_words = np.random.choice(matching_words, num_guesses_to_return)
            return random_words.astype('U13')
        else:
            matching_rows_of_word_array = self.word_array[:, :, self.matching_indices]
            num_guesses_to_return = min(len(matching_rows_of_word_array), num_guesses)
            frequencies_green = np.nanmean(matching_rows_of_word_array, axis=2)
            frequency_sum_green = np.einsum('ij,ijm->m', frequencies_green, matching_rows_of_word_array)

            word_contains_letter = np.max(matching_rows_of_word_array, axis=0)
            frequencies_yellow = np.nanmean(word_contains_letter, axis=1)
            frequency_sum_yellow = np.einsum('j,jm->m', frequencies_yellow, word_contains_letter)

            if suggested_guess_type == w.SuggestedGuessType.EXPECTED_VALUE_GREEN_LOW:
                scores = -1 * frequency_sum_green
            if suggested_guess_type == w.SuggestedGuessType.EXPECTED_VALUE_GREEN:
                scores = frequency_sum_green
            elif suggested_guess_type == w.SuggestedGuessType.EXPECTED_VALUE_YELLOW:
                scores = frequency_sum_yellow
            elif suggested_guess_type == w.SuggestedGuessType.EXPECTED_VALUE_GREEN_AND_YELLOW:
                scores = frequency_sum_green + frequency_sum_yellow
            else:
                raise Exception(f'Suggested guess type {self.suggested_guess_type} was not recognized.')

            indices = np.argsort(scores)
            selected_indices = np.flip(indices[-num_guesses_to_return:])  # last x elements, reordered so highest rated is first
            suggested_guesses = matching_words[selected_indices].astype('U13')
            highest_word_score = scores[indices][-1]
            lowest_word_score = scores[indices][0]
            suggested_guess_scores = self.convert_to_percentage_scale(scores[selected_indices], highest_word_score, lowest_word_score)
            return suggested_guesses, suggested_guess_scores

    def convert_to_percentage_scale(self, scores, high, low):
        return 100 * (scores - low) / (high - low)
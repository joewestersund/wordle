import math

import numpy as np

import letters_included
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

    def apply_filters(self, letters_included, save_result=True):
        count_each_letter = np.sum(self.word_array, axis = 0)

        criteria_by_letter = (count_each_letter == letters_included.copies_of_this_letter) | \
                             ((count_each_letter >= letters_included.copies_of_this_letter) & letters_included.could_be_more_copies)
        criteria_1 = np.all(criteria_by_letter, axis=0)

        criteria_by_position_and_letter = (self.word_array == letters_included.in_this_position) | (letters_included.in_this_position == li.LettersIncluded.VALUE_IF_UNKNOWN)
        criteria_2 = np.all(criteria_by_position_and_letter, axis=(0,1))
        matching_indices = (criteria_1 & criteria_2)
        if save_result:
            self.matching_indices = matching_indices  # save this for future questions about this list
            self.letters_included = letters_included
        return matching_indices

    def get_matching_words(self):
        matching_words = self.words[self.matching_indices]
        return matching_words.astype('U13')  # convert from byte array to strings

    def get_suggested_guesses(self, suggested_guess_type, num_guesses):
        matching_words = self.words[self.matching_indices]
        if suggested_guess_type == w.SuggestedGuessType.RANDOM:
            num_guesses_to_return = min(len(matching_words), num_guesses)
            random_words = np.random.choice(matching_words, num_guesses_to_return)
            scores = [None] * num_guesses
            return random_words.astype('U13'), scores
        elif suggested_guess_type == w.SuggestedGuessType.ENTROPY:
            num_possible_results = 3**w.Wordle.WORD_LENGTH
            num_matching_words = len(matching_words)
            entropy_sums = np.zeros(num_matching_words, np.float)
            for word_index in range(num_matching_words):
                guess = matching_words[word_index].astype('U13')
                print(f'calculating entropy for guess {guess}, {word_index}/{num_matching_words}')
                for result_number in range(num_possible_results):
                    r = result_number
                    result_array = [None for x in range(w.Wordle.WORD_LENGTH)] # blank array
                    for i in range(w.Wordle.WORD_LENGTH):
                        r, result_array[i] = divmod(r, 3)
                    #li = letters_included.LettersIncluded()
                    li = self.letters_included.copy()  # need a deep copy of this
                    li.record_guess(guess, result_array)
                    matching_indices = self.apply_filters(li, False)
                    prob = len(self.words[matching_indices]) / num_matching_words
                    if prob > 0 and prob < 1:
                        entropy_sums[word_index] -= prob * math.log2(prob)
            ordered_indices = np.argsort(entropy_sums)
            low = entropy_sums[ordered_indices[0]]
            high = entropy_sums[ordered_indices[-1]]
            top_indices = np.flip(ordered_indices[-1 * num_guesses :]) # top indices, reordered so highest entropy is first
            scores = entropy_sums[top_indices]
            suggested_guess_scores = self.convert_to_percentage_scale(scores, high, low)
            suggested_guesses = matching_words[top_indices].astype('U13')
            return suggested_guesses, suggested_guess_scores
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
                scores = 1 * frequency_sum_green + 0 * frequency_sum_yellow
            elif suggested_guess_type == w.SuggestedGuessType.EXPECTED_VALUE_GREEN_AND_YELLOW_25:
                scores = 0.75 * frequency_sum_green + 0.25 * frequency_sum_yellow
            elif suggested_guess_type == w.SuggestedGuessType.EXPECTED_VALUE_GREEN_AND_YELLOW_50:
                scores = 0.5 * frequency_sum_green + 0.5 * frequency_sum_yellow
            elif suggested_guess_type == w.SuggestedGuessType.EXPECTED_VALUE_GREEN_AND_YELLOW_75:
                scores = 0.25 * frequency_sum_green + 0.75 * frequency_sum_yellow
            elif suggested_guess_type == w.SuggestedGuessType.EXPECTED_VALUE_YELLOW:
                scores = 0 * frequency_sum_green + 1 * frequency_sum_yellow
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
        if high == low:
            return 100 * scores / scores
        else:
            return 100 * (scores - low) / (high - low)
import numpy as np
import wordle as w

class LettersIncluded:
    VALUE_IF_UNKNOWN = -1

    def __init__(self):
        self.copies_of_this_letter = np.zeros((w.Wordle.NUM_LETTERS, 1), np.int)

        # true if the word could have >= copies_of_this_letter_present copies of this letter
        # false if the word must have exactly copies_of_this_letter_present copies of this letter
        self.could_be_more_copies = np.ones((w.Wordle.NUM_LETTERS,1), np.bool)

        # VALUE_IF_UNKNOWN if it's unknown if this letter could be in this position
        # zero if this letter is not in this position
        # one if this letter is in this position
        self.in_this_position = np.empty((w.Wordle.WORD_LENGTH, w.Wordle.NUM_LETTERS, 1), dtype=np.int)
        self.in_this_position.fill(self.VALUE_IF_UNKNOWN)

    def record_guess(self, guess, result_array):
        # need to add first all the green letters, then all the yellow letters, then the gray letters.
        copies_of_this_letter_this_guess = np.zeros((w.Wordle.NUM_LETTERS, 1), np.int)
        for i in range(w.Wordle.WORD_LENGTH):
            letter_index = w.Wordle.character_index(guess[i])
            if result_array[i] == w.LetterResultCode.GREEN:
                copies_of_this_letter_this_guess[letter_index] += 1
                self.in_this_position[i, letter_index] = 1  # this letter is definitely here
        for i in range(w.Wordle.WORD_LENGTH):
            letter_index = w.Wordle.character_index(guess[i])
            if result_array[i] == w.LetterResultCode.YELLOW:
                copies_of_this_letter_this_guess[letter_index] += 1
                self.in_this_position[i, letter_index] = 0  # this letter is definitely not here
        for i in range(w.Wordle.WORD_LENGTH):
            letter_index = w.Wordle.character_index(guess[i])
            if result_array[i] == w.LetterResultCode.GRAY:
                self.could_be_more_copies[letter_index] = False  # there aren't additional copies of this letter, or this would be yellow.
                self.in_this_position[i, letter_index] = 0  # this letter is definitely not here
        indices_to_update = (copies_of_this_letter_this_guess > self.copies_of_this_letter)
        self.copies_of_this_letter[indices_to_update] = copies_of_this_letter_this_guess[indices_to_update]
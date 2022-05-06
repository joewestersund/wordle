import numpy as np
import wordle as w

class ImpossibleResultError(Exception):
    pass

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

    def copy(self):
        li = LettersIncluded()
        li.copies_of_this_letter = self.copies_of_this_letter.copy()
        li.could_be_more_copies = self.could_be_more_copies.copy()
        li.in_this_position = self.in_this_position.copy()
        return li

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
                if self.in_this_position[i, letter_index] == 1:
                    raise ImpossibleResultError
                self.in_this_position[i, letter_index] = 0  # this letter is definitely not here
        for i in range(w.Wordle.WORD_LENGTH):
            letter_index = w.Wordle.character_index(guess[i])
            if result_array[i] == w.LetterResultCode.GRAY:
                self.could_be_more_copies[letter_index] = False  # there aren't additional copies of this letter, or this would be yellow.
                if self.in_this_position[i, letter_index] == 1:
                    raise ImpossibleResultError
                self.in_this_position[i, letter_index] = 0  # this letter is definitely not here
                if self.copies_of_this_letter[letter_index][0] > copies_of_this_letter_this_guess[letter_index][0]:
                    # this letter wouldn't be gray if it's in the word
                    raise ImpossibleResultError
        for i in range(0, w.Wordle.WORD_LENGTH):
            # check for words with multiple copies of same letter, with earlier copy gray and later copy yellow.
            letter_index1 = w.Wordle.character_index(guess[i])
            if result_array[i] == w.LetterResultCode.GRAY:
                for j in range (i+1, w.Wordle.WORD_LENGTH):
                    letter_index2 = w.Wordle.character_index(guess[j])
                    if letter_index1 == letter_index2 and result_array[j] == w.LetterResultCode.YELLOW:
                        # can't have a gray for one letter, and then a yellow for that same letter later.
                        raise ImpossibleResultError
        indices_to_update = (copies_of_this_letter_this_guess > self.copies_of_this_letter)
        self.copies_of_this_letter[indices_to_update] = copies_of_this_letter_this_guess[indices_to_update]
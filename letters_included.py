class LettersIncluded:
    def __init__(self):
        self.letters = {}
        self.num_criteria = 0

    def add(self, letter, not_in_this_position):
        if letter not in self.letters:
            self.letters[letter] = set()
        if not_in_this_position not in self.letters[letter]:
            self.num_criteria += 1
            self.letters[letter].add(not_in_this_position)

    def num_letters(self):
        return len(self.letters)

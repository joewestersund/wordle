import wordle as w

class WordleGame:

    def __init__(self, word):
        self.word = word

    def get_result(self,guess):
        is_win = guess == self.word
        result = []
        for i in range(len(guess)):
            if guess[i] == self.word[i]:
                result.append(w.LetterResultCode.GREEN)
            elif guess[i] in self.word:
                result.append(w.LetterResultCode.YELLOW)
            else:
                result.append(w.LetterResultCode.GRAY)
        return is_win, result



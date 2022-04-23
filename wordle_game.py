import wordle as w

class WordleGame:

    class GameMode:
        REGULAR = 0
        HARD = 1

    def __init__(self, word, game_mode=GameMode.REGULAR):
        self.word == word
        self.game_mode = game_mode

    def get_result(self,guess):
        result = ' ' * 5 # five spaces
        for i in range(len(guess)):
            if guess[i] == self.word[i]:
                result[i] = w.LetterResultCode.GREEN
            elif guess[i] in self.word
                result[i] = w.LetterResultCode.YELLOW
            else:
                result[i] = w.LetterResultCode.GRAY
        return result



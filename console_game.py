import wordle as w

class ConsoleGame:

    def play_game(self, wordle):
        gr = w.LetterResultCode.GREEN

        suggested_guesses = wordle.get_suggested_guesses(1)
        for i in range(6):
            next_guess, result = self.get_guess_and_result(suggested_guesses[0])
            if result == [gr, gr, gr, gr, gr]:
                print(f'The word was {next_guess}, congratulations, you got it in {i + 1} guesses!')
                break
            wordle.record_guess(next_guess, result)
            matching_words = wordle.get_matching_words()
            if len(matching_words) > 0:
                print(f'There were {len(matching_words)} matching words.')
            else:
                print(f'No words matched those filter criteria in our word list. Good luck!')
                break
            suggested_guesses = wordle.get_suggested_guesses(10)
            print(f'Suggested guesses: {", ".join(suggested_guesses)}')


    def get_guess_and_result(self, suggested_guess):
        print(f'suggested guess: {suggested_guess}')
        while (True):
            print(f'your guess? leave empty to use suggested guess')
            guess = input()
            if len(guess) == 0:
                guess = suggested_guess
                break
            elif len(guess) == 5:
                break
        print(f'you guessed {guess}')

        while (True):
            print(f'result? example: g,g,gr,y,gr')
            result = input()
            result_split = result.split(",")
            if len(result_split) == 5:
                valid = True
                valid_strings = {'g': 0, 'y': 1, 'gr': 2}
                result_array = []
                for str in result_split:
                    if str in valid_strings:
                        result_array.append(valid_strings[str])
                    else:
                        valid = False
                if valid:
                    return guess, result_array
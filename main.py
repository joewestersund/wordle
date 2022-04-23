import numpy as np
import read_data as rd
import wordle as w

def main():
    word_length = 5
    words = rd.read_word_file('wordlist.10000.txt', word_length)

    g = w.LetterResultCode.GRAY
    y = w.LetterResultCode.YELLOW
    gr = w.LetterResultCode.GREEN

    guess_type = w.SuggestedGuessType.RANDOM
    wordle = w.Wordle(words, guess_type)

    success = False
    suggested_guess = 'trans' # wordle.get_suggested_guess() # 'trans'
    for i in range(6):
        next_guess, result = get_guess_and_result(suggested_guess)
        if result == [gr, gr, gr, gr, gr]:
            print(f'The word was {next_guess}, congratulations, you got it in {i+1} guesses!')
            success = True
            break
        wordle.record_guess(next_guess, result)
        suggested_guess, matching_words = wordle.get_matching_words()
    if not success:
        print(f'Too bad, you didn''t get it')

def get_guess_and_result(suggested_guess):
    print(f'suggested guess: {suggested_guess}')
    while(True):
        print(f'your guess? leave empty to use suggested guess')
        guess = input()
        if len(guess) == 0:
            guess = suggested_guess
            break
        elif len(guess) == 5:
            break
    print(f'you guessed {guess}')

    while(True):
        print(f'result? example: g,g,gr,y,gr')
        result = input()
        result_split = result.split(",")
        if len(result_split) == 5:
            valid = True
            valid_strings = {'g':0, 'y':1, 'gr':2}
            result_array = []
            for str in result_split:
                if str in valid_strings:
                    result_array.append(valid_strings[str])
                else:
                    valid = False
            if valid:
                return guess, result_array


if __name__ == '__main__':
    main()




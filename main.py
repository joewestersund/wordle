import numpy as np
import read_data as rd
import wordle as w

def main():
    word_length = 5
    #words = rd.read_word_file('wordlist.10000.txt', word_length)
    words = rd.read_word_file('wlist_match10.txt', word_length)

    g = w.LetterResultCode.GRAY
    y = w.LetterResultCode.YELLOW
    gr = w.LetterResultCode.GREEN

    #guess_type = w.SuggestedGuessType.RANDOM
    guess_type = w.SuggestedGuessType.HIGHEST_FREQUENCY
    wordle = w.Wordle(words, guess_type)

    # suggested_guess = 'trans'
    suggested_guess = wordle.get_suggested_guess() # 'trans'
    for i in range(6):
        next_guess, result = get_guess_and_result(suggested_guess)
        if result == [gr, gr, gr, gr, gr]:
            print(f'The word was {next_guess}, congratulations, you got it in {i+1} guesses!')
            break
        wordle.record_guess(next_guess, result)
        matching_words = wordle.get_matching_words()
        if len(matching_words) > 0:
            indices_to_show = min(10, len(matching_words))
            print(f'There were {len(matching_words)} matching values. Some examples: {",".join(matching_words[:indices_to_show])}')
        else:
            print(f'No words matched those filter criteria in our word list. Good luck!')
            break
        suggested_guess = wordle.get_suggested_guess()

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




import numpy as np

import read_data as rd
import wordle as w
import wordle_game as wg
import console_game as cg
import random

class GameMode:
    CONSOLE = 1
    SUGGESTED_GUESS_TESTING = 2

def main():
    #game_mode = GameMode.CONSOLE
    game_mode = GameMode.SUGGESTED_GUESS_TESTING

    word_length = 5
    words = rd.read_word_file('wlist_match10.txt', word_length)

    g = w.LetterResultCode.GRAY
    y = w.LetterResultCode.YELLOW
    gr = w.LetterResultCode.GREEN

    if game_mode == GameMode.CONSOLE:
        print(f'Starting game in console mode.')
        #guess_type = w.SuggestedGuessType.RANDOM
        guess_type = w.SuggestedGuessType.EXPECTED_VALUE_GREEN
        wordle = w.Wordle(words, guess_type)
        game = cg.ConsoleGame()
        game.play_game(wordle)
    elif game_mode == GameMode.SUGGESTED_GUESS_TESTING:
        NUM_REPETITIONS = 1000
        print(f'Starting suggested guess testing mode with {NUM_REPETITIONS} trials on each suggested guess type.')
        NUM_TURNS_ALLOWED = 6
        guess_types = [{"guess_type_name":"random", "guess_type":w.SuggestedGuessType.RANDOM},
                       {"guess_type_name":"EV green", "guess_type":w.SuggestedGuessType.EXPECTED_VALUE_GREEN},
                       #{"guess_type_name":"EV yellow", "guess_type":w.SuggestedGuessType.EXPECTED_VALUE_YELLOW},
                       {"guess_type_name":"EV green + yellow", "guess_type":w.SuggestedGuessType.EXPECTED_VALUE_GREEN_AND_YELLOW}]
        wordle = w.Wordle(words, guess_types[0])  # initialize
        num_guess_types = len(guess_types)
        num_turns_this_repetition = np.zeros((NUM_REPETITIONS, num_guess_types), np.int)
        for i in range(NUM_REPETITIONS):
            random_index = random.randint(0, len(words) - 1)
            random_word = words[random_index]
            game = wg.WordleGame(random_word)  # test each suggested guess method against the same words
            for j in range(num_guess_types):
                gt = guess_types[j]
                wordle.reset(gt["guess_type"])
                success = False
                while not success:
                    num_turns_this_repetition[i, j] += 1
                    suggested_guesses = wordle.get_suggested_guesses(1)
                    if len(suggested_guesses) == 0:
                        raise Exception(f'Error, there appear to be no words in the dictionary meeting these criteria.')
                    guess = suggested_guesses[0]
                    success, result = game.get_result(guess)
                    wordle.record_guess(guess, result)
        for j in range(num_guess_types):
            num_turns = num_turns_this_repetition[:,j]
            gt = guess_types[j]
            game_result = {}
            game_result["suggested guess type"] = gt["guess_type_name"]
            avg = np.mean(num_turns)
            std_error = np.std(num_turns, ddof=1) / np.sqrt(NUM_REPETITIONS)
            game_result["turns needed to guess word"] = f'{avg} +/- {std_error}'
            num_failures = len(num_turns[num_turns > NUM_TURNS_ALLOWED])
            game_result["num failures"] = f'{num_failures} / {NUM_REPETITIONS} ({100 * num_failures / NUM_REPETITIONS}%)'
            game_result["min turns needed"] = np.min(num_turns)
            game_result["max turns needed"] = np.max(num_turns)
            print(game_result)
            #print(f'debug: {num_turns_this_repetition}')
    else:
        raise Exception(f'game mode {game_mode} was not recognized.')




if __name__ == '__main__':
    main()




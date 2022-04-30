from tkinter import *
from tkinter import ttk
from tkinter import font
import wordle as w
import re

class WordleGUI:
    COLORS = ["Gray", "Yellow", "Green"]
    SUGGESTED_GUESSES_TO_SHOW = 5

    def __init__(self, wordle):
        self.wordle = wordle
        self.row = 0

    def get_guess_and_result(self):
        row = self.row
        guess = []
        result_array = self.results[row]
        for col in range(self.wordle.WORD_LENGTH):
            tb = self.text_boxes[row][col]
            color = tb.config('background')
            letter = self.text_box_values[row][col].get()
            guess.append(letter)
        guess_str = "".join(guess)
        return guess_str, result_array  # return as string

    def guess_and_result_valid(self, guess, result_array):
        guess_valid = bool(re.match('^[a-z]{5}', guess)) # 5 characters
        result_valid = (min(result_array) >= 0)  # result initialized
        return guess_valid and result_valid

    def ok_click(self, *args):
        gr = w.LetterResultCode.GREEN
        current_row = self.row
        guess, result_array = self.get_guess_and_result()
        if result_array == [gr, gr, gr, gr, gr]:
            self.set_instructions(f'Congratulations, you found the answer in {self.row + 1} guesses.', None, None, True)
            self.row = -1 # set to invalid row
            self.set_tb_enabled(current_row)  # disable the textboxes
            self.set_buttons_enabled(current_row) # disable the button
        elif self.row == w.Wordle.NUM_TURNS_ALLOWED-1:
            self.set_instructions(f'Unfortunately, you''re out of guesses.', None, None, True)
            self.row = -1  # set to invalid row
            self.set_tb_enabled(current_row)  # disable the textboxes
            self.set_buttons_enabled(current_row)  # disable the button
        else:
            self.wordle.record_guess(guess, result_array)
            suggested_guesses, scores = self.wordle.get_suggested_guesses(self.SUGGESTED_GUESSES_TO_SHOW)
            self.set_instructions("",suggested_guesses, scores, False)
            new_row = current_row + 1
            self.row = new_row
            self.set_tb_enabled(current_row)
            self.set_buttons_enabled(current_row)
            self.set_tb_enabled(new_row)
            self.set_buttons_enabled(new_row)
            self.set_focus(new_row,0)

    def set_buttons_enabled(self, row):
        print(f'setting buttons enabled for row {row}')
        guess, result_array = self.get_guess_and_result()
        print(f'guess = {guess}, result_array = {result_array}')
        is_valid = self.guess_and_result_valid(guess, result_array)
        print(f'is_valid = {is_valid}')
        if is_valid:
            self.buttons[row].grid()  # show
        else:
            self.buttons[row].grid_forget()  # hide

    def hide_buttons(self):
        for row in range(self.wordle.NUM_TURNS_ALLOWED):
            self.buttons[row].grid_forget()  # hide

    def set_tb_enabled(self, row):
        for col in range(self.wordle.WORD_LENGTH):
            tb = self.text_boxes[row][col]
            if row == self.row:
                tb.config(state='normal')
            else:
                tb.config(state='disabled')

    def set_focus(self, row, col):
        tb = self.text_boxes[row][col]
        tb.focus()

    def tb_click(self, row, col, tb):
        if row == self.row:
            x, result_code = divmod(self.results[row][col] + 1, len(self.COLORS))
            self.results[row][col] = result_code

            color = self.COLORS[result_code]
            tb.config(foreground=color) # set text color

            self.set_buttons_enabled(row)

    def handle_key_release(self, row, col):
        if row == self.row:
            tbv = self.text_box_values[row][col]
            text = tbv.get()
            if bool(re.match('^[a-z]', text)):
                if len(text) > 1:
                    tbv.set(text[-1:])  # just keep last character
                # this was a character from a to z
                if col < self.wordle.WORD_LENGTH - 1:
                    self.set_focus(row, col+1)
            else:
                # clear the text
                tbv.set('')
            self.set_buttons_enabled(row)

    def set_instructions(self, message, suggested_guesses=None, suggested_guess_scores=None, game_complete=False):
        str = ''
        if game_complete:
            str = f'{message} The game is complete.'
        elif not suggested_guesses is None:
            str += f'Suggested guesses: {suggested_guesses}\nSuggested guess scores: {suggested_guess_scores}'
        else:
            str = message
        self.instructions.set(str)

    def show_form(self):
        root = Tk()
        self.root = root
        root.title = "Wordle"

        mainframe = ttk.Frame(root, padding="3 3 12 12")
        mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)

        self.instructions = StringVar(name="instructions")
        ttk.Label(mainframe, textvariable=self.instructions).grid(column=1, columnspan=self.wordle.WORD_LENGTH, sticky=W)

        self.text_boxes = [[[] for col in range(self.wordle.WORD_LENGTH)] for row in range(self.wordle.NUM_TURNS_ALLOWED)]
        self.text_box_values = [[[] for col in range(self.wordle.WORD_LENGTH)] for row in range(self.wordle.NUM_TURNS_ALLOWED)]
        self.results = [[-1 for col in range(self.wordle.WORD_LENGTH)] for row in range(self.wordle.NUM_TURNS_ALLOWED)]
        self.buttons = [[] for row in range(self.wordle.NUM_TURNS_ALLOWED)]
        for row in range(self.wordle.NUM_TURNS_ALLOWED):
            for col in range(self.wordle.WORD_LENGTH):
                tb_text = StringVar()
                tb = ttk.Entry(mainframe, width=2, textvariable=tb_text, font='Georgia 30 bold')
                tb.grid(column=col+1, row=row+2, sticky=W)
                tb.config(state='disabled', justify='center')
                tb.bind("<1>", lambda event, row=row, col=col, tb=tb: self.tb_click(row, col, tb))
                tb.bind("<KeyRelease>", lambda event, row=row, col=col: self.handle_key_release(row, col))
                self.text_boxes[row][col] = tb
                self.text_box_values[row][col] = tb_text
            btn = ttk.Button(mainframe, text="OK", command=self.ok_click)
            self.buttons[row] = btn
            btn.grid(column=col+1, row=row+2, sticky=E)

        row = self.wordle.NUM_TURNS_ALLOWED + 2
        button_frame = Frame(mainframe)
        button_frame.grid(column=1, columnspan=self.wordle.WORD_LENGTH, row=row, sticky=E)
        #self.ok_button = ttk.Button(button_frame, text="OK", command=self.ok_click, default="active")
        #self.ok_button.grid(column=1, row=1, sticky=W)
        ttk.Button(button_frame, text="Exit", command=exit).grid(column=2, row=1, sticky=E)

        # add some padding around each element in mainframe
        for child in mainframe.winfo_children():
            child.grid_configure(padx=1, pady=1)

        root.bind("<Return>", self.ok_click)
        suggested_guesses, scores = self.wordle.get_suggested_guesses(5)
        self.row = 0
        self.set_instructions('Please enter your first guess.', suggested_guesses, scores)
        self.set_tb_enabled(0)  # enable the textboxes in the first row
        self.set_focus(0,0)  # set focus on first textbox
        self.hide_buttons()

        root.mainloop()
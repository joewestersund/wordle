from tkinter import *
from tkinter import ttk
from tkinter import font
from wordle import Wordle
import re

class WordleGUI:
    COLORS = ["White", "Yellow", "Green"]

    def __init__(self, wordle):
        self.wordle = wordle
        self.row = 0
        self.col = 0

    def ok_click(self, *args):
        print(f'ok_click was triggered.')

    def set_focus_on_row(self, row):
        self.text_boxes[row][0].focus()

    def set_enabled(self):
        for row in range(self.wordle.NUM_TURNS_ALLOWED):
            for col in range(self.wordle.WORD_LENGTH):
                tb = self.text_boxes[row][col]
                if row == self.row and col == self.col:
                    tb.config(state='normal')
                    tb.focus()
                else:
                    tb.config(state='disabled')

    def handle_click(self, row, col, tb):
        print(f'click handled. {row} {col}')
        entry_style = ttk.Style()
        entry_style.configure('style.TEntry',
                              fieldbackground="black",
                              foreground="white"
                              )
        #tb.config(style=entry_style)

    def handle_key_release(self, event):
        print(f'key release handled. {event}')
        if bool(re.match('^[a-z]', event.char)):
            # this was a character from a to z
            if self.col < self.wordle.WORD_LENGTH - 1:
                self.col += 1
                self.set_enabled()
        else:
            # clear the text
            self.text_box_values[self.row][self.col] = ''

    def set_instructions(self, message, suggested_guesses=None, suggested_guess_scores=None, game_complete=False):
        str = ''
        if game_complete:
            str = "The game is complete."
        elif not suggested_guesses is None:
            str += f'Suggested guesses: {suggested_guesses}\nSuggested guess scores: {suggested_guess_scores}'
        else:
            str += message
        self.instruction_text.set(str)

    def show_form(self):
        root = Tk()
        root.title = "Wordle"

        mainframe = ttk.Frame(root, padding="3 3 12 12")
        mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)

        self.instruction_text = StringVar()
        ttk.Label(mainframe, text=self.instruction_text).grid(column=1, columnspan=self.wordle.WORD_LENGTH, sticky=W)

        self.text_boxes = [[[] for col in range(self.wordle.WORD_LENGTH)] for row in range(self.wordle.NUM_TURNS_ALLOWED)]
        self.text_box_values = [[[] for col in range(self.wordle.WORD_LENGTH)] for row in range(self.wordle.NUM_TURNS_ALLOWED)]
        for row in range(self.wordle.NUM_TURNS_ALLOWED):
            for col in range(self.wordle.WORD_LENGTH):
                tb_text = StringVar()
                tb = ttk.Entry(mainframe, width=3, textvariable=tb_text, )
                tb.grid(column=col+1, row=row+2, sticky=W)
                tb.config(state='disabled')
                tb.bind("<1>", lambda event, row=row, col=col, tb=tb: self.handle_click(row, col, tb))
                tb.bind("<KeyRelease>", self.handle_key_release)
                self.text_boxes[row][col] = tb
                self.text_box_values[row][col] = tb_text

        row = self.wordle.NUM_TURNS_ALLOWED + 2
        button_frame = Frame(mainframe)
        button_frame.grid(column=1, columnspan=self.wordle.WORD_LENGTH, row=row, sticky=E)
        self.ok_button = ttk.Button(button_frame, text="OK", command=self.ok_click, default="active")
        self.ok_button.grid(column=1, row=1, sticky=W)
        ttk.Button(button_frame, text="Exit", command=exit).grid(column=2, row=1, sticky=E)

        # add some padding around each element in mainframe
        for child in mainframe.winfo_children():
            child.grid_configure(padx=1, pady=1)

        root.bind("<Return>", self.ok_click)
        suggested_guesses, scores = self.wordle.get_suggested_guesses(5)
        self.set_instructions('Please enter your first guess.', suggested_guesses, scores)
        self.set_enabled()  # enable the textbox in the first row & column

        root.mainloop()
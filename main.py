from tkinter import *
import pandas
import random

BACKGROUND_COLOR = "#B1DDC6"
to_learn = {}
current_card = {}
try:
    data = pandas.read_csv('words_to_learn.csv')
except FileNotFoundError:
    original_data = pandas.read_csv('data/ru_eng_words.csv')
    to_learn = original_data.to_dict(orient='records')
else:
    to_learn = data.to_dict(orient='records')


def new_word():
    global current_card, flip_timer
    window.after_cancel(flip_timer)
    current_card = random.choice(to_learn)
    flash_card.itemconfig(card_title, text='English', fill='black')
    flash_card.itemconfig(card_word, text=current_card['English'], fill='black')
    flash_card.itemconfig(card_background, image=CARD_IMAGE)
    flip_timer = window.after(3000, func=flip_card)


def flip_card():
    flash_card.itemconfig(card_title, text='Russian', fill='white')
    flash_card.itemconfig(card_word, text=current_card['Russian'], fill='white')
    flash_card.itemconfig(card_background, image=CARD_BACK_IMAGE)


def is_known():
    to_learn.remove(current_card)
    data = pandas.DataFrame(to_learn)
    data.to_csv('data/words_to_learn.csv', index=False)
    new_word()


# UI SETUP
window = Tk()
window.title('Flashy')
window.config(bg=BACKGROUND_COLOR, padx=50, pady=50)

flip_timer = window.after(3000, func=flip_card)

# FLASH CARD
flash_card = Canvas(highlightthickness=0, width=800, height=526)
CARD_IMAGE = PhotoImage(file='images/card_front.png')
card_background = flash_card.create_image(400, 263, image=CARD_IMAGE)
CARD_BACK_IMAGE = PhotoImage(file='images/card_back.png')
flash_card.config(bg=BACKGROUND_COLOR)
card_title = flash_card.create_text(400, 150, font=('Ariel', 40, 'italic'), text="")
card_word = flash_card.create_text(400, 263, font=('Ariel', 60, 'bold'), text="")
flash_card.grid(row=0, column=0, columnspan=2)

# BUTTONS
right_button = PhotoImage(file='./images/right.png')
agreed_button = Button(image=right_button, highlightthickness=0, relief=SUNKEN, command=is_known)
agreed_button.grid(row=1, column=1)

wrong_button_image = PhotoImage(file='./images/wrong.png')
wrong_button = Button(image=wrong_button_image, highlightthickness=0, relief=SUNKEN, command=new_word)
wrong_button.grid(row=1, column=0)

new_word()

window.mainloop()
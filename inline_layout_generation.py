import telebot

from meme_database import Memes


# Generate inline layout for meme confirmation
def generate_meme_inline_layout(meme_title):

    meme_markup = telebot.types.InlineKeyboardMarkup()
    nav_buttons = list()
    action_buttons = list()
    meme_index = list(Memes.keys()).index(meme_title)

    if meme_index > 0:
        prev_meme = list(Memes.keys())[meme_index-1]
        prev_button = telebot.types.InlineKeyboardButton(text="⬅ Prev",
                                                         callback_data="PR3V" + prev_meme)
        nav_buttons.append(prev_button)
    if meme_index < len(Memes) - 1:
        next_meme = list(Memes.keys())[meme_index+1]
        next_button = telebot.types.InlineKeyboardButton(text="Next ➡",
                                                         callback_data="N3XT" + next_meme)
        nav_buttons.append(next_button)

    back_button = telebot.types.InlineKeyboardButton(text="🔙 Back to all",
                                                     callback_data="BACK")
    select_button = telebot.types.InlineKeyboardButton(text="✅ Select this",
                                                       callback_data="S3L3CT" + meme_title)
    action_buttons.append(back_button)
    action_buttons.append(select_button)

    meme_markup.add(*[i for i in nav_buttons])
    meme_markup.add(*[i for i in action_buttons])

    return meme_markup


# Generation of the inline layout for the particular page for meme selection
def generate_page_inline_layout(page):

    memes_per_page = 12
    page_markup = telebot.types.InlineKeyboardMarkup(row_width=2)
    meme_buttons = list()
    nav_buttons = list()

    if page * memes_per_page + memes_per_page > len(Memes):
        end_index = len(Memes)
    else:
        end_index = page * memes_per_page + memes_per_page

    for i in range(page * memes_per_page, end_index):
        btn = telebot.types.InlineKeyboardButton(text=list(Memes)[i].upper(), callback_data=list(Memes)[i])
        meme_buttons.append(btn)
    page_markup.add(*[i for i in meme_buttons])

    if page > 0:
        button_left = telebot.types.InlineKeyboardButton(text="⬅ Page " + str(page),
                                                         callback_data='L3FT' + str(page))
        nav_buttons.append(button_left)

    if page < len(Memes) // memes_per_page:
        button_right = telebot.types.InlineKeyboardButton(text="Page " + str(page + 2) + ' ➡',
                                                          callback_data='R1GHT' + str(page))
        nav_buttons.append(button_right)

    page_markup.add(*[i for i in nav_buttons])
    return page_markup

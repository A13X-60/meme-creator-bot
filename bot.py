# -*- coding: utf-8 -*-
import os
import telebot
import time

from analytics import send_in_analytics, send_out_analytics
from image_editing import create_meme, create_pic_available_memes
from inline_layout_generation import generate_meme_inline_layout, generate_page_inline_layout
from meme_database import Memes

TOKEN = os.environ['TELEGRAM_TOKEN']

bot = telebot.TeleBot(TOKEN)
print('Starting bot:', bot.get_me())

# Menu reply markup
menu = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
btn1 = telebot.types.KeyboardButton('😂Create meme😂')
btn2 = telebot.types.KeyboardButton('😎List of available memes😎')
btn3 = telebot.types.KeyboardButton('☺Donations☺')
menu.add(btn1, btn2, btn3)

create_pic_available_memes()
available_memes_file_id = None


# Welcome message after user hits /start command
@bot.message_handler(commands=['start'])
def send_welcome(message):
    send_in_analytics({'text': message.text, 'userId': str(message.from_user.id)})
    send_out_analytics({'text': bot.send_message(message.chat.id, parse_mode='Markdown',
                                                 text='Hi there, *' + message.from_user.first_name +
                                                      '*! Go on and make some 😂😂👌👌😂_dank shit_💯💯 here!\n\n'
                                                      'Use /creatememe\n\n'
                                                      'Make yourself familiar with all available _memes_ with /available',
                                                 reply_markup=menu).text,
                        'userId': str(message.from_user.id)})


# /help command handler. Displays all available commands.
@bot.message_handler(commands=['help'])
def help_info(message):
    send_in_analytics({'text': message.text, 'userId': str(message.from_user.id)})
    send_out_analytics({'text': bot.send_message(message.chat.id, '/creatememe - Create a meme from template\n'
                                                                  '/available - List of the all available memes\n'
                                                                  '/cancel - Cancels current action').text,
                        'userId': str(message.from_user.id)})


# /cancel command handler. Cancels current action.
@bot.message_handler(commands=['cancel'])
def cancel(message):
    send_in_analytics({'text': message.text, 'userId': str(message.from_user.id)})
    send_out_analytics(
        {'text': bot.send_message(message.chat.id, 'No action to cancel.').text, 'userId': str(message.from_user.id)})


# /creatememe command handler. Sends user a keyboard to select desired meme.
@bot.message_handler(commands=['creatememe'])
@bot.message_handler(func=lambda m: m.text == '😂Create meme😂')
def choose_meme(message):
    send_in_analytics({'text': message.text, 'userId': str(message.from_user.id),
                       "intent": {"name": "MEME CREATION", "inputs": [{"name": "query", "value": message.text}]}})
    page = 0
    markup = generate_page_inline_layout(page)  # Setup inline keyboard markup
    msg = bot.send_message(message.chat.id, 'Select the meme from database', reply_markup=markup)
    send_out_analytics(
        {'text': msg.text,
         'userId': str(message.from_user.id),
         "intent": {"name": "MEME CREATION", "inputs": [{"name": "select meme menu", "value": msg.text}]}})


# /availablememe command handler. Displays all available memes on the generated picture
@bot.message_handler(func=lambda m: m.text == '😎List of available memes😎')
@bot.message_handler(commands=['available'])
def send_available_memes(message):
    send_in_analytics({'text': message.text, 'userId': str(message.from_user.id)})
    global available_memes_file_id
    if available_memes_file_id is None:
        available_memes_file_id = bot.send_photo(message.chat.id, open('Memes.png', 'rb')).photo[0].file_id
    else:
        bot.send_photo(message.chat.id, available_memes_file_id)
    send_out_analytics({'text': '', 'userId': str(message.from_user.id), 'images': [
        {'url': 'https://api.telegram.org/file/bot' + TOKEN + '/' + bot.get_file(available_memes_file_id).file_path}]})
    

# /donations command handler. Displays information about ways to donate author.
@bot.message_handler(func=lambda m: m.text == '☺Donations☺')
def donation_info(message):
    send_in_analytics({'text': message.text, 'userId': str(message.from_user.id)})
    send_out_analytics({'text': bot.send_message(message.chat.id,
                                                 parse_mode='Markdown',
                                                 text='If you want to thank me for the experience you had with this bot'
                                                      ' you can donate me via:\n\n'
                                                      'PrivatBank:\n*5168 7453 0322 6440*\n\n'
                                                      'Bitcoin:\n*1HvF4uSHNz9z1zafqSr2N8rxXyHcqAGrmY*\n\n'
                                                      'Ethereum:\n*0x5714Dde9B12Bf629F185CeE90f263C05816B1616*').text,
                        'userId': str(message.from_user.id)})


# Text input handler.
@bot.message_handler(func=lambda m: True, content_types=['text'])
def respond_to_message(message):
    send_in_analytics({'text': message.text, 'userId': str(message.from_user.id), 'intent': {'name': 'NotHandled'}})
    send_out_analytics({'text': bot.send_message(message.chat.id, 'I don\'t understand you...Is this loss??').text,
                        'userId': str(message.from_user.id), 'intent': {'name': 'NotHandled'}})


# Callback handler for pushing button on inline keyboard to switch to the previous page
@bot.callback_query_handler(func=lambda call: 'L3FT' in str(call.data))
def choose_page_left(call):
    markup = generate_page_inline_layout(int(str(call.data)[4]) - 1)
    bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=markup)


# Callback handler for pushing button on inline keyboard to switch to the next page
@bot.callback_query_handler(func=lambda call: 'R1GHT' in str(call.data))
def choose_page_right(call):
    markup = generate_page_inline_layout(int(str(call.data)[5]) + 1)
    bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=markup)


# Callback handler for pushing button on inline keyboard to switch to the previous meme
@bot.callback_query_handler(func=lambda call: 'PR3V' in str(call.data))
def choose_meme_prev(call):
    prev_meme = str(call.data)[4:]
    markup = generate_meme_inline_layout(prev_meme)
    if Memes[prev_meme].text_fields_file_id is None:
        photo = telebot.types.InputMediaPhoto(open('MemeTextFields/{}.png'.format(prev_meme), 'rb'),
                                              prev_meme[0].upper() + prev_meme[1:])
        photo_message = bot.edit_message_media(photo, call.message.chat.id,
                                               call.message.message_id, reply_markup=markup)
        Memes[prev_meme].text_fields_file_id = photo_message.photo[0].file_id
    else:
        photo = telebot.types.InputMediaPhoto(Memes[prev_meme].text_fields_file_id,
                                              prev_meme[0].upper() + prev_meme[1:])
        bot.edit_message_media(photo, call.message.chat.id,
                               call.message.message_id, reply_markup=markup)


# Callback handler for pushing button on inline keyboard to switch to the next meme
@bot.callback_query_handler(func=lambda call: 'N3XT' in str(call.data))
def choose_meme_next(call):
    next_meme = str(call.data)[4:]
    markup = generate_meme_inline_layout(next_meme)
    if Memes[next_meme].text_fields_file_id is None:
        photo = telebot.types.InputMediaPhoto(open('MemeTextFields/{}.png'.format(next_meme), 'rb'),
                                              next_meme[0].upper() + next_meme[1:])
        photo_message = bot.edit_message_media(photo, call.message.chat.id,
                                               call.message.message_id, reply_markup=markup)
        Memes[next_meme].text_fields_file_id = photo_message.photo[0].file_id
    else:
        photo = telebot.types.InputMediaPhoto(Memes[next_meme].text_fields_file_id,
                                              next_meme[0].upper() + next_meme[1:])
        bot.edit_message_media(photo, call.message.chat.id,
                               call.message.message_id, reply_markup=markup)


# Callback handler for pushing button on inline keyboard to return back to the meme selecting menu
@bot.callback_query_handler(func=lambda call: 'BACK' == str(call.data))
def back_to_menu(call):
    page = 0
    markup = generate_page_inline_layout(page)  # Setup inline keyboard markup
    bot.send_message(call.message.chat.id, 'Select the meme from database', reply_markup=markup)
    bot.delete_message(call.message.chat.id, call.message.message_id)


# Callback handler for pushing button on inline keyboard to cancel meme creating
@bot.callback_query_handler(func=lambda call: 'CANC3L' == str(call.data))
def cancel_selection(call):
    bot.delete_message(call.message.chat.id, call.message.message_id)
    bot.send_message(call.message.chat.id, 'Current action was cancelled.', reply_markup=menu)


# Callback handler for pushing button on inline keyboard to return back to the meme selecting menu
@bot.callback_query_handler(func=lambda call: 'S3L3CT' in str(call.data))
def select_meme(call):

    curr_meme = str(call.data)[6:]
    bot.answer_callback_query(call.id)
    msg = bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=None)

    sent_messages_id = list()  # Accumulating sent messages in case the user will send /cancel command
    sent_messages_id.append(msg.message_id)

    msg = bot.send_message(call.message.chat.id, parse_mode='Markdown',
                           text='Fill the following content areas. Send me a photo, a text or even a _STICKER_.\n\n'
                                '(type \"-\" to leave the area blank)')
    sent_messages_id.append(msg.message_id)
    send_out_analytics({
        'text': msg.text,
        'userId': str(call.from_user.id),
        "intent": {"name": "MEME CREATION", "inputs": [{"name": "creation info", "value": msg.text}]}})

    area = 1
    num_of_fields_to_read = len(Memes[curr_meme].areas.keys())
    markup = telebot.types.ForceReply()
    meme_content = list()

    msg = bot.send_message(call.message.chat.id, 'Enter the content for the area 1:', reply_markup=markup)
    sent_messages_id.append(msg.message_id)
    send_out_analytics({'text': msg.text, "intent": {"name": "MEME CREATION",
                                                     "inputs": [{"name": "area", "value": str(1)}]}})

    bot.register_next_step_handler(msg, content_injection, num_of_fields_to_read, area, curr_meme, meme_content,
                                   sent_messages_id)


# Callback handler for pushing button on inline keyboard to select meme.
@bot.callback_query_handler(func=lambda call: call.data in Memes.keys())
def menu_button_callback(call):

    meme_markup = generate_meme_inline_layout(call.data)
    curr_meme = call.data

    if Memes[curr_meme].text_fields_file_id is None:
        photo_message = bot.send_photo(call.message.chat.id,
                                       open('MemeTextFields/{}.png'.format(curr_meme), 'rb'),
                                       caption=call.data[0].upper() + call.data[1:],
                                       reply_markup=meme_markup)
        Memes[curr_meme].text_fields_file_id = photo_message.photo[0].file_id
    else:
        bot.send_photo(call.message.chat.id,
                       Memes[curr_meme].text_fields_file_id,
                       caption=call.data[0].upper() + call.data[1:],
                       reply_markup=meme_markup)

    bot.delete_message(call.message.chat.id, call.message.message_id)


# Collecting data for meme contents
def content_injection(message, num_of_fields_to_read, area, curr_meme, meme_content, sent_messages):

    num_of_fields_to_read -= 1
    area += 1
    markup = telebot.types.ForceReply()

    if message.text == '-':
        meme_content.append('')

    elif message.text == '/cancel':
        send_in_analytics({'text': message.text, 'userId': message.from_user.id})
        send_out_analytics(
            {'text': bot.send_message(message.chat.id, 'Current action was cancelled.', reply_markup=menu).text,
             'userId': message.from_user.id})
        num_of_fields_to_read = -1
        delete_messages(message.chat.id, sent_messages)
        del meme_content

    elif message.content_type == 'photo':
        file_id = message.photo[-1].file_id
        file = bot.get_file(file_id)
        meme_content.append(file.file_path)
        send_in_analytics({'text': '', 'userId': str(message.from_user.id),
                           'images': [{'url': 'https://api.telegram.org/file/bot' + TOKEN + '/' + file.file_path}]})

    elif message.content_type == 'sticker':
        sticker = message.sticker.file_id
        sticker_file = bot.get_file(sticker)
        meme_content.append(sticker_file.file_path)
        send_in_analytics({'text': '', 'userId': str(message.from_user.id),
                           'images': [{'url': 'https://api.telegram.org/file/bot' + TOKEN + '/' + sticker_file.file_path
                                       }]})

    elif message.content_type == 'text':
        meme_content.append(message.text)
        send_in_analytics({'text': message.text, 'userId': str(message.from_user.id)})

    else:
        err_msg = bot.send_message(message.chat.id, 'Please, try to send me some text, picture or a sticker')
        send_out_analytics({'text': err_msg.text, 'userId': message.from_user.id, 'intent': {'name': 'NotHandled'}})
        sent_messages.append(err_msg.message_id)
        num_of_fields_to_read += 1
        area -= 1

    if num_of_fields_to_read > 0:
        msg = bot.send_message(message.chat.id, 'Enter the content for the area ' + str(area) + ':',
                               reply_markup=markup)
        send_out_analytics({'text': msg.text, 'userId': str(message.from_user.id)})
        sent_messages.append(msg.message_id)
        bot.register_next_step_handler(msg, content_injection, num_of_fields_to_read, area,
                                       curr_meme, meme_content, sent_messages)

    elif num_of_fields_to_read == 0:
        send_out_analytics({'text': bot.send_message(message.chat.id, 'Your meme', reply_markup=menu).text,
                            'userId': str(message.from_user.id)})
        file_id = bot.send_photo(message.chat.id, create_meme(curr_meme, meme_content, TOKEN)).photo[-1].file_id
        file = bot.get_file(file_id)
        send_out_analytics({'text': '', 'userId': str(message.from_user.id),
                           'images': [{'url': 'https://api.telegram.org/file/bot' + TOKEN + '/' + file.file_path}]})
        del sent_messages

    else:
        pass


# Deleting sent messages from chat
def delete_messages(chat_id, sent_messages):
    for message in sent_messages:
        bot.delete_message(chat_id, message)
    del sent_messages


try:
    bot.polling(none_stop=True)
except Exception as err:
    time.sleep(5)
    if str(err) != "HTTPSConnectionPool(host='api.telegram.org', port=443): Read timed out. (read timeout=30)":
        bot.send_message(int(os.environ['CHAT_ID']), 'Error occurred: ' + str(err))
    print('Error occurred:', err)

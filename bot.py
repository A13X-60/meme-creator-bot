# -*- coding: utf-8 -*-
import os
import redis
import telebot
import time

from analytics import send_in_analytics, send_out_analytics
from image_editing import create_meme, create_pic_available_memes
from meme_database import Memes

token = os.environ['TELEGRAM_TOKEN']
r = redis.from_url(os.environ.get('REDIS_URL'))

bot = telebot.TeleBot(token)
print('Starting bot:', bot.get_me())

# Menu reply markup
menu = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
btn1 = telebot.types.KeyboardButton('😂Create meme😂')
btn2 = telebot.types.KeyboardButton('😎List of available memes😎')
btn3 = telebot.types.KeyboardButton('🤔Information🤔')
btn4 = telebot.types.KeyboardButton('☺Donations☺')
menu.add(btn1, btn2, btn3, btn4)

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
    markup = generate_inline_layout(page)  # Setup inline keyboard markup
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
        {'url': 'https://api.telegram.org/file/bot' + token + '/' + bot.get_file(available_memes_file_id).file_path}]})


# /information command handler. Displays some information about bot.
@bot.message_handler(func=lambda m: m.text == '🤔Information🤔')
def info(message):
    send_in_analytics({'text': message.text, 'userId': str(message.from_user.id)})
    send_out_analytics({'text': bot.send_message(message.chat.id,
                                                 'Bot made by @TheSubliminal\n'
                                                 'Feel free to send me any suggestions or bug reports.').text,
                        'userId': str(message.from_user.id)})


# /donations command handler. Displays information about ways to donate author.
@bot.message_handler(func=lambda m: m.text == '☺Donations☺')
def donation_info(message):
    send_in_analytics({'text': message.text, 'userId': str(message.from_user.id)})
    send_out_analytics({'text': bot.send_message(message.chat.id,
                                                 parse_mode='Markdown',
                                                 text='If you want to thank me for the experience you had with this bot'
                                                      ' you can donate me via:\n\n'
                                                      'PrivatBank:\n*4149 4978 5676 6680*\n\n'
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
def choose_meme_left(call):
    markup = generate_inline_layout(int(str(call.data)[4]) - 1)
    bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=markup)


# Callback handler for pushing button on inline keyboard to switch to the next page
@bot.callback_query_handler(func=lambda call: 'R1GHT' in str(call.data))
def choose_meme_right(call):
    markup = generate_inline_layout(int(str(call.data)[5]) + 1)
    bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=markup)


# Callback handler for pushing button on inline keyboard to select meme.
@bot.callback_query_handler(func=lambda call: call.data in Memes.keys())
def button_callback(call):
    sent_messages = list()
    bot.answer_callback_query(call.id)
    send_in_analytics({'text': call.data, 'userId': str(call.from_user.id),
                       "intent": {"name": "MEME CREATION", "inputs": [{"name": "meme", "value": call.data}]}})
    bot.delete_message(call.message.chat.id, call.message.message_id)
    curr_meme = call.data
    msg = bot.send_message(call.message.chat.id, parse_mode='Markdown',
                           text='Fill the following content areas. Send me a photo, a text or even a _STICKER_.\n\n'
                                '(type \"-\" to leave the area blank)')
    sent_messages.append(msg.message_id)
    send_out_analytics({
        'text': msg.text,
        'userId': str(call.from_user.id),
        "intent": {"name": "MEME CREATION", "inputs": [{"name": "creation info", "value": msg.text}]}})
    if Memes[curr_meme].text_fields_file_id is None:
        photo_message = bot.send_photo(call.message.chat.id, open('MemeTextFields/' + curr_meme + '.png', 'rb'))
        Memes[curr_meme].text_fields_file_id = photo_message.photo[0].file_id
        sent_messages.append(photo_message.message_id)
    else:
        sent_messages.append(bot.send_photo(call.message.chat.id, Memes[curr_meme].text_fields_file_id).message_id)
    area = 1
    num_of_fields_to_read = len(Memes[curr_meme].areas.keys())
    markup = telebot.types.ForceReply()
    meme_content = list()
    msg = bot.send_message(call.message.chat.id, 'Enter the content for the area 1:', reply_markup=markup)
    send_out_analytics({'text': msg.text, "intent": {"name": "MEME CREATION",
                                                     "inputs": [{"name": "area", "value": str(1)}]}})
    bot.register_next_step_handler(msg, content_injection, num_of_fields_to_read, area, curr_meme, meme_content,
                                   sent_messages)


# Generation of the inline layout for the particular page for meme selection
def generate_inline_layout(page):
    memes_per_page = 12
    page_markup = telebot.types.InlineKeyboardMarkup(row_width=2)
    button_list = list()
    nav_btns = list()
    if page * memes_per_page + memes_per_page > len(Memes):
        end_index = len(Memes)
    else:
        end_index = page * memes_per_page + memes_per_page
    for i in range(page * memes_per_page, end_index):
        btn = telebot.types.InlineKeyboardButton(text=list(Memes)[i].upper(), callback_data=list(Memes)[i])
        button_list.append(btn)
    page_markup.add(*[i for i in button_list])
    if page > 0:
        button_left = telebot.types.InlineKeyboardButton(text="⬅ Page " + str(page),
                                                         callback_data='L3FT' + str(page))
        nav_btns.append(button_left)
    if (page + 1) < len(Memes) // memes_per_page:
        button_right = telebot.types.InlineKeyboardButton(text="Page " + str(page + 2) + ' ➡',
                                                          callback_data='R1GHT' + str(page))
        nav_btns.append(button_right)
    page_markup.add(*[i for i in nav_btns])
    return page_markup


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
                           'images': [{'url': 'https://api.telegram.org/file/bot' + token + '/' + file.file_path}]})
    elif message.content_type == 'sticker':
        sticker = message.sticker.file_id
        sticker_file = bot.get_file(sticker)
        meme_content.append(sticker_file.file_path)
        send_in_analytics({'text': '', 'userId': str(message.from_user.id),
                           'images': [{'url': 'https://api.telegram.org/file/bot' + token + '/' + sticker_file.file_path
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
        bot.register_next_step_handler(msg, content_injection, num_of_fields_to_read, area, curr_meme, meme_content,
                                       sent_messages)
    elif num_of_fields_to_read == 0:
        send_out_analytics({'text': bot.send_message(message.chat.id, 'Your meme', reply_markup=menu).text,
                            'userId': str(message.from_user.id)})
        file_id = bot.send_photo(message.chat.id, create_meme(curr_meme, meme_content, token)).photo[-1].file_id
        file = bot.get_file(file_id)
        send_out_analytics({'text': '', 'userId': str(message.from_user.id),
                           'images': [{'url': 'https://api.telegram.org/file/bot' + token + '/' + file.file_path}]})
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

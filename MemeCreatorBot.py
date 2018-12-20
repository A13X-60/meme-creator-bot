# -*- coding: utf-8 -*-
import redis
import os
import telebot
import time
import math
import requests
from Memebase import Memes
from telebot import types
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont

token = os.environ['TELEGRAM_TOKEN']
r = redis.from_url(os.environ.get('REDIS_URL'))

bot = telebot.TeleBot(token)
print('Starting bot:', bot.get_me())

# Menu reply markup
menu = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
btn1 = types.KeyboardButton('😂Create meme😂')
btn2 = types.KeyboardButton('😎List of available memes😎')
btn3 = types.KeyboardButton('🤔Information🤔')
btn4 = types.KeyboardButton('☺Donations☺')
menu.add(btn1, btn2, btn3, btn4)


# A function which creates a list of the available memes on the bot's start up
def create_pic_available_memes():
    memes_per_row = 7
    font_size = 40
    txt = Image.new("RGBA", (281, 42), (255, 255, 255, 0))
    draw = ImageDraw.Draw(txt)
    font_head = ImageFont.truetype('impact.ttf', 40)
    font_title = ImageFont.truetype('impact.ttf', font_size)
    maxstr = max(list(Memes.keys()), key=len)
    while draw.textsize(maxstr, font_title)[0] > 256 or draw.textsize(maxstr, font_title)[1] > 30:
        font_size -= 1
        font_title = ImageFont.truetype('impact.ttf', font_size)
    head_w, head_h = draw.textsize('Available memes', font_head)
    background = Image.new('RGBA', (memes_per_row * 256 + 10 * (memes_per_row + 1),
                                    head_h + 20 + (math.ceil(len(list(Memes.keys())) / memes_per_row)) * (256 + 50)),
                           (255, 255, 255))
    img_draw = ImageDraw.Draw(background)
    img_draw.text(((background.size[0] - head_w) / 2, 10), 'Available memes', (0, 0, 0), font_head)
    header_bottom = 20 + head_h
    for i in range(math.ceil(len(list(Memes.keys())) / memes_per_row)):
        for j in range(memes_per_row):
            if i * memes_per_row + j > len(list(Memes.keys())) - 1:
                break
            meme = Image.open('MemeTemplates/' + list(Memes.keys())[i * memes_per_row + j] + '.png')
            meme.thumbnail((256, 256), Image.ANTIALIAS)
            background.paste(meme, (256 * j + 10 * (j + 1) + (256 - meme.size[0]) // 2,
                                    header_bottom + (256 + 50) * i + (256 - meme.size[1]) // 2))
            img_draw.text((256 * j + 10 * (j + 1) + (
                    256 - draw.textsize(list(Memes.keys())[i * memes_per_row + j], font_title)[0]) // 2,
                           (header_bottom + (256 + 5)) + i * (256 + 50)),
                          list(Memes.keys())[i * memes_per_row + j].upper(),
                          (0, 0, 0), font_title)
            del meme
    background.save('Memes.png')
    print('Memes.png was successfully saved.')
    del background
    del txt


create_pic_available_memes()
available_memes_file_id = None


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, parse_mode='Markdown',
                     text='Hi there, *' + message.from_user.first_name + '*! Go on and make some 😂😂👌👌😂_dank shit_💯💯 here!\n\nUse /creatememe\n\nMake yourself familiar with all available _memes_ with /available',
                     reply_markup=menu)


@bot.message_handler(commands=['help'])
def help_info(message):
    bot.send_message(message.chat.id,
                     '/creatememe - Create a meme from template\n/available - List of the all available memes\n/cancel - Cancels current action')


@bot.message_handler(commands=['cancel'])
def cancel(message):
    bot.send_message(message.chat.id, 'No action to cancel.')


@bot.message_handler(commands=['creatememe'])
@bot.message_handler(func=lambda m: m.text == '😂Create meme😂')
def choose_meme(message):
    page = 0
    markup = generate_inline_layout(page)
    bot.send_message(message.chat.id, 'Select the meme from database', reply_markup=markup)


@bot.message_handler(func=lambda m: m.text == '😎List of available memes😎')
@bot.message_handler(commands=['available'])
def send_available_memes(message):
    global available_memes_file_id
    if available_memes_file_id is None:
        available_memes_file_id = bot.send_photo(message.chat.id, open('Memes.png', 'rb')).photo[0].file_id
    else:
        bot.send_photo(message.chat.id, available_memes_file_id)


@bot.message_handler(func=lambda m: m.text == '🤔Information🤔')
def info(message):
    bot.send_message(message.chat.id,
                     'Bot made by @TheSubliminal\nFeel free to send me any suggestions or bug reports.\n\nRate this bot here: https://telegram.me/storebot?start=MemeCreate_bot')


@bot.message_handler(func=lambda m: m.text == '☺Donations☺')
def donation_info(message):
    bot.send_message(message.chat.id, parse_mode='Markdown',
                     text='If you want to thank me for the experience you had with this bot you can donate me via:\n\nBitcoin:\n*1HvF4uSHNz9z1zafqSr2N8rxXyHcqAGrmY*\n\nEthereum:\n*0x5714Dde9B12Bf629F185CeE90f263C05816B1616*')


@bot.message_handler(func=lambda m: True, content_types=['text'])
def respond_to_message(message):
    bot.send_message(message.chat.id, 'I don\'t understand you...Is this loss??')


@bot.callback_query_handler(func=lambda call: 'L3FT' in str(call.data))
def choose_meme_left(call):
    markup = generate_inline_layout(int(str(call.data)[4]) - 1)
    bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=markup)


@bot.callback_query_handler(func=lambda call: 'R1GHT' in str(call.data))
def choose_meme_right(call):
    markup = generate_inline_layout(int(str(call.data)[5]) + 1)
    bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data in Memes.keys())
def button_callback(call):
    sent_messages = list()
    bot.answer_callback_query(call.id)
    bot.delete_message(call.message.chat.id, call.message.message_id)
    curr_meme = call.data
    sent_messages.append(bot.send_message(call.message.chat.id, parse_mode='Markdown',
                     text='Fill the following content areas. Send me a photo, a text or even a _STICKER_.\n\n(type \"-\" to leave the area blank)').message_id)
    if Memes[curr_meme].text_fields_file_id is None:
        photo_message = bot.send_photo(call.message.chat.id, open('MemeTextFields/' + curr_meme + '.png', 'rb'))
        Memes[curr_meme].text_fields_file_id = photo_message.photo[0].file_id
        sent_messages.append(photo_message.message_id)
    else:
        sent_messages.append(bot.send_photo(call.message.chat.id, Memes[curr_meme].text_fields_file_id).message_id)
    area = 1
    num_of_fields_to_read = len(Memes[curr_meme].areas.keys())
    markup = types.ForceReply()
    meme_content = list()
    msg = bot.send_message(call.message.chat.id, 'Enter the content for the area 1:', reply_markup=markup)
    sent_messages.append(msg.message_id)
    bot.register_next_step_handler(msg, content_injection, num_of_fields_to_read, area, curr_meme, meme_content, sent_messages)


# Generation of the inline layout for the particular page for meme selection
def generate_inline_layout(page):
    memes_per_page = 8
    page_markup = types.InlineKeyboardMarkup(row_width=2)
    button_list = list()
    nav_btns = list()
    if page*memes_per_page + memes_per_page > len(Memes):
        end_index = len(Memes)
    else:
        end_index = page*memes_per_page + memes_per_page
    for i in range(page*memes_per_page, end_index):
        btn = types.InlineKeyboardButton(text=list(Memes)[i].upper(), callback_data=list(Memes)[i])
        button_list.append(btn)
    page_markup.add(*[i for i in button_list])
    if page > 0:
        button_left = types.InlineKeyboardButton(text="⬅ Page " + str(page), callback_data='L3FT' + str(page))
        nav_btns.append(button_left)
    if page < len(Memes) // memes_per_page:
        button_right = types.InlineKeyboardButton(text="Page " + str(page + 2) + ' ➡', callback_data='R1GHT' + str(page))
        nav_btns.append(button_right)
    page_markup.add(*[i for i in nav_btns])
    return page_markup


# Collecting data for meme contents
def content_injection(message, num_of_fields_to_read, area, curr_meme, meme_content, sent_messages):
    num_of_fields_to_read -= 1
    area += 1
    markup = types.ForceReply()
    if message.text == '-':
        meme_content.append('')
    elif message.text == '/cancel':
        bot.send_message(message.chat.id, 'Current action was cancelled.', reply_markup=menu)
        num_of_fields_to_read = -1
        delete_messages(message.chat.id, sent_messages)
        del meme_content
    elif message.content_type == 'photo':
        file_id = message.photo[-1].file_id
        file = bot.get_file(file_id)
        meme_content.append(file.file_path)
    elif message.content_type == 'sticker':
        sticker = message.sticker.file_id
        sticker_file = bot.get_file(sticker)
        meme_content.append(sticker_file.file_path)
    elif message.content_type == 'text':
        meme_content.append(message.text)
    else:
        sent_messages.append(bot.send_message(message.chat.id, 'Please, try to send me some text, picture or a sticker').message_id)
        num_of_fields_to_read += 1
        area -= 1
    if num_of_fields_to_read > 0:
        msg = bot.send_message(message.chat.id, 'Enter the content for the area ' + str(area) + ':',
                               reply_markup=markup)
        sent_messages.append(msg.message_id)
        bot.register_next_step_handler(msg, content_injection, num_of_fields_to_read, area, curr_meme, meme_content, sent_messages)
    elif num_of_fields_to_read == 0:
        bot.send_message(message.chat.id, 'Your meme', reply_markup=menu)
        create_meme(message, curr_meme, meme_content)
        del sent_messages
    else:
        pass


# Injecting collected data into the image, adjusting size of the text and pictures for the size of meme content fields
def create_meme(message, curr_meme, meme_content):
    j = 0
    meme = Image.open('MemeTemplates/' + curr_meme + '.png')
    for WH, position in Memes[curr_meme].areas.items():
        font_size = 40
        font_type = ImageFont.truetype(Memes[curr_meme].font_name, font_size)
        add_text = True
        width, height = WH[0], WH[1]
        im = Image.new("RGBA", (width, height), (255, 255, 255, 0))
        draw = ImageDraw.Draw(im)
        text = meme_content[j]
        if (('photos/' in text or 'stickers/' in text) and '.jpg' in text) or ('stickers/' in text and '.webp'):
            try:
                response = requests.get(
                    'https://api.telegram.org/file/bot' + token + '/' + text)
                user_img = Image.open(BytesIO(response.content))
                user_img.thumbnail((width, height), Image.ANTIALIAS)
                im.paste(user_img, ((im.size[0] - user_img.size[0]) // 2, (im.size[1] - user_img.size[1]) // 2))
                add_text = False
                del user_img
            except Exception as err:
                print(err)
                add_text = True
        elif add_text:
            modifiedtext = ''
            currstr = ''
            if draw.textsize(text, font=font_type)[0] < width:
                modifiedtext = text
            else:
                words = text.split()
                for i in range(len(words)):
                    if draw.textsize(currstr, font=font_type)[0] + draw.textsize(words[i], font=font_type)[0] < width:
                        currstr += words[i] + ' '
                    else:
                        modifiedtext += currstr + '\n'
                        currstr = words[i] + ' '
                    if i == len(words) - 1:
                        modifiedtext += currstr
                while draw.textsize(modifiedtext, font=font_type)[1] > height or \
                        draw.textsize(modifiedtext, font=font_type)[0] > width:
                    font_size -= 1
                    font_type = ImageFont.truetype(Memes[curr_meme].font_name, font_size)
            datas = im.getdata()
            new_data = []
            for item in datas:
                if item[0] == 255 and item[1] == 255 and item[2] == 255:
                    new_data.append((255, 255, 255, 0))
                else:
                    new_data.append(item)
            im.putdata(new_data)
            W, H = draw.textsize(modifiedtext, font=font_type)
            if Memes[curr_meme].font_colour == (255, 255, 255):
                draw.text(((width - W) / 2 - 1, (height - H) / 2 - 1), modifiedtext, font=font_type, fill=(0, 0, 0),
                          spacing=3, align='center')
                draw.text(((width - W) / 2 + 1, (height - H) / 2 - 1), modifiedtext, font=font_type, fill=(0, 0, 0),
                          spacing=3, align='center')
                draw.text(((width - W) / 2 - 1, (height - H) / 2 + 1), modifiedtext, font=font_type, fill=(0, 0, 0),
                          spacing=3, align='center')
                draw.text(((width - W) / 2 + 1, (height - H) / 2 + 1), modifiedtext, font=font_type, fill=(0, 0, 0),
                          spacing=3, align='center')
            draw.text(((width - W) / 2, (height - H) / 2), modifiedtext, fill=Memes[curr_meme].font_colour,
                      font=font_type, spacing=3, align='center')
        meme.paste(im, position, im)
        del im
        j += 1
    bio = BytesIO()
    bio.name = 'meme.png'
    meme.save(bio, 'PNG')
    bio.seek(0)
    bot.send_photo(message.chat.id, bio)
    del meme


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
        bot.send_message('CHAT_ID', 'Error occurred: ' + str(err))
    print('Error occurred:', err)

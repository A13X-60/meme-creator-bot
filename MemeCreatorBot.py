# -*- coding: utf-8 -*-
import redis
import os
import telebot
import time
import math
from telebot import types
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont

# import some_api_lib
# import ...

# Example of your code beginning
#           Config vars
token = os.environ['TELEGRAM_TOKEN']
#             ...

# If you use redis, install this add-on https://elements.heroku.com/addons/heroku-redis
r = redis.from_url(os.environ.get("REDIS_URL"))

#       Your bot code below
# bot = telebot.TeleBot(token)
# some_api = some_api_lib.connect(some_api_token)
#              ...

bot = telebot.TeleBot(token)
print('Starting bot:', bot.get_me())


class Meme:
    def __init__(self, areas, font_name, font_colour):
        self.areas = areas
        self.font_name = font_name
        self.font_colour = font_colour


drake = Meme({(319, 256): (322, 0), (319, 289): (322, 261)}, 'impact.ttf', (0, 0, 0))
scroll_of_truth = Meme({(96, 119): (95, 288)}, 'impact.ttf', (0, 0, 0))
expanding_brain = Meme({(422, 296): (0, 0), (420, 301): (2, 303), (417, 269): (2, 611), (419, 304): (2, 895)},
                       'impact.ttf', (0, 0, 0))
who_would_win = Meme({(404, 398): (5, 97), (371, 396): (424, 97)}, 'impact.ttf', (0, 0, 0))
the_rock_driving = Meme({(241, 116): (316, 31), (229, 106): (330, 263)}, 'impact.ttf', (0, 0, 0))
sleeping_shaq = Meme({(309, 335): (2, 2), (304, 285): (2, 342)}, 'impact.ttf', (0, 0, 0))
nut_button = Meme({(308, 222): (12, 179), (315, 318): (270, 41)}, 'impact.ttf', (255, 255, 255))
batman_slapping_robin = Meme({(167, 75): (21, 3), (169, 82): (223, 2)}, 'impact.ttf', (0, 0, 0))
is_this_a_pigeon = Meme({(326, 110): (28, 65), (217, 84): (416, 91), (568, 90): (33, 478)}, 'impact.ttf',
                        (255, 255, 255))
distracted_boyfriend = Meme({(161, 88): (97, 271), (150, 62): (309, 163), (151, 75): (449, 222)}, 'impact.ttf',
                            (0, 0, 0))
croatia_bosnia_border = Meme({(418, 157): (305, 128), (449, 137): (360, 370), (528, 130): (40, 623)}, 'impact.ttf',
                             (0, 0, 0))
left_exit_12_off_ramp = Meme({(262, 181): (101, 88), (276, 182): (369, 88), (427, 143): (195, 501)}, 'impact.ttf',
                             (255, 255, 255))
hard_to_swallow_pills = Meme({(278, 216): (135, 558)}, 'impact.ttf', (0, 0, 0))
trump_presenting = Meme({(289, 96): (2, 251), (308, 100): (133, 146), (409, 199): (383, 274)}, 'impact.ttf',
                        (255, 255, 255))
double_d_facts_book = Meme({(264, 130): (20, 494)}, 'impact.ttf', (0, 0, 0))
water_gun = Meme({(383, 112): (106, 343), (295, 214): (500, 369)}, 'impact.ttf', (255, 255, 255))
man_bear_fish = Meme({(561, 116): (103, 388), (333, 114): (219, 219), (232, 253): (560, 172)}, 'impact.ttf',
                     (255, 255, 255))
upvotes = Meme({(177, 45): (8, 392)}, 'impact.ttf', (0, 0, 0))
who_killed_hannibal = Meme({(319, 275): (513, 178), (307, 234): (83, 229), (930, 118): (15, 958)}, 'impact.ttf',
                           (255, 255, 255))
Memes = {'drake': drake, 'scroll of truth': scroll_of_truth, 'expanding brain': expanding_brain,
         'who would win': who_would_win, 'the rock driving': the_rock_driving, 'sleeping shaq': sleeping_shaq,
         'nut button': nut_button, 'batman slapping robin': batman_slapping_robin, 'is this a pigeon': is_this_a_pigeon,
         'distracted boyfriend': distracted_boyfriend, 'croatia bosnia border': croatia_bosnia_border,
         'left exit 12 off ramp': left_exit_12_off_ramp, 'hard to swallow pills': hard_to_swallow_pills,
         'trump presenting': trump_presenting, 'double d facts book': double_d_facts_book, 'water gun': water_gun,
         'man bear fish': man_bear_fish, 'upvotes': upvotes, 'who killed hannibal': who_killed_hannibal}


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, 'Hi there!')


@bot.message_handler(commands=['help'])
def help_info(message):
    bot.send_message(message.chat.id,
                     '/menu - All bot\'s options\n/creatememe - Create a meme from template\n/cancel - Cancels current action\n/available - List of the all available memes')


@bot.message_handler(commands=['menu'])
def open_buttons(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    btn1 = types.KeyboardButton('Create meme')
    markup.add(btn1)
    bot.send_message(message.chat.id, 'Select an option', reply_markup=markup)


@bot.message_handler(commands=['cancel'])
def cancel(message):
    markup = types.ReplyKeyboardRemove()
    bot.send_message(message.chat.id, 'Current action was cancelled.', reply_markup=markup)


@bot.message_handler(commands=['creatememe'])
@bot.message_handler(func=lambda m: m.text == 'Create meme')
def choose_meme(message):
    markup = types.InlineKeyboardMarkup()
    button_list = list()
    for i in Memes.keys():
        btn = types.InlineKeyboardButton(text=i[0].upper() + i[1:], callback_data=i)
        button_list.append(btn)
    markup.add(*[i for i in button_list])
    bot.send_message(message.chat.id, 'Select the meme from database', reply_markup=markup)


@bot.message_handler(commands=['available'])
def available_memes(message):
    memes_per_row = 3
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
    bio = BytesIO()
    bio.name = 'memes.png'
    background.save(bio, 'PNG')
    bio.seek(0)
    bot.send_photo(message.chat.id, bio)
    del background
    del txt


@bot.callback_query_handler(func=lambda call: True)
def button_callback(call):
    if call.data in Memes.keys():
        bot.answer_callback_query(call.id)
        bot.delete_message(call.message.chat.id, call.message.message_id)
        curr_meme = call.data
        bot.send_message(call.message.chat.id, 'Fill the following text areas(type \"-\" to leave the area blank):')
        bot.send_photo(call.message.chat.id, open('MemeTextFields/' + curr_meme + '.png', 'rb'))
        area = 1
        num_of_fields_to_read = len(Memes[curr_meme].areas.keys())
        markup = types.ForceReply()
        meme_texts = list()
        msg = bot.send_message(call.message.chat.id, 'Enter the text for the area 1:', reply_markup=markup)
        bot.register_next_step_handler(msg, read_text, num_of_fields_to_read, area, curr_meme, meme_texts)


def read_text(message, num_of_fields_to_read, area, curr_meme, meme_texts):
    num_of_fields_to_read -= 1
    area += 1
    markup = types.ForceReply()
    if message.text == '-':
        meme_texts.append('')
    elif message.text == '/cancel':
        bot.send_message(message.chat.id, 'Current action was cancelled.')
        num_of_fields_to_read = -1
    else:
        meme_texts.append(message.text)
    if num_of_fields_to_read > 0:
        msg = bot.send_message(message.chat.id, 'Enter the text for the area ' + str(area) + ':', reply_markup=markup)
        bot.register_next_step_handler(msg, read_text, num_of_fields_to_read, area, curr_meme, meme_texts)
    elif num_of_fields_to_read == 0:
        bot.send_message(message.chat.id, 'Your meme')
        create_meme(message, curr_meme, meme_texts)
    else:
        pass


def create_meme(message, curr_meme, meme_texts):
    j = 0
    font_size = 40
    meme = Image.open('MemeTemplates/' + curr_meme + '.png')
    font_type = ImageFont.truetype(Memes[curr_meme].font_name, font_size)
    for WH, position in Memes[curr_meme].areas.items():
        width, height = WH[0], WH[1]
        im = Image.new("RGBA", (width, height), (255, 255, 255, 0))
        draw = ImageDraw.Draw(im)
        text = meme_texts[j]
        modifiedtext = ''
        words = text.split()
        currstr = ''
        if draw.textsize(text, font=font_type)[0] < width:
            modifiedtext = text
        else:
            for i in words:
                if draw.textsize(currstr, font=font_type)[0] + draw.textsize(i, font=font_type)[0] < width:
                    currstr += i + ' '
                else:
                    modifiedtext += currstr + '\n'
                    currstr = i + ' '
                if words.index(i) == len(words) - 1:
                    modifiedtext += currstr
                while draw.textsize(modifiedtext, font=font_type)[1] > height or \
                        draw.textsize(modifiedtext, font=font_type)[0] > width:
                    font_size -= 1
                    font_type = ImageFont.truetype('impact.ttf', font_size)
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
        draw.text(((width - W) / 2, (height - H) / 2), modifiedtext, fill=Memes[curr_meme].font_colour, font=font_type,
                  spacing=3, align='center')
        meme.paste(im, position, im)
        del im
        j += 1
    bio = BytesIO()
    bio.name = 'meme.png'
    meme.save(bio, 'PNG')
    bio.seek(0)
    bot.send_photo(message.chat.id, bio)
    del meme


try:
    bot.polling(none_stop=True)
except Exception as err:
    time.sleep(5)
    bot.send_message(426440597, 'Error occurred: ' + str(err))
    print('Error occurred:', err)

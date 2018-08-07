# -*- coding: utf-8 -*-
import redis
import os
import telebot
import time
import math
import requests
from telebot import types
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont

token = os.environ['TELEGRAM_TOKEN']
r = redis.from_url(os.environ.get("REDIS_URL"))

#       Your bot code below
# bot = telebot.TeleBot(token)
# some_api = some_api_lib.connect(some_api_token)
#              ...

bot = telebot.TeleBot(token)
print('Starting bot:', bot.get_me())


# 'Areas' variable is a dict structured like this:
#                   {(width_of_the_area, height_of_the_area): (x_of_the_left_top_corner, y_of_the_left_top_corner), ...}
class Meme:
    def __init__(self, areas, font_name, font_colour):
        self.areas = areas
        self.font_name = font_name
        self.font_colour = font_colour
        self.text_fields_file_id = None


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
                            (255, 255, 255))
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
american_chopper_argument = Meme(
    {(232, 88): (12, 185), (311, 108): (185, 477), (282, 90): (1, 790), (228, 118): (1, 1066), (281, 98): (219, 1374)},
    'impact.ttf', (0, 0, 0))
battle_with_giant = Meme({(260, 224): (228, 96), (242, 153): (67, 506)}, 'impact.ttf', (255, 255, 255))
this_is_brilliant_but_i_like_this = Meme({(270, 166): (319, 127), (244, 172): (32, 460)}, 'impact.ttf', (255, 255, 255))
trojan_horse = Meme({(349, 131): (43, 207), (378, 147): (26, 346), (343, 135): (368, 41), (311, 155): (363, 527)},
                    'impact.ttf', (255, 255, 255))
homers_fat = Meme({(222, 99): (426, 157), (284, 199): (130, 128), (319, 236): (124, 594)}, 'impact.ttf',
                  (255, 255, 255))
you_cant_defeat_me = Meme({(262, 123): (221, 136), (243, 119): (431, 439), (357, 225): (195, 629)}, 'impact.ttf',
                          (255, 255, 255))
Memes = {'drake': drake, 'scroll of truth': scroll_of_truth, 'expanding brain': expanding_brain,
         'who would win': who_would_win, 'the rock driving': the_rock_driving, 'sleeping shaq': sleeping_shaq,
         'nut button': nut_button, 'batman slapping robin': batman_slapping_robin, 'is this a pigeon': is_this_a_pigeon,
         'distracted boyfriend': distracted_boyfriend, 'croatia bosnia border': croatia_bosnia_border,
         'left exit 12 off ramp': left_exit_12_off_ramp, 'hard to swallow pills': hard_to_swallow_pills,
         'trump presenting': trump_presenting, 'double d facts book': double_d_facts_book, 'water gun': water_gun,
         'man bear fish': man_bear_fish, 'upvotes': upvotes, 'who killed hannibal': who_killed_hannibal,
         'american chopper argument': american_chopper_argument,
         'battle with giant': battle_with_giant, 'this is brilliant but i like this': this_is_brilliant_but_i_like_this,
         'trojan horse': trojan_horse, 'homer\'s fat': homers_fat, 'you can\'t defeat me': you_cant_defeat_me}

# Menu reply markup
menu = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
btn1 = types.KeyboardButton('😂Create meme😂')
btn2 = types.KeyboardButton('😎List of available memes😎')
btn3 = types.KeyboardButton('🤔Information🤔')
btn4 = types.KeyboardButton('☺Donations☺')
menu.add(btn1, btn2, btn3, btn4)


# A function which creates a list of the available memes on the bot's start up
def create_pic_available_memes():
    memes_per_row = 5
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
                     text='Hi there, *' + message.from_user.first_name + '*! Go on and make some 😂😂👌👌😂_dank shit_💯💯 here!\n\nUse /creatememe\n\nMake yourself familiar with all available _memes_ with /available')


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
    markup = types.InlineKeyboardMarkup()
    button_list = list()
    for i in Memes.keys():
        btn = types.InlineKeyboardButton(text=i.upper(), callback_data=i)
        button_list.append(btn)
    markup.add(*[i for i in button_list])
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


@bot.callback_query_handler(func=lambda call: True)
def button_callback(call):
    if call.data in Memes.keys():
        bot.answer_callback_query(call.id)
        bot.delete_message(call.message.chat.id, call.message.message_id)
        curr_meme = call.data
        bot.send_message(call.message.chat.id,
                         'Fill the following content areas. Send me a photo or a text.\n\n(type \"-\" to leave the area blank)')
        if Memes[curr_meme].text_fields_file_id is None:
            Memes[curr_meme].text_fields_file_id = \
                bot.send_photo(call.message.chat.id, open('MemeTextFields/' + curr_meme + '.png', 'rb')).photo[
                    0].file_id
        else:
            bot.send_photo(call.message.chat.id, Memes[curr_meme].text_fields_file_id)
        area = 1
        num_of_fields_to_read = len(Memes[curr_meme].areas.keys())
        markup = types.ForceReply()
        meme_content = list()
        msg = bot.send_message(call.message.chat.id, 'Enter the content for the area 1:', reply_markup=markup)
        bot.register_next_step_handler(msg, content_injection, num_of_fields_to_read, area, curr_meme, meme_content)


@bot.message_handler(func=lambda m: True, content_types=['text'])
def respond_to_message(message):
    bot.send_message(message.chat.id, 'I don\'t understand you...Is this loss??')


def content_injection(message, num_of_fields_to_read, area, curr_meme, meme_content):
    num_of_fields_to_read -= 1
    area += 1
    markup = types.ForceReply()
    if message.text == '-':
        meme_content.append('')
    elif message.text == '/cancel':
        bot.send_message(message.chat.id, 'Current action was cancelled.', reply_markup=menu)
        num_of_fields_to_read = -1
    elif message.content_type == 'photo':
        file_id = message.photo[-1].file_id
        file = bot.get_file(file_id)
        meme_content.append(file.file_path)
    elif message.content_type == 'text':
        meme_content.append(message.text)
    else:
        bot.send_message(message.chat.id, 'Please, try to send me some text or a picture.')
        num_of_fields_to_read += 1
        area -= 1
    if num_of_fields_to_read > 0:
        msg = bot.send_message(message.chat.id, 'Enter the content for the area ' + str(area) + ':',
                               reply_markup=markup)
        bot.register_next_step_handler(msg, content_injection, num_of_fields_to_read, area, curr_meme, meme_content)
    elif num_of_fields_to_read == 0:
        bot.send_message(message.chat.id, 'Your meme', reply_markup=menu)
        create_meme(message, curr_meme, meme_content)
    else:
        pass


def create_meme(message, curr_meme, meme_content):
    j = 0
    font_size = 40
    meme = Image.open('MemeTemplates/' + curr_meme + '.png')
    font_type = ImageFont.truetype(Memes[curr_meme].font_name, font_size)
    for WH, position in Memes[curr_meme].areas.items():
        add_text = True
        width, height = WH[0], WH[1]
        im = Image.new("RGBA", (width, height), (255, 255, 255, 0))
        draw = ImageDraw.Draw(im)
        text = meme_content[j]
        if 'photos/' in text and '.jpg' in text:
            try:
                response = requests.get(
                    'https://api.telegram.org/file/bot' + token + '/' + text)
                user_img = Image.open(BytesIO(response.content))
                user_img.thumbnail((width, height), Image.ANTIALIAS)
                im.paste(user_img, ((im.size[0] - user_img.size[0]) // 2, (im.size[1] - user_img.size[1]) // 2))
                add_text = False
                del user_img
            except:
                add_text = True
        elif add_text:
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
            draw.text(((width - W) / 2, (height - H) / 2), modifiedtext, fill=Memes[curr_meme].font_colour,
                      font=font_type,
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

from io import BytesIO
import math
from PIL import Image, ImageFont, ImageDraw
import requests

from meme_database import Memes


# Injecting collected data into the image, adjusting size of the text and pictures for the size of meme content fields
def create_meme(curr_meme, meme_content, token):

    j = 0  # Content area index
    meme = Image.open('MemeTemplates/' + curr_meme + '.png')

    # For each content area of the current meme
    for WH, position in Memes[curr_meme].areas.items():

        width, height = WH[0], WH[1]  # Width and height of the current content area
        text = meme_content[j]  # Getting content for the current content area

        # Creating image with the following size as a "patch" which will be filled with text or image
        # and injected in the meme template
        im = Image.new("RGBA", (width, height), (255, 255, 255, 0))
        draw = ImageDraw.Draw(im)

        font_size = int(10*math.sqrt(width/len(text)))  # Calculating initial font size
        font_type = ImageFont.truetype('fonts/' + Memes[curr_meme].font_name, font_size)  # Getting meme's font
        add_text = True  # Add text information by default

        # If the sent content is a sticker or a photo, get the image from Telegram API
        if (('photos/' in text or 'stickers/' in text) and '.jpg' in text) or ('stickers/' in text and '.webp'):
            try:
                # Request the image
                response = requests.get('https://api.telegram.org/file/bot' + token + '/' + text)
                user_img = Image.open(BytesIO(response.content))
                # Resize it
                user_img.thumbnail((width, height), Image.ANTIALIAS)
                # Paste into the middle of the current content area
                im.paste(user_img, ((im.size[0] - user_img.size[0]) // 2, (im.size[1] - user_img.size[1]) // 2))
                add_text = False  # Mark that the content is a picture
                del user_img
            except Exception as err:
                print(err)
                add_text = True
        # If the content is a text
        elif add_text:
            modifiedtext = ''  # Variable for formatted string
            currstr = ''  # Variable for string for the current line of text in the content area

            if draw.textsize(text, font=font_type)[0] < width:  # If text fits in the current content area
                modifiedtext = text  # Leave everything unchanged
            else:
                words = list()  # List of words for the text area

                if '\n' not in text:  # If the text is not separated into multiple lines
                    words = text.split()  # Simply split by words
                else:
                    lines = text.splitlines(keepends=True)  # First, split by lines

                    for line in lines:  # For each line
                        line_words = line.split()  # Split by words
                        for i in range(len(line_words)):  # Add every word in list
                            if i == len(line_words) - 1:
                                words.append((str(line_words[i]) + '\n'))
                            else:
                                words.append((line_words[i]))

                for i in range(len(words)):

                    # If adding new word won't make the line wider than the width of the content area and there is
                    # no line breaks
                    if draw.textsize(currstr, font=font_type)[0] + draw.textsize(words[i], font=font_type)[0] < width \
                            and '\n' not in words[i]:
                        currstr += words[i] + ' '  # Add word for the current line
                    else:
                        modifiedtext += currstr + '\n'  # Add current line to the resulting text and break the lines
                        currstr = words[i] + ' '  # Add current word to the new line

                    if i == len(words) - 1:  # If last word
                        modifiedtext += currstr  # Simply add to the resulting string

                # Fit the text size for the content area
                while (draw.textsize(modifiedtext, font=font_type)[1] > height or
                        draw.textsize(modifiedtext, font=font_type)[0] > width):
                    font_size -= 1
                    font_type = ImageFont.truetype(Memes[curr_meme].font_name, font_size)

            datas = im.getdata()
            new_data = []

            # Provide transparent background of the content "patch"
            for item in datas:
                if item[0] == 255 and item[1] == 255 and item[2] == 255:
                    new_data.append((255, 255, 255, 0))
                else:
                    new_data.append(item)

            im.putdata(new_data)  # Update "patch"
            w, h = draw.textsize(modifiedtext, font=font_type)

            # If the font color is white, create black border around it
            if Memes[curr_meme].font_colour == (255, 255, 255):
                draw.text(((width - w) / 2 - 1, (height - h) / 2 - 1), modifiedtext, font=font_type, fill=(0, 0, 0),
                          spacing=3, align='center')
                draw.text(((width - w) / 2 + 1, (height - h) / 2 - 1), modifiedtext, font=font_type, fill=(0, 0, 0),
                          spacing=3, align='center')
                draw.text(((width - w) / 2 - 1, (height - h) / 2 + 1), modifiedtext, font=font_type, fill=(0, 0, 0),
                          spacing=3, align='center')
                draw.text(((width - w) / 2 + 1, (height - h) / 2 + 1), modifiedtext, font=font_type, fill=(0, 0, 0),
                          spacing=3, align='center')
            draw.text(((width - w) / 2, (height - h) / 2), modifiedtext, fill=Memes[curr_meme].font_colour,
                      font=font_type, spacing=3, align='center')

        meme.paste(im, position, im)  # Paste the "patch" in the stated position
        del im
        j += 1  # Switch to the next content area

    draw_wm = ImageDraw.Draw(meme)  # Watermark patch

    # Calculate the size of the watermark
    if meme.size[0] > meme.size[1]:
        watermark_font_size = int(math.sqrt(meme.size[0]/7))
    else:
        watermark_font_size = int(math.sqrt(meme.size[1]/7))

    watermark_font = ImageFont.truetype('fonts/impact.ttf', watermark_font_size)
    # Create black border around text of the watermark
    draw_wm.text((2, meme.size[1] - (draw_wm.textsize('@MemeCreate_bot', font=watermark_font)[1] + 4)),
                 '@MemeCreate_bot', font=watermark_font,
                 fill=(0, 0, 0), spacing=3, aling='left')
    draw_wm.text((4, meme.size[1] - (draw_wm.textsize('@MemeCreate_bot', font=watermark_font)[1] + 4)),
                 '@MemeCreate_bot', font=watermark_font,
                 fill=(0, 0, 0), spacing=3, aling='left')
    draw_wm.text((2, meme.size[1] - (draw_wm.textsize('@MemeCreate_bot', font=watermark_font)[1] + 2)),
                 '@MemeCreate_bot', font=watermark_font,
                 fill=(0, 0, 0), spacing=3, aling='left')
    draw_wm.text((4, meme.size[1] - (draw_wm.textsize('@MemeCreate_bot', font=watermark_font)[1] + 2)),
                 '@MemeCreate_bot', font=watermark_font,
                 fill=(0, 0, 0), spacing=3, aling='left')
    draw_wm.text((3, meme.size[1] - (draw_wm.textsize('@MemeCreate_bot', font=watermark_font)[1] + 3)),
                 '@MemeCreate_bot', font=watermark_font,
                 fill=(255, 255, 255), spacing=3, aling='left')

    bio = BytesIO()  # Convert the picture
    bio.name = 'meme.png'
    meme.save(bio, 'PNG')
    bio.seek(0)
    del meme
    return bio


# A function which creates a list of the available memes on the bot's start up
def create_pic_available_memes():

    memes_per_row = 7
    font_size = 40
    txt = Image.new("RGBA", (281, 42), (255, 255, 255, 0))
    draw = ImageDraw.Draw(txt)
    font_head = ImageFont.truetype('fonts/impact.ttf', 40)  # Header font
    font_title = ImageFont.truetype('fonts/impact.ttf', font_size)  # Meme titles' font
    maxstr = max(list(Memes.keys()), key=len)  # Maximum length of the meme title

    # Fit the font size for the titles
    while draw.textsize(maxstr, font_title)[0] > 256 or draw.textsize(maxstr, font_title)[1] > 30:
        font_size -= 1
        font_title = ImageFont.truetype('fonts/impact.ttf', font_size)

    head_w, head_h = draw.textsize('Available memes', font_head)  # Header size
    # Calculate the size of the picture
    background = Image.new('RGBA', (memes_per_row * 256 + 10 * (memes_per_row + 1),
                                    head_h + 20 + (math.ceil(len(list(Memes.keys())) / memes_per_row)) * (256 + 50)),
                           (255, 255, 255))
    img_draw = ImageDraw.Draw(background)
    img_draw.text(((background.size[0] - head_w) / 2, 10), 'Available memes', (0, 0, 0), font_head)
    header_bottom = 20 + head_h

    # Print the images and the titles on the background
    for i in range(math.ceil(len(list(Memes.keys())) / memes_per_row)):
        for j in range(memes_per_row):
            if i * memes_per_row + j > len(list(Memes.keys())) - 1:
                break
            meme = Image.open('MemeTemplates/' + list(Memes.keys())[i * memes_per_row + j] + '.png')
            meme.thumbnail((256, 256), Image.ANTIALIAS)  # Fit the picture in the area
            background.paste(meme, (256 * j + 10 * (j + 1) + (256 - meme.size[0]) // 2,
                                    header_bottom + (256 + 50) * i + (256 - meme.size[1]) // 2))
            img_draw.text((256 * j + 10 * (j + 1) +
                           (256 - draw.textsize(list(Memes.keys())[i * memes_per_row + j], font_title)[0]) // 2,
                           (header_bottom + (256 + 5)) + i * (256 + 50)),
                          list(Memes.keys())[i * memes_per_row + j].upper(), (0, 0, 0), font_title)
            del meme

    background.save('Memes.png')
    print('Memes.png was successfully saved.')
    del background
    del txt

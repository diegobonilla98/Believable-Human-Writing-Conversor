from PIL import Image, ImageFont, ImageDraw
import numpy as np
import matplotlib.pyplot as plt
from num2words import num2words
from fontTools.ttLib import TTFont
from fontTools.unicode import Unicode


def blank_page():
    file_name = "blank_pages\\blank_%i.jpeg" % np.random.randint(0, 5)
    image = Image.open(file_name)
    return image


def buff_command(text_batch, start_idx, max_batch):
    global special
    comm_buff = text_batch[start_idx + 1: start_idx + max_batch]
    end_idx = comm_buff.find(special)
    comm_buff = comm_buff[: end_idx]
    return comm_buff


def new_line():
    global font_size, y, x, paragraph_rand_spacing, initial_font_size, indent_rand
    paragraph_rand_spacing = (font_size - font_size // 2.5, font_size)
    y += np.random.randint(*paragraph_rand_spacing)
    font_size = initial_font_size
    x = np.random.randint(*indent_rand)


def new_page():
    global page, canvas, x, y, width, height, indent_rand, initial_y, images
    page += 1
    images.append(blank_page())
    canvas = ImageDraw.Draw(images[page])
    width, height = images[page].size
    x = np.random.randint(*indent_rand)
    y = initial_y


def has_glyph(glyph):
    global font_code
    for table in font_code['cmap'].tables:
        if ord(glyph) in table.cmap.keys():
            return True
    return False


initial_font_size = 100
lang = 'es'
font_name = "fonts\\Merche-Regular.ttf"
font_code = TTFont(font_name)
image_0 = blank_page()
width, height = image_0.size
images = [image_0]
canvas = ImageDraw.Draw(images[0])

page = 0
font_size = initial_font_size
paragraph_rand_spacing = (font_size - font_size // 2, font_size)
initial_y = 200
indent_rand = (120, 130)
new_line_indent = 1.3
word_rand_spacing_range = (font_size // 3.5, font_size // 3.5 + font_size // 10)
delta_y_rand_gaussian = (0, 0.8)
special = '~'
read_command = False
color = (0, 0, 0)


with open("texto.txt", encoding='utf-8') as file:
    text = file.read()
if text[0] == ':':
    end_format = text.find('\n')
    formats = text[1: end_format].split(', ')
    for argument in formats:
        exec(argument)
    text = text[end_format+1:]

font = ImageFont.truetype(font_name, initial_font_size)
x = np.random.randint(*indent_rand)
y = initial_y

idx = -1
while idx < len(text)-1:
    idx += 1
    char = text[idx]
    if char == special:
        read_command = not read_command
        continue

    if read_command:
        if char == 'C':
            command = buff_command(text, idx, 30)
            if command == 'red':
                color = (169, 9, 0)
            elif command == 'blue':
                color = (0, 38, 127)
            elif command == 'green':
                color = (32, 117, 75)
            else:
                color = exec(command)
            continue
        elif char == 'S':
            command = eval(buff_command(text, idx, 10))
            word_rand_spacing_range = (command // 4, command // 4 + command // 10)
            font_size = command if command > font_size else font_size
            font = ImageFont.truetype(font_name, command)
            continue
        elif char == 'T':
            command = eval(buff_command(text, idx, 10))
            x += command
            continue
        elif char == 'P':
            command = eval(buff_command(text, idx, 10))
            y += command
            continue
        elif char == 'R':
            word_rand_spacing_range = (initial_font_size // 4, initial_font_size // 4 + initial_font_size // 10)
            color = (0, 0, 0)
            font = ImageFont.truetype(font_name, initial_font_size)
            continue
        elif char == '#':
            command = eval(buff_command(text, idx, 30))
            x += np.random.randint(*word_rand_spacing_range)
            y += np.random.normal(*delta_y_rand_gaussian)
            number_str = num2words(command, lang=lang)
            canvas.text((x, y), number_str, color, font=font)
            x += np.random.randint(word_rand_spacing_range[0] * len(number_str),
                                   word_rand_spacing_range[1] * len(number_str))
            continue
        elif char == 'N':
            new_page()
            continue
        continue

    if char == '\n':
        new_line()
        if new_line_indent > 0:
            x += indent_rand[1] * np.random.normal(new_line_indent, 0.2)
        continue

    if not has_glyph(char):
        continue

    x += np.random.randint(*word_rand_spacing_range)
    y += np.random.normal(*delta_y_rand_gaussian)

    if y >= height - 2 * initial_y:
        new_page()
        continue

    if 123 > ord(char) > 40 and x >= width - 4 * np.random.randint(*indent_rand):
        if text[idx+1] not in [' ', '\n']:
            if not (33 <= ord(text[idx+1]) <= 47 and 33 <= ord(text[idx-1]) <= 47):
                end_word = text[idx: idx+20].find(' ')
                char = text[idx: idx+end_word]
                idx += end_word
            canvas.text((x, y), char, color, font=font)
            new_line()
            continue

    canvas.text((x, y), char, color, font=font)

for sheet in images:
    plt.imshow(sheet), plt.show()

if len(images) > 1:
    images[0].save("text.pdf", save_all=True, append_images=images[1:])
else:
    images[0].save("text.pdf")

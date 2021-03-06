import argparse
import configparser
import csv
import errno
import os
import requests
import sys
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from PIL import ImageChops
from datetime import date
from datetime import datetime
from fpdf import FPDF


def draw_page(draw_criteria, pages, current_dir, remainder, whole_pages):  # controls the creation of the body pages
    total_pages = pages  # necessary for the maths for the numbers being shown on each page
    page_counter = 1  # this counter allows the tally in the terminal to display correctly
    if args.log:
        log.write(f"Creating PNG pages:\n\n")
    if draw_criteria == 'test':  # test area (unused)
        icon = Image.open(f"{current_dir}/Assets/Icons/death_icon.png")
        page = Image.new('RGB', (1748, 2480), color=(255, 255, 255))
        page.paste(icon, box=(200, 200), mask=None)
        page.save('test.png')
        page.close()
    elif draw_criteria == 'main':  # main routine
        try:
            os.makedirs(f"{current_dir}/Output")
        except OSError as exc:  # handles the error if the directory already exists
            if exc.errno != errno.EEXIST:
                raise
            pass
        output_increment = 0
        while os.path.exists(f"{current_dir}/Output/Tally {output_increment}"):
            output_increment += 1
        try:
            os.makedirs(f"{current_dir}/Output/Tally {output_increment}")
        except OSError as exc:  # handles the error if the directory already exists
            if exc.errno != errno.EEXIST:
                raise
            pass
        os.chdir(f"{current_dir}/Output/Tally {output_increment}")
        if whole_pages is False:  # this special 'if' creates the last (not completely filled) page. Clean up?
            page_draw(remainder, pages, current_dir, total_pages)
            pages -= 1
            print('|', end='')
        else:
            pass
        while pages > 0:
            page_draw(500, pages, current_dir, total_pages)
            pages -= 1
            page_counter += 1
            print('|', end='')
            if page_counter % 20 == 0:  # keeps the tally neat
                print('')
        print(' 100%')
    else:
        pass


def page_draw(page_icon, pages, current_dir, total_pages):  # this routine creates individual pages
    icon = Image.open(f"{current_dir}/Assets/Icons/death_icon.png")  # imports the death icon
    page = Image.new('RGB', (1748, 2480), color=(255, 255, 255))  # makes the blank page
    if pages % 2 == 0:
        even_page = True
    else:
        even_page = False
    for x in range(page_icon):  # this draws the icons on a regular grid
        icon_number = x
        row = icon_number // 25
        column = icon_number % 25
        cursor_x = 65 + (65 * column)
        cursor_y = 148 + (108 * row)
        page.paste(icon, box=(cursor_x, cursor_y), mask=None)
    text_font = ImageFont.truetype(font=f"{current_dir}/Assets/Fonts/Crimson-Italic.ttf", size=40, index=0, encoding='',
                                   layout_engine=None)  # the font for the top and bottom matter
    page_text = ImageDraw.Draw(page)
    page_offset = page_text.textsize(f"Page {pages}", font=text_font)  # gets offset for right-aligned page numbers
    if even_page is True:
        cursor_x = 78
    elif even_page is False:
        cursor_x = 1670
        cursor_x -= page_offset[0]
    cursor_y = 2340
    page_text = ImageDraw.Draw(page)
    page_text.text((cursor_x, cursor_y), f"Page {pages}", font=text_font,
                   fill=(000, 000, 000))
    first_tally = ((pages - 1) * 500) + 1  # these two lines work out the numbers to be displayed for deaths per page
    second_tally = (first_tally + page_icon) - 1
    death_offset = page_text.textsize(f"Deaths {first_tally} - {second_tally}", font=text_font)
    if even_page is True:
        cursor_x = 78
    elif even_page is False:
        cursor_x = 1670
        cursor_x -= death_offset[0]
    cursor_y = 70
    page_text.text((cursor_x, cursor_y), f"Deaths {first_tally} - {second_tally}", font=text_font,
                   fill=(000, 000, 000))
    tally_offset = page_text.textsize(f"The Tally", font=text_font)
    if even_page is False:
        cursor_x = 78
    elif even_page is True:
        cursor_x = 1670
        cursor_x -= tally_offset[0]
    cursor_y = 70
    page_text.text((cursor_x, cursor_y), f"The Tally", font=text_font,
                   fill=(000, 000, 000))
    padding = len(str(total_pages)) - len(str(pages))
    page.save(f"main{padding * '0'}{pages}.png")  # saves a file with the appropriate number
    if args.log:
        small_time = now.strftime("%H:%M:%S")
        log.write(f"Page {padding * '0'}{pages} created successfully at {small_time}\n")
    page.close()


def book_stats(death_number):  # this function gets basic stats about the book from the number of total deaths
    page_value_1 = death_number // 500
    page_value_2 = death_number / 500
    page_value_3 = death_number % 500
    if page_value_2 > page_value_1:
        page_value_1 += 1
        whole_pages = False
        remainder = page_value_3
    else:
        remainder = 0
    return (page_value_1, whole_pages, remainder)


def path_pad(log_increment, log_length):  # pads out the increments on the log files to 3 digits
    path_pad_num = log_length - len(str(log_increment))
    path_pad_string = '0' * path_pad_num
    return path_pad_string


def read_csv(current_dir):  # reads the csv file
    os.chdir(current_dir)  # moves to the main directory
    table_data = []  # initialises the 'table_data' list
    csv.register_dialect('death', delimiter=",",  quoting=csv.QUOTE_NONE)  # creates a csv dialect that
    # seperates on commas
    try:
        with open('death_data.csv', newline='') as csv_file:
            csv_object = csv.reader(csv_file, dialect='death')   # creates a csv object
            for row in csv_object:
                table_data.append(row)
    except FileNotFoundError:
        table_data = None
    return table_data


def death_get(data_source):  # retrieves the dataset from coronavirus.gov.uk
    req = requests.get(data_source)
    death_data = req.content
    if args.log:
        log.write('New download request.\n\n')
        log.write('request status code:\n')
        log.write(f"{req.status_code}\n\n")
        log.write('request header:\n')
        log.write(f"{req.headers}\n\n")
    csv_file = open('death_data.csv', 'wb')
    csv_file.write(death_data)
    csv_file.close()


def front_matter(mode):  # creates the front matter of the book.
    blanks = 2
    for x in range (blanks):
        page = Image.new('RGB', (1748, 2480), color=(255, 255, 255))  # makes the blank page
        page.save(f"frnt00{x}.png")  # saves a file with the appropriate number
    page = Image.new('RGB', (1748, 2480), color=(255, 255, 255))  # makes the blank page
    isbn = Image.open(f"{current_dir}/Assets/Icons/ISBN.png")  # imports the isbn
    title_font = ImageFont.truetype(font=f"{current_dir}/Assets/Fonts/Crimson-Bold.ttf", size=260, index=0, encoding='',
                                    layout_engine=None)  # the font for the main title
    name_font = ImageFont.truetype(font=f"{current_dir}/Assets/Fonts/Crimson-Semibolditalic.ttf", size=70,
                                   index=0, encoding='', layout_engine=None)  # the font for the author's name
    intro_font = ImageFont.truetype(font=f"{current_dir}/Assets/Fonts/Crimson-Roman.ttf", size=60,
                                    index=0, encoding='', layout_engine=None)  # the font for the intro
    copy_font = ImageFont.truetype(font=f"{current_dir}/Assets/Fonts/Crimson-Semibold.ttf", size=50,
                                   index=0, encoding='', layout_engine=None)  # the font for the copyright notice
    page_text = ImageDraw.Draw(page)
    page_text.text((200, 620), f"THE TALLY", font=title_font, fill=(000, 000, 000))
    page_text.multiline_text((660, 1050), f"An Artist’s Book\nBy Sydney Cardew", font=name_font, align="center",
                             spacing=10, fill=(000, 000, 000))
    page.paste((190, 190, 190), box=(280, 1370, 1468, 1780))
    if mode == '1year':
        page_text.multiline_text((360, 1440), f"A record of the deaths during the 1st\n"
                                              f"year of the Coronavirus pandemic in the UK", font=intro_font,
                                 fill=(000, 000, 000), align="center", spacing=10)
    elif mode == 'total':
        page_text.multiline_text((360, 1440), f"A record of the deaths during the\n"
                                              f"time of the Coronavirus pandemic in the UK", font=intro_font,
                                 fill=(000, 000, 000), align="center", spacing=10)
    page_text.text((422, 1660), f"Our leaders have blood on their hands.", font=intro_font, fill=(000, 000, 000))
    if args.noisbn:
        pass
    else:
        page.paste(isbn, box=(588, 1920), mask=None)
    page_text.text((451, 2350), f"© Sydney Cardew for Idle Toil Press, 2021", font=copy_font, fill=(000, 000, 000))
    page.save(f"frnt003.png")
    if args.log:
        log.write('Front matter successfully created.\n\n')


def back_matter(pages):  # creates the back matter of the book.
    if pages % 2 == 0:
        blanks = 2
    else:
        blanks = 3
    for x in range (blanks):
        page = Image.new('RGB', (1748, 2480), color=(255, 255, 255))  # makes the blank page
        page.save(f"rear00{x}.png")  # saves a file with the appropriate number
    if args.log:
        log.write('Back matter successfully created.\n\n')


def cover_maker(current_dir, working_dir):  # makes the cover. Does not currently adjust for page count
    cover = Image.new('RGB', (3762, 2556), color=(255, 255, 255))  # makes the blank cover
    isbn = Image.open(f"{current_dir}/Assets/Icons/ISBN.png")  # imports the isbn
    title_font = ImageFont.truetype(font=f"{current_dir}/Assets/Fonts/Crimson-Bold.ttf", size=260, index=0, encoding='',
                                    layout_engine=None)  # the font for the main title
    name_font = ImageFont.truetype(font=f"{current_dir}/Assets/Fonts/Crimson-Semibold.ttf", size=100,
                                   index=0, encoding='', layout_engine=None)  # the font for the front name
    spine_title_font = ImageFont.truetype(font=f"{current_dir}/Assets/Fonts/Crimson-Semibold.ttf", size=90,
                                          index=0, encoding='', layout_engine=None)  # the font for the front name
    spine_name_font = ImageFont.truetype(font=f"{current_dir}/Assets/Fonts/Crimson-Italic.ttf", size=90,
                                         index=0, encoding='', layout_engine=None)  # the font for the front name
    opacity_table = [x for x in range(1, 6)]
    opacity_reverse = opacity_table[::-1]
    opacity_table.extend(opacity_reverse)
    pos_table_raw = [x for x in range (120, 601) if x % 120 == 0]
    pos_table = []
    for entry in pos_table_raw:
        pos_table.append(entry + 448)
    for entry in pos_table_raw:
        pos_table.append(entry + 1345)
    for value in range(len(opacity_table)):
        for repeat_icon in range(24):
            icon = Image.open(f"{current_dir}/Assets/Icons/cover_icon_{opacity_table[value]}.png")  # gets correct icon
            x_cursor = 2228 + (54 * repeat_icon)
            y_cursor = pos_table[value]
            cover.paste(icon, box=(x_cursor, y_cursor), mask=None)
    cover_text = ImageDraw.Draw(cover)
    cover_text.text((2206, 1216), f"THE TALLY", font=title_font, fill=(000, 000, 000))
    cover_text.text((2532, 2250), f"Sydney Cardew", font=name_font, fill=(000, 000, 000))
    spine = Image.new('RGB', (1142, 180), color=(255, 255, 255))  # makes the temporary image for the spine
    spine_text = ImageDraw.Draw(spine)
    spine_text.text((80, 45), f"Sydney Cardew", font=spine_name_font, fill=(000, 000, 000))
    spine_text.text((694, 45), f"The Tally", font=spine_title_font, fill=(000, 000, 000))
    spine_rotate = spine.rotate(270, expand=1)
    cover.paste(spine_rotate, (1780, 700))
    if args.noisbn:
        pass
    else:
        cover.paste(isbn, (872, 2106))
    cover.save(f"{working_dir}/cover_wrap.png")
    cover_pdf = FPDF('P', 'mm', (318.511, 216.408))
    cover_pdf.add_page()
    cover_pdf.image(f"{working_dir}/cover_wrap.png", 0, 0, 318.511)
    cover_pdf.output(f"{working_dir}/cover_pdf.pdf")
    if args.logs:
        log.write(f"Cover successfully generated.\n\n")


def pdf_maker(today):  # creates the print-ready PDF
    working_dir = os.getcwd()
    pdf = FPDF('P', 'mm', 'A5')
    for entry in os.scandir(f"{working_dir}"):
        filename = str(entry)[-13:-2]
        pdf.add_page()
        pdf.image(f"{working_dir}/{filename}", 0, 0, 148)
    pdf.output(f"{working_dir}/The_Tally-{today}.pdf")
    if args.log:
        log.write('PDF of \'The Tally\' successfully created.\n\n')
    return (working_dir)


parser = argparse.ArgumentParser(prog="CoronaBook")
parser.add_argument("-l", "--log", action='store_true', help="saves a log")
parser.add_argument("-u", "--user", action='store_true', help="uses user config settings")
parser.add_argument("-nd", "--nodownload", action='store_true', help="does not download a new csv file")
parser.add_argument("-nc", "--nocover", action='store_true', help="does not create a cover")
parser.add_argument("-ct", "--covertest", action='store_true', help="creates just a cover")
parser.add_argument("-ni", "--noisbn", action='store_true', help="creates a version without an ISBN")
parser.add_argument("-v", "--version", action='version', version='0.5.1')
args = parser.parse_args()
current_dir = os.getcwd()  # retrieves the current directory in which the script is running
today = str(date.today())  # gets today's date
config = configparser.ConfigParser()
if args.user:
    config_seg = 'CURRENT'
else:
    config_seg = 'DEFAULT'
config.read('Settings/config.ini')
data_source = config[(config_seg)]['data_source']  # gets the data url
log_length = int(config[(config_seg)]['log_length'])  # gets the log length
mode = config[(config_seg)]['mode']  # gets the mode
if args.log:
    now = datetime.now()
    small_time = now.strftime("%H:%M:%S")
    try:
        os.makedirs((current_dir) + '/Logs/')
    except OSError as exc:  # handles the error if the directory already exists
        if exc.errno != errno.EEXIST:
            raise
        pass
    log_increment = 0
    path_pad_string = path_pad(log_increment, log_length)
    while os.path.exists(f"{current_dir}/Logs/log {today} {path_pad_string}{str(log_increment)}.txt"):
        log_increment += 1
        path_pad_string = path_pad(log_increment, log_length)  # This increments the log filenames correctly
    log = open(f"{current_dir}/Logs/log {today} {path_pad_string}{str(log_increment)}.txt", "w")
    log_num = str(len([name for name in os.listdir(f"{current_dir}/Logs")
                      if os.path.isfile(os.path.join(f"{current_dir}/Logs", name))]))  # gets the total number of logs
    log.write(f"CoronaBook log number {log_num}. Date: {today}. Time: {small_time}\n")
    log.write(' ' + '\n')
    logging = True
if args.nodownload:
    if args.log:
        log.write('No new download request.\n\n')
else:
    death_get(data_source)
table_data = read_csv(current_dir)
if table_data is None:
    print('Error! No dataset available. Program will end.')
    if args.log:
        log.write('Error! No dataset available. Program will end.')
        log.close()
    sys.exit()
del table_data[0]
if mode == '1year':
    while (len(table_data)) > 365:
        del table_data[0]
if mode == '1year':
    if (len(table_data)) < 365:
        print('Error! Less than 1 years data exists. Proceeding with available dataset.')
        if args.log:
            log.write('Error! Less than 1 years data exists. Proceeding with available dataset.')
if mode == '1year':
    time_string = 'year'
elif mode == 'total':
    time_string = 'time'
latest_death_date = table_data[0][0][1:-1]
first_death_date = table_data[-1][0][1:-1]
death_number = int(table_data[0][4])
if args.covertest:
    working_dir_flag = False
else:
    print("""
    CoronaBook
    
    ---
    
    A program by Sydney Cardew
    
    ---
    
    """)
    print(f"The first person in the UK died of Coronavirus on {first_death_date}. In the {time_string} since,"
          f" {death_number} have died.\n")
    print(f"This program constructs a book called \'The Tally\' containing an icon for each individual death, in order")
    print(f"to convey the enormity of the tragedy by converting the data into a physical object.\n")
    print(f"It is intended as an explicit indictment of the British government's handling of this disaster.\n")
    input(f"Press enter to continue with memorial book generation.\n")
    pages, whole_pages, remainder = book_stats(death_number)
    print(f"500 deaths can be recorded on each page. The book will have {pages} pages of deaths.\n")
    draw_page('main', pages, current_dir, remainder, whole_pages)
    print('')
    print(f"Creating front matter.\n")
    front_matter(mode)
    print(f"Creating back matter.\n")
    back_matter(pages)
    print(f"PNG generation is complete.\n")
    print(f"Generating PDF.\n")
    working_dir = pdf_maker(today)
    working_dir_flag = True
    print(f"PDF generation is complete.\n")
    print(f"Book successfully generated in {working_dir}.\n")
if args.nocover:
    pass
else:
    if working_dir_flag is False:
        working_dir = current_dir
    print(f"Generating cover wrap.\n")
    cover_maker(current_dir, working_dir)
    print(f"Cover wrap generation complete.\n")
if args.log:
    log.write('CoronaBook has generated successfully.\n')
    log.close()

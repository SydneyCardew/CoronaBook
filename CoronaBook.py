import requests
import argparse
import os
import csv
import errno
import configparser
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from datetime import date
from datetime import datetime


def draw_page(draw_criteria, pages, current_dir, remainder, whole_pages):
    if draw_criteria == 'test':
        icon = Image.open(f"{current_dir}/Assets/Icons/Deathicon.png")
        page = Image.new('RGB', (1748, 2480), color=(255, 255, 255))
        page.paste(icon, box=(200, 200), mask=None)
        page.save('test.png')  # saves a file with the appropriate number
        page.close()
    elif draw_criteria == 'main':
        try:
            os.mkdir(f"{current_dir}/Test/")
        except FileExistsError:
            pass
        os.chdir(f"{current_dir}/Test/")
        if whole_pages is False:
            page_draw(remainder, pages, current_dir)
        else:
            pass
        while pages > 0:
            page_draw(500, pages, current_dir)
            pages -= 1
        print ('100%')
    else:
        pass


def page_draw(page_icon, pages, current_dir):
    cursor_x = 65
    cursor_y = 148
    icon = Image.open(f"{current_dir}/Assets/Icons/Deathicon.png")
    page = Image.new('RGB', (1748, 2480), color=(255, 255, 255))
    if page_icon == 500:
        full_rows = True
        rows = 20
    else:
        full_rows = False
        rows = page_icon//25
        last_row_num = page_icon % 25
        print(page_icon, full_rows, rows, last_row_num)
    while rows > 0:
        if full_rows is False:
            if rows == 1:
                row_fill = last_row_num
            else:
                row_fill = 25
        else:
            row_fill = 25
        while row_fill > 0:
            page.paste(icon, box=(cursor_x, cursor_y), mask=None)
            cursor_x += 65
            page_icon -= 1
            row_fill -= 1
        cursor_y += 108
        cursor_x = 65
        rows -= 1
    cursor_x = 1480
    cursor_y = 2400
    textfont = ImageFont.truetype(font=f"{current_dir}/Assets/Fonts/Crimson-Italic.ttf", size=10, index=0, encoding='',
                                  layout_engine=None)
    page_text = ImageDraw.Draw(page)
    page_text.text((cursor_x, cursor_y), f"{pages}", font=textfont,
              fill=(000, 000, 000))
    page.save(f"test{pages}.png")  # saves a file with the appropriate number
    page.close()
    print('|', end='')


def book_stats(death_number):
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


def path_pad(logincrement):  # pads out the increments on the log files to 3 digits
    path_pad_num = 3 - len(str(logincrement))
    path_pad_string = '0' * path_pad_num
    return path_pad_string


def readcsv(current_dir):  # reads the csv file
    os.chdir(current_dir)  # moves to the main directory
    tabledata = []  # initialises the 'tabledata' list
    csv.register_dialect('death', delimiter=",",  quoting=csv.QUOTE_NONE)  # creates a csv dialect that
    # seperates on commas
    with open('deathdata.csv', newline='') as csvfile:
        csvobject = csv.reader(csvfile, dialect='death')   # creates a csv object
        for row in csvobject:
            tabledata.append(row)
    return tabledata


def deathget(data_source):  # retrieves the dataset from coronavirus.gov.uk
    req = requests.get(data_source)
    death_data = req.content
    if args.log:
        log.write('New download request\n\n')
        log.write('request status code:\n')
        log.write(f"{req.status_code}\n\n")
        log.write('request header:\n')
        log.write(f"{req.headers}\n\n")
    csv_file = open('deathdata.csv', 'wb')
    csv_file.write(death_data)
    csv_file.close()


parser = argparse.ArgumentParser(prog="CoronaBook")
parser.add_argument("-d", "--debug", action='store_true', help="runs in debug mode.")
parser.add_argument("-l", "--log", action='store_true', help="saves a log")
parser.add_argument("-u", "--user", action='store_true', help="uses user config settings")
parser.add_argument("-nd", "--nodownload", action='store_true', help="does not download a new csv file")
args = parser.parse_args()
current_dir = os.getcwd()  # retrieves the current directory in which the script is running
today = str(date.today())  # gets today's date
config = configparser.ConfigParser()
if args.user:
    configseg = 'CURRENT'
else:
    configseg = 'DEFAULT'
config.read('Settings/config.ini')
data_source = config[(configseg)]['data_source']  # gets the data url
if args.log:
    now = datetime.now()
    smalltime = now.strftime("%H:%M:%S")
    try:
        os.makedirs((current_dir) + '/Logs/')
    except OSError as exc:  # handles the error if the directory already exists
        if exc.errno != errno.EEXIST:
            raise
        pass
    log_increment = 0
    path_pad_string = path_pad(log_increment)
    while os.path.exists(f"{current_dir}/Logs/log {today} {path_pad_string}{str(log_increment)}.txt"):
        log_increment += 1
        path_pad_string = path_pad(log_increment)
    log = open(f"{current_dir}/Logs/log {today} {path_pad_string}{str(log_increment)}.txt", "w")
    log_num = str(len([name for name in os.listdir(f"{current_dir}/Logs")
                      if os.path.isfile(os.path.join(f"{current_dir}/Logs", name))]))
    log.write(f"CoronaBook log number {log_num}. Date: {today}. Time: {smalltime}\n")
    log.write(' ' + '\n')
    logging = True
if args.nodownload:
    pass
else:
    deathget(data_source)
tabledata = readcsv(current_dir)
del tabledata[0]
while (len(tabledata)) > 365:
    del tabledata[0]
if (len(tabledata)) < 365:
    print('(Error: Less than 1 years data exists)')
latestdeathdate = tabledata[0][0][1:-1]
firstdeathdate = tabledata[-1][0][1:-1]
death_number = int(tabledata[0][4])
print(f"The first person in the UK died of Coronavirus on {firstdeathdate}. In the year since,"
      f"{death_number} have died.")
print(f"This program constructs a memorial book containing an icon for each individual death, in order to convey the "
      f"enormity of the tragedy.")
print(f"It is intended as an explicit indictment of the British government's handling of this disaster.")
input(f"Press enter to continue with memorial book generation.")
pages, whole_pages, remainder = book_stats(death_number)
print(f"The book will have {pages} pages.")
draw_page('main', pages, current_dir, remainder, whole_pages)

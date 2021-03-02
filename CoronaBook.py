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

def pathpad(logincrement): #pads out the increments on the log files to 3 digits
    if len(str(logincrement)) < 3:
        pathpadnum = 3 - len(str(logincrement))
        pathpadstring = '0' * pathpadnum
    return pathpadstring

def readcsv(currentdir): #reads the csv file
    os.chdir(currentdir) #moves to the main directory
    tabledata = [] #initialises the 'tabledata' list
    csv.register_dialect('death',delimiter=",",  quoting=csv.QUOTE_NONE) #creates a csv dialect that seperates on commas
    with open('deathdata.csv', newline='') as csvfile:
        csvobject = csv.reader(csvfile, dialect='death')  #creates a csv object
        for row in csvobject:
            tabledata.append(row)
    return tabledata

def deathget(datasource): # retrieves the dataset from coronavirus.gov.uk
    req = requests.get(datasource)
    deathdata = req.content
    if args.log:
        log.write('New download request\n\n')
        log.write('request status code:\n')
        log.write(f"{req.status_code}\n\n")
        log.write('request header:\n')
        log.write(f"{req.headers}\n\n")
    csv_file = open('deathdata.csv', 'wb')
    csv_file.write(deathdata)
    csv_file.close()

parser = argparse.ArgumentParser(prog="CoronaBook")
parser.add_argument("-d", "--debug", action='store_true', help = "runs in debug mode.")
parser.add_argument("-l", "--log", action='store_true', help = "saves a log")
parser.add_argument("-u", "--user", action='store_true', help = "uses user config settings")
parser.add_argument("-nd", "--nodownload", action = 'store_true', help = "does not download a new csv file")
args = parser.parse_args()
currentdir = os.getcwd() # retrieves the current directory in which the script is running
today = str(date.today()) # gets today's date
config = configparser.ConfigParser()
if args.user:
    configseg = 'CURRENT'
else:
    configseg = 'DEFAULT'
config.read('Settings/config.ini')
datasource = config[(configseg)]['datasource'] #gets the data url
if args.log:
    now = datetime.now()
    smalltime = now.strftime("%H:%M:%S")
    try:
        os.makedirs((currentdir) + '/Logs/')
    except OSError as exc:  # handles the error if the directory already exists
        if exc.errno != errno.EEXIST:
            raise
        pass
    logincrement = 0
    pathpadstring = pathpad(logincrement)
    while os.path.exists(f"{currentdir}/Logs/log {today} {pathpadstring}{str(logincrement)}.txt"):
        logincrement += 1
    pathpadstring = pathpad(logincrement)
    log = open(f"{currentdir}/Logs/log {today} {pathpadstring}{str(logincrement)}.txt", "w")
    lognum = str(len([name for name in os.listdir(f"{currentdir}/Logs") if os.path.isfile(os.path.join(f"{currentdir}/Logs", name))]))
    log.write (f"CoronaBook log number {lognum}. Date: {today}. Time: {smalltime}\n")
    log.write(' ' + '\n')
    logging = True
if args.nodownload:
    pass
else:
    deathget(datasource)
tabledata = readcsv(currentdir)
del tabledata[0]
while (len(tabledata)) > 365:
    del tabledata[0]
if (len(tabledata)) < 365:
    print ('(Error: Less than 1 years data exists)')
latestdeathdate = tabledata[0][0][1:-1]
firstdeathdate = tabledata[-1][0][1:-1]
deathnumber = int(tabledata[0][4])
print (f"The first person in the UK died of Coronavirus on {firstdeathdate}. In the year since, {deathnumber} have died.")
print (f"This program constructs a memorial book containing an icon for each individual death, in order to convey the enormity of the tragedy.")
print (f"It is intended as an explicit indictment of the British government's handling of this disaster.")
input (f"Press enter to continue with memorial book generation.")
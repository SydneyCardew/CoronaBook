import configparser
import errno
import os
import sys
from datetime import date
from datetime import datetime
import CoronaFunctions as f


def main():
    args = f.arguments()
    current_dir = os.getcwd()  # retrieves the current directory in which the script is running
    today = str(date.today())  # gets today's date
    config = configparser.ConfigParser()
    log = None
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
        path_pad_string = f.path_pad(log_increment, log_length)
        while os.path.exists(f"{current_dir}/Logs/log {today} {path_pad_string}{str(log_increment)}.txt"):
            log_increment += 1
            path_pad_string = f.path_pad(log_increment, log_length)  # This increments the log filenames correctly
        log = open(f"{current_dir}/Logs/log {today} {path_pad_string}{str(log_increment)}.txt", "w")
        log_num = str(len([name for name in os.listdir(f"{current_dir}/Logs")
                          if os.path.isfile(os.path.join(f"{current_dir}/Logs", name))]))  # gets number of logs
        log.write(f"CoronaBook log number {log_num}. Date: {today}. Time: {small_time}\n")
        log.write(' ' + '\n')
    if args.nodownload:
        if args.log:
            log.write('No new download request.\n\n')
    else:
        f.death_get(data_source, args, log)
    table_data = f.read_csv(current_dir)
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
    elif mode == '2year':
        while (len(table_data)) > 730:
            del table_data[0]
    if mode == '1year':
        if (len(table_data)) < 365:
            print('Error! Less than 1 years data exists. Proceeding with available dataset.')
            if args.log:
                log.write('Error! Less than 1 years data exists. Proceeding with available dataset.')
    if mode == '1year':
        time_string = 'year'
    elif mode == '2year':
        time_string = 'years'
    elif mode == 'total':
        time_string = 'time'
    latest_death_date = table_data[0][3]
    first_death_date = table_data[-1][3]
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
        print(f"This program constructs a book called \'The Tally\' "
              f"containing an icon for each individual death, in order")
        print(f"to convey the enormity of the tragedy by converting the data into a physical object.\n")
        print(f"It is intended as an explicit indictment of the British government's handling of this disaster.\n")
        input(f"Press enter to continue with memorial book generation.\n")
        pages, whole_pages, remainder = f.book_stats(death_number)
        print(f"500 deaths can be recorded on each page. The book will have {pages} pages of deaths.\n")
        f.draw_pages('main', pages, current_dir, remainder, whole_pages, args, log)
        print('')
        print(f"Creating front matter.\n")
        f.front_matter(mode, current_dir, args, log)
        print(f"Creating back matter.\n")
        f.back_matter(pages, args, log)
        print(f"PNG generation is complete.\n")
        print(f"Generating PDF.\n")
        working_dir = f.pdf_maker(today, args, log)
        working_dir_flag = True
        print(f"PDF generation is complete.\n")
        print(f"Book successfully generated in {working_dir}.\n")
    if args.nocover:
        pass
    else:
        if working_dir_flag is False:
            working_dir = current_dir
        print(f"Generating cover wrap.\n")
        f.cover_maker(current_dir, working_dir, args, log)
        print(f"Cover wrap generation complete.\n")
    if args.log:
        log.write('CoronaBook has generated successfully.\n')
        log.close()


if __name__ == "__main__":
    main()
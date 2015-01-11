import sys
import string
import re
import requests
import subprocess
import logging
import json


def get_metro_html():
    """
    :return: (string) HTML from metro_arrests_url
    """
    metro_arrests_url = "http://www.nashville.gov/Police-Department/News-and-Reports/Daily-Booking-List.aspx"
    return requests.get(metro_arrests_url).text


def get_first_pdf_link(html_text):
    """
    :param html_text: (string) - html expected from get_metro_html()
    :return: Text - the url of the most recent embedded pdf
    """
    lines = html_text.split("\n")
    target = re.compile(r'^\s+<li><a href="/Portals/0/SiteContent/Police/docs/Media/Daily')
    most_recent_arrests = [line.strip()  for line in lines if re.match(target, line)][0]
    end_of_link = string.find(most_recent_arrests, '">')

    return "http://www.nashville.gov{}".format(most_recent_arrests[13: end_of_link])


def pull_report(url):
    """
    :param url: (string) - the url of the target pdf
    :return: Saves the pdf file to the current dir and returns its filename (a string)
    """
    #TODO read output to memory instead of save file
    filename_pos = string.rfind(url, '/') + 1
    filename = url[filename_pos:].replace('%20', ' ')
    subprocess.check_output(['wget', url])
    return filename


def pdf_to_text(pdf):
    """
    :param pdf: (string) A filename
    :return: If a pdf filename matches the input, a .txt file is derived/saved. Pdf is deleted.
    Return value is a string (filename.txt).
    """
    # TODO try pdftotext writing to stdout instead of writing file: http://linux.die.net/man/1/pdftotext
    subprocess.check_output(['pdftotext', '-table', '-nopgbrk', pdf])
    
    subprocess.call(['rm', pdf])
    return pdf[:-3] + 'txt'


def read_text_file(text_file):
    """
    :param text_file: (file) .txt
    :return: (list) lines of the text file
    """
    with open(text_file) as f:
        return [line for line in f.readlines()]


def parse_text_file(lines_from_text_file):
    """
    :param lines_from_text_file: (list) the lines from a text file
    :return: A list of lists (of arrests): [['date', 'time', 'offense', 'last name', 'first name', 'location'],...]
    :comment: Each page of .txt file starts with 'Arrests'.  This header determines the position of the fields.
    """
    result = []

    for item in lines_from_text_file:
            
        if item[0] == 'A':
            date_pos = item.find('Arrest')
            offense_pos = item.find('Charge')
            name_pos = item.find('Last')
            location_pos = item.find('Street')

        if item[0].isdigit():
            datetime = item[date_pos: offense_pos-1].rstrip().split()
            offense = ' '.join(item[offense_pos: name_pos-1].lower().split())
            name = ' '.join(item[name_pos: location_pos-1].split()).lower().split()  # split/join to extra spaces, then split again
            location = ' '.join(item[location_pos:].lower().replace('\n', '').split())
            while len(name) < 2: # Is either name field empty?
                name.append('')

            arrest = [convert_date(datetime[0]), convert_time(datetime[-1]), offense, name[0], name[1], location]
            if len(arrest) != 6:
                arrest.append(None)
            if len(arrest) == 6:
                result.append(arrest)
            else:
                print("there was a problem with {}".format(arrest)) #if not the right length, print/log error & do not append
    return result
                

def convert_date(date_str):
    """
    :param date_str:(string) Date in the format 'M/D/YYYY'
    :return: (string) 'YYYY-MM-DD'
    """
    date_str = date_str.replace(' ', '').replace('-', '/')

    # Convert to 'MM/DD/YYYY'
    if date_str[1] == '/':
        date_str = '0' + date_str
        if date_str[4] == '/':
            date_str = date_str[:3] + '0' + date_str[3:]

    date_list = date_str.split('/')

    return '{}-{}-{}'.format(date_list[2], date_list[0], date_list[1])


def convert_time(time_str):
    """
    :param time_str: (string) 'H:MM' or 'HH:MM' or ''
    :return: (string) 'HH:MM' or ''
    """
    if time_str == '' or '/' in time_str:
        return '00:00'
    else:
        assert((3 < len(time_str) < 6) and (':' in time_str) and (int(time_str[-2:]) <= 59)) # rough check for validity
        if time_str[1] == ':':
            time_str = '0' + time_str

    assert(int(time_str[:2]) <= 23)

    return time_str


def fix_raw_datetime(bookings_list):
        """
        :param bookings_list: (list) A list of lists of arrest records.[['datetime', 'offense', 'last_name', 'first_name', 'location']] 
        :return:(list) [['YYYY-MM-DD', 'HH:MM', 'offense', 'last_name', 'first_name', 'location'], ['etc',]]
        """
        result = []
        for record in bookings_list:
            if len(record) < 5:
                record.append('')
            date_time = record[0].split(' ')
            date = date_time[0]

            if len(date_time) != 2:
                time = ''
            else:
                time = date_time[1]
            result.append([convert_date(date), convert_time(time)]) #fix the date/time
            for item in record[1:]:
                result[-1].append(item) #append the rest of the record to the list recently appended

        return result


def remove_duplicates(iterable):
    """
    :param iterable: (list)
    :return: (list) duplicates removed, original order preserved
    """
    unique = []
    for item in iterable:
        if item not in unique:
            unique.append(item)


def create_daily_booking_list():
    """
    :details: Get the link, download pdf, convert to .txt, parse it, fix the date/time item
    :return: a list of lists of the most recent arrests listed on nashville.gov
    :notes: multiple counts will appear as duplicates
    """
    return parse_text_file(read_text_file(pdf_to_text(pull_report(get_first_pdf_link(get_metro_html())))))


def booking_list_from_text_file(text_file):
    """
    :param text_file: an existing text file
    :return: a list of lists
    """
    return fix_raw_datetime(parse_text_file((read_text_file(text_file))))    


def json_from_daily_booking(booking_list):
    """
    :param booking_list: A list of lists from create_daily_booking_list() or booking_list_from_text_file()
    :return: (json) [{"model": crimeapp.crimes,
                      "pk": pk_number,
                      "fields": {
                                  "date": date,
                                  "time": time,
                                  "offense": offense,
                                  "surname": surname,
                                  "first_name": first_name,
                                  "location": location
                                }
                    }]
    """
    result = []
    for crime in booking_list:
        if crime[-1] == 'None':
            print("error detected in \n{}\n".format(crime))
        result.append(dict([
            ("model", "crimeapp.crimes"),
            ("fields", dict([
                ("date", crime[0]),
                ("time", crime[1]),
                ("offense", crime[2]),
                ("surname", crime[3]),
                ("first_name", crime[4]),
                ("location", crime[5])
            ]))

        ]))

    with open('recent_arrests.json', 'w') as outfile:
        json.dump(result, outfile, indent=4)



def main():
    json_from_daily_booking(create_daily_booking_list())


if __name__ == '__main__':
    sys.exit(main())





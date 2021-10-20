from requests_html import HTMLSession
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import time
import math
import re
import sys
import os.path

USAGE_URL = "https://www.purdue.edu/recwell/facility-usage/"
TEST_STR = "Colby Fitness"
headers = {"Accept" : "application/json, text/plain, */*",
"Accept-Encoding" : "gzip, deflate, br",
"Accept-Language" : "en-US,en;q=0.5",
"Cache-Control" : "max-age=0",
"Connection": "keep-alive",
"DNT" : "1",
"Host": "www.purdue.edu",
"Referer" : "https://www.purdue.edu/recwell/facility-usage/index.php",
"User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:85.0) Gecko/20100101 Firefox/85.0"}

def main():
    if len(sys.argv) != 2:
        print('Enter a file name to record to as an argument.')
        quit()
        # quit()
    # fix Encoding issues with replacement
    # sys.stdout.errors = 'replace'
    # sys.stdout.reconfigure(encoding='utf-8')
    # data python is behind, so reconfigure doesn't work

    url_html = get_url()
    # print('got url')
    rooms = process_for_rooms(url_html)
    # print('got rooms len:', len(rooms))
    rooms_data = []
    for room in rooms:
        # trying to show columns as I make them to avoid mixing them up
        name, current_capacity, total_capacity, percent_capacity = process_room(room)
        rooms_data.append([name, current_capacity, total_capacity, percent_capacity])
    df = pd.DataFrame(rooms_data, columns = ['name',
                                            'current_capacity',
                                            'total_capacity',
                                            'percent_capacity'])
    df['date_time'] = time.time()
    # print(df.head().to_string())
    record_df(df)

def get_url():
    with HTMLSession() as session:
        r = session.get(USAGE_URL, headers=headers)
        # print(r.text)
        render_success = False
        for i in range(3):
            # sometimes doesn't render right, try again if
            # it doesn't have the string we want, or it has run 3 times
            r.html.render(timeout = 4, sleep = 3)
            str_html = str(r.html.html) # this is getting the raw text
            if TEST_STR in str_html:
                print(f'Found {TEST_STR}!')
                render_success = True
                # this is an irritating hack but since requests_html is
                # inconsistent it's as good as i can do now.
                break
        if not render_success:
            print('Render failed. Aborting.')
            quit()
    return str_html

def process_for_rooms(str_html):
    soup = BeautifulSoup(str_html,features="lxml")
    div_containing = soup.find(name="div", attrs={"data-recwell-widget":"connect-feed","data-recwell-widget-json":"facility-usage-json"}).text
    locations = soup.find_all(name="div", attrs={"class":"rw-c2c-feed__location"})
    return locations

def process_room(soup_div):
    try:
        name = soup_div.find(name="h5", attrs={"class":"rw-c2c-feed__location--name"}).text
    except AttributeError:
        # print('No name on a location', soup_div)
        name = ""
    try:
        capacity_string = soup_div.find(name="span", attrs={"class":"rw-c2c-feed__about--capacity"}).text
    except AttributeError:
        # print('No capacity on a location', soup_div)
        total_capacity = np.nan
        current_capacity = np.nan
        percent_capacity = np.nan
        return name, current_capacity, total_capacity, percent_capacity
    # match the capacity
    # re_capacity = re.compile(r'\d\\\d')
    # print('capstr', capacity_string)
    number_strs = re.findall(r'\d+', capacity_string)
    numbers = []
    for number_str in number_strs:
        numbers.append(int(number_str))
    total_capacity = numbers[1]
    current_capacity = numbers[0]
    percent_capacity = numbers[2]
    return name, current_capacity, total_capacity, percent_capacity
# record the df to a csv
def record_df(df):
    # check if file exists
    filename = sys.argv[1]
    print('Printing to file:', filename)
    if os.path.isfile(filename):
        print(filename, 'already exists, appending to it.')
        df.to_csv(filename, header = False, mode = 'a')
    else:
        df.to_csv(filename)
    print('Finished.')



if __name__ == '__main__':
    main()

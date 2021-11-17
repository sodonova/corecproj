import requests
import pandas as pd
import time
import sys
import os.path

# Write or append the results of the corec api call onto the specified file.
# I'm considering melting it into a nicer format, but think preserving
# the api response as it's returned might be helpful in the future?
# This way I don't have to worry if the api returns something helpful that I wanted,
# but formatted out.
# It is pretty vulnerable to api changes though. A new entry in the JSON might screw up the csv.


url = r'https://www.purdue.edu/recwell/data/c2c-api.php'
headers = {"Accept" : "application/json, text/plain, */*",
"Accept-Encoding" : "gzip, deflate, br",
"Accept-Language" : "en-US,en;q=0.5",
"Cache-Control" : "max-age=0",
"Connection": "keep-alive",
"Cookie" : r'_gcl_au=1.1.75364913.1606677592; oribi_user_guid=f6a1c777-30ee-7a48-20bd-a93b4d03742e; nmstat=b0525745-b331-ba29-9f37-a9a77752294f; BIGipServer~WEB~pool_www.purdue.edu_ITSP_4443=!0iY/13+oxoCZC3AIlvTeHWdva3WNpis9/tWAJxNjKzj1ESPBuz/EHSL+7SveVr7z8yChUX/4nFZV4co=; BIGipServer~WEB~pool_www.purdue.edu_ITSP_web=!nhCVd87SIgjZKIcIlvTeHWdva3WNpkaElxhQvOP0ckGvo0HHv9Knp6wh8AjD0luWEN+k0wBoXA==; BIGipServer~WEB~pool_lpXwebapa02.itap.purdue.edu_web=!EUQv27TscMu7wHgIlvTeHWdva3WNpq+DGxBIQKmTLKUrsC+G0EbPTZkwXnX6jVnU/OlgJtdOvw==; BIGipServer~WEB~pool_wpvwebasp03-01-04_www.purdue.edu_web=!+5dMojiQ9q/QG/gIlvTeHWdva3WNpgPfkH1KjExc/UBNiyZiLdYRU+zq8DXw56Zw3rGeC67Ezg==',
"DNT" : "1",
"Host": "www.purdue.edu",
"Referer" : "https://www.purdue.edu/recwell/facility-usage/index.php",
"User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:85.0) Gecko/20100101 Firefox/85.0"}

def main():
    # make a dict of the corec usage data, store in dataframe.
    # Most recent occupancy data is in LastCount, not CountOfParticipants.  
    response = requests.get(url) # , headers = headers) used before 11/16 for headers, don't think they helped
    dict_of_json = response.json()
    df = pd.DataFrame.from_dict(dict_of_json)
    # store epoch time of when recording was made
    df['TimeRetrived'] = time.time()
    record_df(df)

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
    if len(sys.argv) != 2:
        print('Enter a file name to record to as an argument.')
        quit()
    main()

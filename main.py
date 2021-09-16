import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import urllib.parse
import re
import json
import csv
import datetime


def get_search_value(ptn, str0):
    result = re.search(ptn, str0)

    if result:
        return result.group(1)
    else:
        return None


def make_csv(tit, head, dat):
    with open(tit, 'w') as f:
        writer = csv.writer(f)
        writer.writerow(head)
        writer.writerow(dat)
    f.close()


if __name__ == '__main__':
    # Receive Instagram id from CUI (for now)
    instaID = input('Please input Instagram ID: ')
    print('Processing...')
    url = "https://www.instagram.com/" + urllib.parse.quote(instaID) + "/"

    options = Options()
    options.add_argument('--headless')
    options.add_argument('--user-agent=anonymous')
    driver = webdriver.Chrome(options=options)
    driver.get(url)

    driver.implicitly_wait(10)  # 10s

    html = driver.page_source

    # The following code is dependent on the form of Instagram
    json_str = get_search_value("window._sharedData = (.*);</script>", html)

    json_dict = json.loads(json_str)

    # Start the process for making csv data
    time_now = datetime.datetime.now()
    title = 'data' + time_now.strftime('%m%d%H%M%S') + '.csv'
    header = ['ID', 'Private', 'Follow', 'Follower', 'Media_count', 'Profile']
    data = [instaID,
            (json_dict['entry_data']['ProfilePage'][0]['graphql']['user']['is_private']),
            json_dict['entry_data']['ProfilePage'][0]['graphql']['user']['edge_follow']['count'],
            json_dict['entry_data']['ProfilePage'][0]['graphql']['user']['edge_followed_by']['count'],
            json_dict['entry_data']['ProfilePage'][0]['graphql']['user']['edge_owner_to_timeline_media']['count'],
            json_dict['entry_data']['ProfilePage'][0]['graphql']['user']['full_name']
            ]

    try:
        make_csv(title, header, data)
    except IOError as e:
        print(e)
    else:
        print('Successfully making csv data: ', os.getcwd() + '/' + title)
    finally:
        print('End')

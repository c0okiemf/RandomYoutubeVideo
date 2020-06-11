import random
import urllib.request
import webbrowser
import time
import json


def fetch_links(channel_id, key):
    base_video_url = 'https://www.youtube.com/watch?v='
    base_search_url = 'https://www.googleapis.com/youtube/v3/search?'

    first_url = \
        base_search_url + 'key={}&channelId={}&part=snippet,id&order=date&maxResults=50'.format(key, channel_id)

    video_links = []
    url = first_url
    ctr = 0
    try:
        while True:
            inp = urllib.request.urlopen(url)
            resp = json.load(inp)
            for i in resp['items']:
                if i['id']['kind'] == "youtube#video":
                    video_links.append(base_video_url + i['id']['videoId'])
            next_page_token = resp['nextPageToken']
            if next_page_token == '' or ctr > 10:
                break
            url = first_url + '&pageToken={}'.format(next_page_token)
            ctr += 1
        return video_links
    except Exception as e:
        print(str(e))
        return [1, 1]


try:
    file = open("links", "r")
    links = file.readlines()
    file.close()
except IOError:
    print("File not accessible, fetching new links...")
    links = []

if not links:
    try:
        key_file = open("key", "r")
        api_key = key_file.readline()
        links = fetch_links('UCdbcyBj6OO8lGMDQul1ansQ', api_key)
        file = open("links", "w")
        for link in links:
            file.write('%s\n' % link)
        file.close()
    except IOError:
        print("File \"key\" not found or corrupted, aborting...")
        time.sleep(3)

webbrowser.open(random.choice(links), new=2)

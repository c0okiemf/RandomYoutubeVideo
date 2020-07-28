import random
import urllib.request
import webbrowser
import time
import json
from pprint import pprint
from venv import logger


def fetch_links(playlist_id, key):
    base_video_url = 'https://www.youtube.com/watch?v='
    base_search_url = 'https://www.googleapis.com/youtube/v3/playlistItems?'

    first_url = \
        base_search_url + 'key={}&playlistId={}&part=snippet&maxResults=50'.format(key, playlist_id)

    video_links = []
    url = first_url
    try:
        for x in range(0, 30):
            inp = urllib.request.urlopen(url)
            resp = json.load(inp)
            for i in resp['items']:
                if i['snippet']['resourceId']['kind'] == "youtube#video":
                    video_links.append(base_video_url + i['snippet']['resourceId']['videoId'])
            if 'nextPageToken' not in resp or resp['nextPageToken'] == '':
                break
            url = first_url + '&pageToken={}'.format(resp['nextPageToken'])
        return video_links
    except Exception as e:
        logger.exception("Response is wrong...")
        return []


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
        links = fetch_links('UUdbcyBj6OO8lGMDQul1ansQ', api_key)
        file = open("links", "w")
        for link in links:
            file.write('%s\n' % link)
        file.close()
    except IOError:
        print("File \"key\" not found or corrupted, aborting...")
        time.sleep(3)

if len(links) > 0:
    webbrowser.open(random.choice(links), new=2)
else:
    print("No links available")
    time.sleep(3)

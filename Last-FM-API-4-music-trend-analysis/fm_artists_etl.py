import requests 
import json 
import requests_cache
import time
import pandas as pd 
from IPython.core.display import clear_output

def lastfm_get(playload):
    headers = {'user-agent': 'leolikedata'}
    url = 'https://ws.audioscrobbler.com/2.0/'

    playload['api_key'] = '01c65ba6504623c5e48586febced5463'
    playload['format'] = 'json'

    response = requests.get(url, headers= headers, params= playload)
    return response 

def run_fm_etl():
    responses = []

    page = 1
    total_pages = 999 # this is just a dummy number so the loop starts

    while page <= total_pages:
        payload = {
            'method': 'chart.gettopartists',
            'limit': 500,
            'page': page
        }


        print("Requesting page {}/{}".format(page, total_pages))
        # clear the output to make things neater
        clear_output(wait = True)

        # make the API call
        response = lastfm_get(payload)

        # if we get an error, print the response and halt the loop
        if response.status_code != 200:
            print(response.text)
            break

        # extract pagination info
        page = int(response.json()['artists']['@attr']['page'])

        total_pages = int(response.json()['artists']['@attr']['totalPages'])


        # append response
        responses.append(response)

        # if it's not a cached result, sleep
        if not getattr(response, 'from_cache', False):
            time.sleep(0.25)

        # increment the page number
        page += 1

        frames = [pd.DataFrame(r.json()["artists"]['artist']) for r in responses ]
        artists = pd.concat(frames)
        artists = artists.drop(['url', 'mbid', 'streamable', 'image'], axis = 1)
        artists.to_csv('s3://8893-artists-20211101/artists.csv', index= False)

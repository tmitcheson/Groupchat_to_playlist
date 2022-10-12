import json
import requests
from requests.structures import CaseInsensitiveDict
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
import csv
import os
load_dotenv()

# set up .env file with PLAYLIST_ID constant and link
PLAYLIST_ID = os.environ.get("PLAYLIST_ID")

# also put:
# SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET, and SPOTIPY_REDIRECT_URI in .env
# as per the Spotipy documenation

def get_list_of_tunes_from_file(conversation):

    ''' given a Messenger downloaded chat history in json format, this function
        will return a list of all the spotify tracks shared in it in list form
        '''

    f = open(conversation)
    data = json.load(f)
    messages = data["messages"]

    list_of_tunes = []

    for message in messages:
        try:
            if "https://open.spotify.com/track/" in message["content"]:

                message_content = message["content"]

                start = message_content.find("https://open.spotify.com/track/")

                # magic numbers used for isolating just trackID code
                track_code = message_content[start + 31: start + 53]

                parameter_tune_link = "spotify:track:" + track_code

                list_of_tunes.append(parameter_tune_link)

        except KeyError:
            continue

    list_of_tunes = list(dict.fromkeys(list_of_tunes))
    list_of_tunes.reverse()
    return list_of_tunes

def save_uploaded_tunes_to_csv(list_of_tunes):
    with open('list_of_tunes.csv', 'w') as f:
        writer = csv.writer(f)
        writer.writerow(list_of_tunes)

def get_old_tunes_from_csv():
    with open('list_of_tunes.csv', 'r') as tunes:
        reader = csv.reader(tunes)
        for row in reader:
            return row

def upload_new_tunes(list_of_new_tunes):
    scope = "playlist-modify-public"
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))

    for tune in list_of_new_tunes:
        sp.playlist_add_items(PLAYLIST_ID, [tune])
        
def identify_new_tunes(list_of_all_tunes, old_tunes):
    new_tunes = [item for item in list_of_all_tunes if item not in old_tunes]
    return new_tunes



conversation_file = "message_1.json"

# Uncomment these calls as you like

list_of_all_tunes = get_list_of_tunes_from_file(conversation_file)

old_tunes = get_old_tunes_from_csv()

list_of_new_tunes = identify_new_tunes(list_of_all_tunes, old_tunes)

# upload_new_tunes(list_of_new_tunes)

save_uploaded_tunes_to_csv(list_of_all_tunes)

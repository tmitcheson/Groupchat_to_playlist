import json
import requests
from requests.structures import CaseInsensitiveDict
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
import csv
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
            if(message["content"].startswith("https://open.spotify.com/")):

                message_content = message["content"]

                # cut extra url parameters like fb specification
                tune_link = message_content[:79]

                # the identifyier tag (?si=blahblahblah)
                tune_link = tune_link[:53]

                parameter_tune_link = "spotify:track:" + tune_link[31:]

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
    print(new_tunes)
    return new_tunes



conversation_file = "message_1.json"

list_of_all_tunes = get_list_of_tunes_from_file(conversation_file)

old_tunes = get_old_tunes_from_csv()

list_of_new_tunes = identify_new_tunes(list_of_all_tunes, old_tunes)

upload_new_tunes(list_of_new_tunes)

save_uploaded_tunes_to_csv(list_of_all_tunes)




















# print(list_of_tunes)

# url = "https://api.spotify.com/v1/playlists/1A5jPs20h5bPMAllh9zHCH/tracks"

# headers = CaseInsensitiveDict()
# headers["Accept"] = "application/json"
# headers["Content-Type"] = "application/json"
# headers["Authorization"] = "Bearer BQCSTstFkjf_-oGb-C-SHeV8GfIEXY2BQMOOp_sUA-EO8BWF6WK93FV4r_kkiQKXNB4TlsVxkks38n7Y1oYya4QD3nW4UEVkDdyfVy4KgnqHyyJuZytHE8MPM_k04_q8MZEjnGjiCz2iZKh_d6fKBQ80KxEbITVchxuDVsIDWv0AZ6-i9v3XM-BLR-OWaBl_S-Y7eyRCj-xb9g"
# headers["Content-Length"] = "0"

# params = CaseInsensitiveDict()
# params["position"] = "0"

# for tune in list_of_tunes:
#     params["uris"] = tune
#     resp = requests.post(url, headers=headers, params=params)
#     print(resp.content)




# # https://open.spotify.com/track/3FpRoDRfpSJzv2oNuJ2zGj?si=9fda3f0c86f247f3"
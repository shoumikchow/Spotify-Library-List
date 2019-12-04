import argparse
import csv
import math
import operator

from tqdm import tqdm

import spotipy
import spotipy.util as util

parser = argparse.ArgumentParser()
parser.add_argument('-id',
                    '--client_id',
                    help='enter client id from developer.spotify.com')
parser.add_argument('-secret',
                    '--client_secret',
                    help='enter client secret from developer.spotify.com')

parser.add_argument('-u',
                    '--username',
                    help='enter your spotify username')

scope = 'user-library-read'
username = args.username

args = parser.parse_args()

token = util.prompt_for_user_token(username,
                                   scope,
                                   client_id=args.client_id,
                                   client_secret=args.client_secret,
                                   redirect_uri='http://localhost/')

total = int(input("Enter total number of songs in your library: "))

songs_artists_albums = []
sp = spotipy.Spotify(auth=token)
for i in tqdm(range(math.ceil(total / 20))):
    results = sp.current_user_saved_tracks(offset=20 * i)
    for item in results['items']:
        track = item['track']
        songs_artists_albums.append([
            track['name'], track['artists'][0]['name'], track['album']['name'],
            track['external_urls']['spotify']
        ])

sortedlist = sorted(songs_artists_albums, key=operator.itemgetter(1))

for i in sortedlist:
    with open('spotify_list.csv', 'a') as out:
        writer = csv.writer(out)
        writer.writerow([i[0], i[1], i[2], i[3]])

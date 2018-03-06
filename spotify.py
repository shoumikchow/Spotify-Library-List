import spotipy
import spotipy.util as util
import csv
import math
from tqdm import tqdm
import operator

scope = 'user-library-read'
username = 'shoumikchow'

token = util.prompt_for_user_token(username, scope, client_id='client_id', client_secret='client_secret', redirect_uri='http://localhost/')

total = int(input("Enter total number of songs in your library: "))

songs_artists_albums = []
sp = spotipy.Spotify(auth=token)
for i in tqdm(range(math.ceil(total / 20))):
    results = sp.current_user_saved_tracks(offset=20 * i)
    for item in results['items']:
        track = item['track']
        songs_artists_albums.append([track['name'], track['artists'][0]['name'], track['album']['name'], track['external_urls']['spotify']])

sortedlist = sorted(songs_artists_albums, key=operator.itemgetter(1))

for i in sortedlist:
    with open('spotify_list.csv', 'a') as out:
        writer = csv.writer(out)
        writer.writerow([i[0], i[1], i[2], i[3]])

LASTFM_KEY = "{Insert_lastfm_key_here}"
LASTFM_SECRET = "{Insert_lastfm_secret_here}"
SPOTIFY_KEY = "{Insert_spotify_app_key_here}"
SPOTIFY_SECRET = "{Insert_spotify_app_secret_here}"

VERBOSE = True

import pylast, os, spotipy
from spotipy.oauth2 import SpotifyOAuth

def verboseprint(message):
    if VERBOSE:
        print(message)

#last.fm auth
def lastfmauth():
    SESSION_KEY_FILE = os.path.join(os.path.expanduser("~"), ".session_key")
    network = pylast.LastFMNetwork(LASTFM_KEY, LASTFM_SECRET)
    if not os.path.exists(SESSION_KEY_FILE):
        skg = pylast.SessionKeyGenerator(network)
        url = skg.get_web_auth_url()

        print(f"Please authorize this script to access your account: {url}\n")
        import time
        import webbrowser

        webbrowser.open(url)

        while True:
            try:
                session_key = skg.get_web_auth_session_key(url)
                with open(SESSION_KEY_FILE, "w") as f:
                    f.write(session_key)
                break
            except pylast.WSError:
                time.sleep(1)
    else:
        session_key = open(SESSION_KEY_FILE).read()

    network.session_key = session_key
    return network

#spotify
def spotifyauth():
    return spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=SPOTIFY_KEY,
                                        client_secret=SPOTIFY_SECRET,
                                        redirect_uri="http://localhost:42010",
                                        scope="user-library-read"))


def show_tracks(results):
    for item in results['items']:
        track = item['track']
        verboseprint("%32.32s %s" % (track['artists'][0]['name'], track['name']))
        track = network.get_track(track['artists'][0]['name'], track['name'])
        track.love()

verboseprint("Authenticating Spotify...")
sp = spotifyauth()
verboseprint("Done\nAuthenticating Last.fm")
network = lastfmauth()
verboseprint("Done!\nStarting...")

results = sp.current_user_saved_tracks()
show_tracks(results)

while results['next']:
    results = sp.next(results)
    show_tracks(results)

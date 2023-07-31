# LastLovedSyncify
A quick and dirty script to iterate over the spotify liked songs and love them on lastfm

## Install
Required for this script to work are the following python libraries:
- pylast
- os (probably preinstalled)
- spotipy

Install these using the following command:
```
pip install pylast os spotipy
```

## Run
Make sure to insert your api keys and secrets into the variable fields at the top of the python file

### 1. Last.fm
For LastFM, get a developer account [here](https://www.last.fm/api/account/create) (no new account creation required, unless you don't already have a last.fm account) and then apply for an api key. Insert the key and secret into the dedicated fields in the python file

### 2. Spotify
For Spotify head over to the [developer dashboard](https://developer.spotify.com/dashboard) and create a new app. as the redirect URI input `http://localhost:42010` (or a custom one and change it in the python code) and after creation, insert the key and secret into the dedicated fields in the python file.

#### Example
```
LASTFM_KEY = "aCDwi6Jvu5LrYrwQ248cxUJwjSqS3Y"
LASTFM_SECRET = "xKBYQCrz9yav3Yo9ncAQS2mahELgH3"
SPOTIFY_KEY = "48iTEzmsvNg8H33ccyyKRB786ZM5Di"
SPOTIFY_SECRET = "Diusmu8mefab5CXx5ttSpjoFj3nZFS"

SPOTIFY_REDIRECT_URI="http://localhost:42010"
```

### 3. Verbose logging
Verbose logging is enabled by default with the `VERBOSE` boolean constant. Setting it to false will stop printing anything to the console which might reduce runtime. Depending on the size of the liked songs playlist on Spotify the impact this has, may be noticable (very unlikely).

#### Example
```
ETA:1min     [2591/2596]                        Artist-1 Song-1
ETA:0min     [2592/2596]               Another-Artist-69 Some-Other-Song-420

```

## Notice
- The more liked songs in Spotify, the longer it takes (Took about 15mins for rougly 2500 songs for me)
- Unknown songs are skipped and there's no way for me to detect it.
- This script likely only works with a Spotify PREMIUM account
- The script works from the most recent liked song downwards

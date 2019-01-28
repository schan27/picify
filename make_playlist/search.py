import flask
from dotenv import load_dotenv
load_dotenv()
import os
import random
import requests
import json

def search(search_terms):
    access_token = flask.session.get("access_token")
    songs = []
    for term in search_terms[:5]:
        search_response = requests.get(
            'https://api.spotify.com/v1/search',
            params={'q': term, 'type': 'track'},
            headers={"Authorization": "Bearer " + access_token})

        # print(search_response)

        for track in search_response.json()["tracks"]["items"]:
            artists = [artist["name"] for artist in track["artists"]]
            if len(artists) == 1:
                artists = artists[0]
            elif len(artists) == 2:
                artists = " & ".join(artists)
            else:
                artists = ", ".join(artists[:-1]) + " & " + artists[-1]

            song_details = dict(
                id=track["id"],
                name=track["name"],
                artists=artists,
            )
            songs.append(song_details)
    # flask.session['songs'] = songs
    # print(flask.session.get('songs'))
    return songs


def search_by_playlist(search_terms):
    # Get Spotify token
    access_token = flask.session.get("access_token")

    # Magic numbers
    search_terms_used = 5
    playlists_per_keyword = 5
    tracks_per_playlist = 3

    songs = []

    for term in search_terms[:search_terms_used]:
        playlist_response = requests.get(
            "https://api.spotify.com/v1/search",
            params={"q": term, "type": "playlist", "limit": playlists_per_keyword},
            headers={"Authorization": "Bearer " + access_token},
        )

        for playlist in playlist_response.json()["playlists"]["items"]:
            tracks_href = playlist["tracks"]["href"]

            tracks_response = requests.get(
                tracks_href,
                params={"limit": tracks_per_playlist},
                headers={"Authorization": "Bearer " + access_token},
            )

            for track_wrapper in tracks_response.json()["items"]:
                track = track_wrapper["track"]

                artists = [artist["name"] for artist in track["artists"]]
                if len(artists) == 1:
                    artists = artists[0]
                elif len(artists) == 2:
                    artists = " & ".join(artists)
                else:
                    artists = ", ".join(artists[:-1]) + " & " + artists[-1]

                song_details = dict(id=track["id"], name=track["name"], artists=artists)
                songs.append(song_details)

    # Randomize the songs we sampled from the above playlists
    random.shuffle(songs)

    return songs

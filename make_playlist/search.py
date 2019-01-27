import flask
from dotenv import load_dotenv
load_dotenv()
import os
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

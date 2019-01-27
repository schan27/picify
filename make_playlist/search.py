import flask
from dotenv import load_dotenv
load_dotenv()
import os
import requests
import json

def search(search_terms):
    access_token = flask.session.get('access_token')
    songs = []

    for term in search_terms[:5]:
        search_response = requests.get(
            'https://api.spotify.com/v1/search',
            params={'q': term, 'type': 'track'},
            headers={"Authorization": "Bearer " + access_token})

        for track in search_response.json()["tracks"]["items"]:
            song_details = dict(
                id=track["id"],
                name=track["name"],
                artists=[artist["name"] for artist in track["artists"]],
            )
            songs.append(song_details)
    # flask.session['songs'] = songs
    # print(flask.session.get('songs'))
    return songs

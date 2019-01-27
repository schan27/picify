import flask
from dotenv import load_dotenv
load_dotenv()
import os
import requests

def search():
    terms = ['sun', 'fun', 'love']
    access_token = flask.session.get('access_token')
    
    search_request = requests.get('https://api.spotify.com/v1/search', params={'q': 'sun', 'type': 'album,artist,playlist,track'}, headers={"Authorization": "Bearer " + access_token})

    print(search_request.json())

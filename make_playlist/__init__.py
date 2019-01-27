from make_playlist import image_parse, search, whitelist, spotify_playlist
from google.oauth2 import service_account
import flask
import io
import os

APP_BASE = os.path.dirname(os.path.realpath(__file__))

credentials = service_account.Credentials.from_service_account_file(
    os.path.join(os.path.dirname(APP_BASE), "gcp_credentials.json")
)

def get_search_terms(filepath):
    with io.open(filepath, "rb") as image_file:
        raw_image = image_file.read()
    image_details = image_parse.parse_image(raw_image, credentials)
    # set the playlist name from the 'best guess' from Google
    flask.session['playlist_name'] = image_details['title']
    search_terms = image_details['labels']
    return search_terms


def get_songs(search_terms):
    # TODO: add adjectives and whitelist logic
    return search.search(search_terms)

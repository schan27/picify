from make_playlist import image_parse, search, whitelist, spotify_playlist, words_associate
from google.oauth2 import service_account
import flask
import io
import os

APP_BASE = os.path.dirname(os.path.realpath(__file__))

credentials = service_account.Credentials.from_service_account_file(
    os.path.join(os.path.dirname(APP_BASE), "gcp_credentials.json")
)

def get_search_terms(filepath):
    # Read image
    with io.open(filepath, "rb") as image_file:
        raw_image = image_file.read()

    # Iteratively reduce confidence threshold until we get some terms
    confidence_threshold = 0.9
    search_terms = []

    while not search_terms:
        # Analyse image
        image_details = image_parse.parse_image(raw_image, credentials, confidence_threshold)

        # Grab adjectives of all the labels and web entities
        word_cluster = image_details["labels"] + image_details["web_entities"]
        adjectives_cluster = []

        for word in word_cluster:
            adjectives_cluster += words_associate.get_associated_adjectives(word, 1)

        # Grab the intersection of the whitelist and all the words
        word_cluster_set = set(word_cluster + adjectives_cluster)
        whitelisted_words_set = word_cluster_set & whitelist.whitelist

        search_terms = list(whitelisted_words_set)

        if not search_terms:
            confidence_threshold -= 0.1

        # Always include the highest confidence web entity
        if image_details["web_entities"]:
            search_terms.insert(0, image_details["web_entities"][0])

    # set the playlist name from the 'best guess' from Google
    flask.session['playlist_name'] = image_details['title']

    return search_terms


def get_songs(search_terms):
    # TODO: add adjectives and whitelist logic
    return search.search(search_terms)

#!/usr/bin/env python3

import io
import os
from google.oauth2 import service_account
from make_playlist.image_parse import parse_image
from make_playlist.words_associate import get_associated_adjectives
from make_playlist.whitelist import whitelist


def main():
    """Runs the image processing script."""
    # GCP credentials
    credentials = service_account.Credentials.from_service_account_file(
        "gcp_credentials.json"
    )

    # Loads an image into memory
    file_name = os.path.join(os.path.dirname(__file__), "testimage.jpg")

    with io.open(file_name, "rb") as image_file:
        raw_image = image_file.read()

    # Analyse the image
    image_details = parse_image(raw_image, credentials, confidence_threshold=0.9)

    # Grab adjectives of all the labels and web entities
    word_cluster = image_details["labels"] + image_details["web_entities"]
    adjectives_cluster = []

    for word in word_cluster:
        adjectives_cluster += get_associated_adjectives(word, 1)

        # DEBUG printing!
        adjectives = get_associated_adjectives(word, 1)
        print(word)
        print(adjectives)
        print()

    # Grab the intersection of the whitelist and all the words
    word_cluster_set = set(word_cluster + adjectives_cluster)
    whitelisted_words_set = word_cluster_set & whitelist

    # DEBUG see what was whitelisted out
    print("REMOVED WORDS")
    print(word_cluster_set - whitelisted_words_set)
    print()
    print("WORDS WE KEEP")
    print(whitelisted_words_set)


if __name__ == "__main__":
    # Run it
    main()

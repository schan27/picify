#!/usr/bin/env python3

import io
import os
from google.oauth2 import service_account
from make_playlist.image_parse import parse_image


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
    responses = parse_image(raw_image, credentials)

    # DEBUG: print responses
    print(responses)

if __name__ == "__main__":
    # Run it
    main()

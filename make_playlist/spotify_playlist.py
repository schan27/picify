"""Create Spotify playlists."""

import flask
import json
import requests


def get_user_id():
    """Return the user's Spotify ID.

    Returns (string):
        The user's Spotify ID (*not their URI).

    Raises:
        AssertionError: The HTTP request to lookup the user failed.
    """
    # Make request and validate
    response = requests.get(
        "https://api.spotify.com/v1/me",
        headers={"Authorization": "Bearer " + flask.session.get("access_token")},
    )

    assert response.status_code == requests.codes.ok

    # Return the user ID
    return response.json()["id"]


def create_empty_playlist(user_id, name, description=None, public=True):
    """Creates an empty Spotify playlist for the user.

    Args:
        user_id (string): The user's Spotify ID.
        name (string): The name of the playlist.
        description (string, optional): The playlist's description.
            Defaults to None.
        public (boolean, optional): A boolean signaling if the playlist
            should be public. Defaults to True.

    Returns (string):
        The full playlist URI. For example,
        "spotify:user:thelinmichael:playlist:7d2D2S200NyUE5KYs80PwO".

    Raises:
        AssertionError: The HTTP request to create the playlist failed.
    """
    # Build request data
    request_data = {"name": name, "public": public}

    if description is not None:
        request_data["description"] = description

    # Make request and validate
    response = requests.post(
        "https://api.spotify.com/v1/users/%s/playlists" % user_id,
        data=json.dumps(request_data),
        headers={"Authorization": "Bearer " + flask.session.get("access_token")},
    )

    assert response.status_code in (requests.codes.ok, requests.codes.created)

    # Return the playlist URI
    return response.json()["uri"]

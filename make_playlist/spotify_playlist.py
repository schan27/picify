"""Create Spotify playlists."""

import flask
import requests


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
        data=request_data,
        headers={"Authorization": "Bearer " + flask.session.get("access_token")},
    )

    assert response.status_code in (response.codes.ok, response.codes.created)

    # Return the playlist URI
    return response.json()["uri"]

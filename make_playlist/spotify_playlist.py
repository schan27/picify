"""Create Spotify playlists."""

import json
import flask
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
        The Spotify playlist ID.

    Raises:
        AssertionError: The HTTP request to create the playlist failed.
    """
    # Build request data
    request_data = {"name": name, "public": public}

    print(json.dumps(request_data))
    if description is not None:
        request_data["description"] = description

    # Make request and validate
    response = requests.post(
        "https://api.spotify.com/v1/users/%s/playlists" % user_id,
        data=json.dumps(request_data),
        headers={"Authorization": "Bearer " + flask.session.get("access_token")},
    )

    print(response.json())

    assert response.status_code in (requests.codes.ok, requests.codes.created)

    # Return the playlist URI
    return response.json()["id"]


def add_songs_to_playlist(playlist_id, song_ids):
    """Add songs to a Spotify playlist.

    The tracks passed in can be of format

    "spotify:track:4iV5W9uYEdYUVa79Axb7Rh"

    or

    "4iV5W9uYEdYUVa79Axb7Rh"

    Either is fine.

    Args:
        playlist_id (string): The playlist's Spotify ID.
        song_ids (list): A list of Spotify track IDs.

    Raises:
        AssertionError: The HTTP request to add the songs failed.
    """
    # Prepend track IDs to form full URI if necessary
    uri_start = "spotify:track:"
    song_ids = [id if id.startswith(uri_start) else uri_start + id for id in song_ids]

    # Make request and validate
    response = requests.post(
        "https://api.spotify.com/v1/playlists/%s/tracks" % playlist_id,
        data=json.dumps({"uris": song_ids}),
        headers={"Authorization": "Bearer " + flask.session.get("access_token")},
    )
    print(response.json())
    assert response.status_code == requests.codes.created


def create_spotify_playlist_with_songs(
    song_ids, playlist_name, playlist_description=None, playlist_public=True
):
    """Create a Spotify playlist with songs.

    Args:
        song_ids (list): A list of Spotify track IDs.
        playlist_name (string): The name of the playlist.
        playlist_description (string, optional): The playlist's
            description.  Defaults to None.
        playlist_public (boolean, optional): A boolean signaling if the
            playlist should be public. Defaults to True.
    """
    # Grab the user's ID
    user_id = get_user_id()
    print('playlist name: ' + playlist_name)
    # Create a playlist
    playlist_id = create_empty_playlist(
        user_id, playlist_name, description=playlist_description, public=playlist_public
    )

    # Add songs to the playlist
    add_songs_to_playlist(playlist_id, song_ids)

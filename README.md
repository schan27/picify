# :city_sunset: Picify :headphones:

**Picify** is a [Flask](http://flask.pocoo.org) application that converts your photos into Spotify playlists that can be saved for later listening, providing a uniquely personal way to explore new music. The experience is facilitated by interacting and integrating a wide range of services.

## Resources
This app uses [Google Cloud Vision](https://cloud.google.com/vision/) to extract key terms from the image, searches for songs and creates playlists using the [Spotify API](https://developer.spotify.com/documentation/web-api/), and uses [Azure](https://portal.azure.com) for deployment.

It can also incorporate genre information by searching [AllMusic](https://www.allmusic.com/moods) and [Every Noise at Once](http://everynoise.com/genrewords.html), and extends the search terms by searching for semantically similar words using the [Datamuse API](https://www.datamuse.com/api/).

## Contributors
- [Macguire Rintoul](https://github.com/mrintoul)
- [Matt Wiens](https://github.com/mwiens91)
- [Sophia Chan](https://github.com/schan27)

## Screenshots
![Landing Page](./product/landing.png)

![Upload Page](./product/upload.png)

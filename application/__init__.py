import flask
from dotenv import load_dotenv
load_dotenv()
import os
from base64 import urlsafe_b64encode
import requests
from werkzeug.utils import secure_filename

import make_playlist

APP_BASE = os.path.dirname(os.path.realpath(__file__))

UPLOAD_FOLDER = os.path.join(APP_BASE, "images")

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app = flask.Flask(__name__)
app.secret_key = os.getenv('secret_key')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# http://flask.pocoo.org/docs/1.0/patterns/fileuploads/
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def index():
    if (flask.request.args.get('code') != None):
        authorization_code = flask.request.args.get('code', '')
        flask.session['authorization_code'] = authorization_code
        base64_encoded_auth = urlsafe_b64encode(bytes(os.getenv("client_id") + ":" + os.getenv("client_secret"), "utf-8")).decode()

        token_request = requests.post('https://accounts.spotify.com/api/token', data={"grant_type": "authorization_code", "code": authorization_code, "redirect_uri": "http://localhost:5000"}, headers={'content-type': 'application/x-www-form-urlencoded', "Authorization": "Basic " + base64_encoded_auth})

        access_token = token_request.json()["access_token"]
        flask.session['access_token'] = access_token

    return flask.render_template('index.html', authorization_code=flask.session.get('authorization_code', None), client_id=os.getenv('client_id'), redirect_uri=os.getenv('redirect_uri'))

@app.route('/playlist', methods=['POST'])
def upload_file(name=None):
    if flask.request.method == 'POST':
        # check if the post flask.request has the file part
        if 'file' not in flask.request.files:
            flask.flash('No file part')
            return flask.redirect(flask.request.url)
        file = flask.request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flask.flash('No selected file')
            return flask.redirect(flask.request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            songs = make_playlist.get_songs(filepath)
            return flask.render_template('playlist.html', songs=songs)

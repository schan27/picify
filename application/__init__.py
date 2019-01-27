import flask
import os
import io
from werkzeug.utils import secure_filename
from make_playlist import image_parse
from google.oauth2 import service_account

APP_BASE = os.path.dirname(os.path.realpath(__file__))

UPLOAD_FOLDER = os.path.join(APP_BASE, "images")

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

credentials = service_account.Credentials.from_service_account_file(
    os.path.join(os.path.dirname(APP_BASE), "grp_credentials.json")
)

app = flask.Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# http://flask.pocoo.org/docs/1.0/patterns/fileuploads/
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
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
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return flask.redirect(flask.url_for('parse_image',
                                    filename=filename))
    return flask.render_template('index.html', name=name)


@app.route('/parse/<filename>')
def parse_image(filename):
    image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    with io.open(image_path, "rb") as image_file:
        raw_image = image_file.read()
    result = image_parse.parse_image(raw_image, credentials)
    return " ".join(result["labels"])

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return flask.send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)

@app.route('/hello/')
@app.route('/hello/<name>')
def hello(name=None):
    return flask.render_template('hello.html', name=name)

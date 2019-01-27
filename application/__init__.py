import flask
import os
from werkzeug.utils import secure_filename


UPLOAD_FOLDER = os.path.join(
    os.path.dirname(os.path.realpath(__file__)),
    "images"
)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app = flask.Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# http://flask.pocoo.org/docs/1.0/patterns/fileuploads/
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
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
            return flask.redirect(flask.url_for('uploaded_file',
                                    filename=filename))
    return flask.render_template('index.html', name=name)

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return flask.send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)

@app.route('/hello/')
@app.route('/hello/<name>')
def hello(name=None):
    return flask.render_template('hello.html', name=name)

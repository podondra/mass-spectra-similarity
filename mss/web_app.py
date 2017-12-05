import os
from . import app
from flask import render_template, request, redirect, url_for, flash
from flask_pymongo import PyMongo
from werkzeug.utils import secure_filename
from .similarity import detect_similar
from .spectra import read_mgf


# TODO db generation view
# TODO results view
# TODO result view
# TODO result's spectra visualization view


ALLOWED_EXTENSIONS = set(['mgf', 'fasta'])


app.config['SECRET_KEY'] = os.urandom(24)
app.config['MONGO_DBNAME'] = 'mss'
app.config['MONGO_URI'] = 'mongodb://localhost:27017/mss'


mongo = PyMongo(app)


# TODO merge with upload_mgf
@app.route('/')
def index():
    return render_template('index.html')


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# TODO allow to choose which ionts to compare b, y, a and all combination
# TODO allow to choose which charge to compare 1, 2, 3, ...
@app.route('/upload/', methods=['GET', 'POST'])
def upload_mgf():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('no file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('no selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            mongo.save_file(filename, file)
            return redirect(url_for('results'))
    else:
        return render_template('upload.html')


@app.route('/result/')
def results():
    files = mongo.db.fs.files.find()
    spectra = read_mgf(next(files).read())
    return str(spectra)
    detect_similar(spectra)
    return render_template('results.html')

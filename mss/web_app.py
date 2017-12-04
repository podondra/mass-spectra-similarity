import os
import time
from . import app
from flask import render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
from .similarity import detect_similar
from .spectra import read_mgf


ALLOWED_EXTENSIONS = set(['mgf', 'fasta'])
UPLOAD_FOLDER = os.path.join(os.sep, 'tmp')

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SECRET_KEY'] = os.urandom(24)


@app.route('/')
def index():
    return render_template('index.html')


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


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
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('similarity_view', filename=filename))
    else:
        return render_template('upload.html')


@app.route('/similarity/<filename>')
def similarity_view(filename):
    start = time.time()
    path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    spectra = read_mgf(path)
    similarities = detect_similar(spectra)
    end = time.time()
    return render_template('similarities.html', similarities=similarities,
                           time=(end - start))

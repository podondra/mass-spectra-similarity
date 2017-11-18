import os
from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
import random # TODO delete
from pyteomics import mgf
from .similarity import detect_similar


ALLOWED_EXTENSIONS = set(['mgf'])
UPLOAD_FOLDER = os.path.join(os.sep, 'tmp')

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SECRET_KEY'] = 'development key'


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET', 'POST'])
def upload_file():
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

    return '''
    <!doctype html>
    <title>upload mgf file</title>
    <h1>upload mgf file</h1>
    <form method="post" enctype="multipart/form-data">
      <p><input type="file" name="file">
         <input type="submit" value="upload">
    </form>
    '''


# TODO move to other module. import problem with app object
def read_mgf(filename):
    path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    with mgf.read(path) as reader:
        spectra = list(reader)
    return spectra


@app.route('/similarity/<filename>')
def similarity_view(filename):
    spectra = read_mgf(filename)
    # TODO for all spectra in the file
    #for spectrum in spectra:
    spectrum = random.choice(spectra)
    similar_spectra = detect_similar(spectrum)
    # TODO view
    return str(similar_spectra)

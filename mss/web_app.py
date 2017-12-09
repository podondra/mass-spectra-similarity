import os
import io
from . import app
from flask import render_template, request, redirect, url_for, jsonify
from flask_pymongo import PyMongo
# from werkzeug.utils import secure_filename
from .similarity import detect_similar
from .spectra import read_mgf
from .db import get_db


app.config['SECRET_KEY'] = os.urandom(24)
app.config['MONGO_DBNAME'] = 'mss'
app.config['MONGO_URI'] = 'mongodb://localhost:27017/mss'


mongo = PyMongo(app)
# TODO document
PEPTIDES, MZS, DATABASE = get_db('data/db.npz')


def allowed_file(filename, extension):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() == extension


# TODO allow to choose which ionts to compare b, y, a and all combination
# TODO allow to choose which charge to compare 1, 2, 3
# TODO allow to choose number of returned similarities, the k parameter
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            return redirect(request.url)
        if file and allowed_file(file.filename, 'mgf'):
            # filename = secure_filename(file.filename)
            # convert bytes file to string file
            stringio = io.StringIO(file.read().decode('utf-8'))
            spectra = read_mgf(stringio)
            indexes = detect_similar(spectra, DATABASE, k=2)
            spectra_list = [{
                'mz': spectrum['m/z array'].tolist(),
                'intensity': spectrum['intensity array'].tolist(),
                'indexes': index.tolist(),
                } for spectrum, index in zip(spectra, indexes)]
            spectra_col = mongo.db.spectra
            spectra_ids = spectra_col.insert_many(spectra_list).inserted_ids

            result = {'spectra': spectra_ids}
            result_id = mongo.db.results.insert_one(result).inserted_id
            return redirect(url_for('results', result_id=result_id))

    return render_template('index.html')


@app.route('/result/')
@app.route('/result/<ObjectId:result_id>')
def results(result_id=None):
    if result_id is None:
        results = mongo.db.results.find()
        return render_template('results.html', results=results)
    else:
        result = mongo.db.results.find_one({'_id': result_id})
        return render_template('result.html', result=result)


@app.route('/spectrum/<ObjectId:spectrum_id>')
def spectrum(spectrum_id):
    spectrum = mongo.db.spectra.find_one({'_id': spectrum_id})
    similar = [(index, PEPTIDES[index]) for index in spectrum['indexes']]
    return render_template('spectrum.html', spectrum_id=spectrum_id,
                           similar=similar)


@app.route('/spectrum/<ObjectId:spectrum_id>.json')
def spectrum_json(spectrum_id):
    spectrum = mongo.db.spectra.find_one({'_id': spectrum_id})
    mz_intensity = [{'mz': mz, 'intensity': i}
                    for mz, i in zip(spectrum['mz'], spectrum['intensity'])]
    return jsonify(mz_intensity)


@app.route('/db/')
def db():
    n_spectra, bins = DATABASE.shape
    return render_template('db.html', n_spectra=n_spectra, bins=bins)


@app.route('/db/<int:index>.json')
def database_json(index):
    mzs = MZS[index]
    mz_intensity = [{'mz': mz, 'intensity': 1}
                    for mz in mzs]
    return jsonify(mz_intensity)

import numpy
from sklearn.metrics.pairwise import cosine_similarity
from .spectra import bin_spectrum
from .db import get_db


def bin_spectra(spectra, bins):
    mz_matrix = numpy.zeros((len(spectra), bins))
    for i, spectrum in enumerate(spectra):
        mz = spectrum['m/z array']
        intensities = spectrum['intensity array']
        mz_matrix[i, :] = bin_spectrum(mz, intensities, bins)
    return mz_matrix


def detect_similar(spectra, bins=13000):
    mz_matrix = bin_spectra(spectra, bins)
    # get database
    db_peptides, db_mz, db_binned = get_db('data/db.npz')
    # compute similarity matrix
    similarities = cosine_similarity(mz_matrix, db_binned)
    # choose top 5 for each spectrum
    index = numpy.flip(numpy.argsort(similarities)[:, -5:], axis=-1)
    top_peptides = db_peptides[index]
    top_mz = db_mz[index]
    return top_peptides, top_mz

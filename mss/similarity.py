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


# TODO experiment with bin sizes 0.1, 0.5, 1
def detect_similar(spectra, k, bins=13000):
    mz_matrix = bin_spectra(spectra, bins)
    # get database
    db_peptides, db_mz, db_binned = get_db('data/db.npz')
    # compute similarity matrix
    similarities = cosine_similarity(mz_matrix, db_binned)
    # choose top 5 for each spectrum
    index = numpy.flip(numpy.argsort(similarities)[:, -k:], axis=-1)
    top_peptides = db_peptides[index]
    top_mz = db_mz[index]
    return top_peptides, top_mz

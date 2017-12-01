import numpy
from sklearn.metrics.pairwise import cosine_similarity
from .preprocessing import bin_spectrum
from .db import get_db


def detect_similar(spectra):
    bins = 13000
    mz_matrix = numpy.zeros((len(spectra), bins))
    for i, spectrum in enumerate(spectra):
        mz = spectrum['m/z array']
        intensities = spectrum['intensity array']
        mz_matrix[i, :] = bin_spectrum(mz, intensities, bins)

    # get database
    db_peptides, db_mz, db_binned = get_db()
    # compute similarity matrix
    similarities = cosine_similarity(mz_matrix, db_binned)
    # choose top 5 for each spectrum
    index = numpy.flip(numpy.argsort(similarities)[:, -5:], axis=-1)
    top_petides = db_peptides[index]
    top_mz = db_mz[index]

    return [{'spectrum': spectrum, 'peptides': top_petides[i], 'mz': top_mz[i]}
            for i, spectrum in enumerate(spectra)]

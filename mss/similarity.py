import numpy
from sklearn.metrics.pairwise import cosine_similarity
from .spectra import bin_spectrum


def bin_spectra(spectra, bins):
    mz_matrix = numpy.zeros((len(spectra), bins))
    for i, spectrum in enumerate(spectra):
        mz = spectrum['m/z array']
        intensities = spectrum['intensity array']
        mz_matrix[i, :] = bin_spectrum(mz, intensities, bins)
    return mz_matrix


# TODO experiment with bin sizes 0.1, 0.5, 1
def detect_similar(spectra, database, k=5, bins=13000):
    mz_matrix = bin_spectra(spectra, bins)
    # compute similarity matrix
    similarities = cosine_similarity(mz_matrix, database)
    # choose top 5 for each spectrum
    index = numpy.flip(numpy.argsort(similarities)[:, -k:], axis=-1)
    return index

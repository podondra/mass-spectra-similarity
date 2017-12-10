import numpy
from sklearn.metrics.pairwise import cosine_similarity
from .spectra import bin_spectrum
from scipy.sparse import lil_matrix


def bin_spectra(spectra, bins=3871):
    mz_matrix = lil_matrix((len(spectra), bins))
    for i, spectrum in enumerate(spectra):
        mz = spectrum['m/z array']
        intensities = spectrum['intensity array']
        mz_matrix[i, :] = bin_spectrum(mz, intensities, bins)
    return mz_matrix


def knn_query(spectra_mat, db_mat, k):
    n_spectra = spectra_mat.shape[0]
    similarities = cosine_similarity(spectra_mat, db_mat, dense_output=False)
    result = numpy.zeros((n_spectra, k), dtype=numpy.int32)
    for i in range(n_spectra):
        result[i, :] = numpy.argsort(similarities.getrow(i).toarray()[0])[-k:]
    return result

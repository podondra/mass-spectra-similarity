import numpy
from sklearn.metrics.pairwise import cosine_similarity
from .preprocessing import compute_mass_spectrum_wrapper, bin_spectrum
from .db import get_db


def detect_similar(spectrum):
    ms = bin_spectrum(compute_mass_spectrum_wrapper(spectrum))
    names, db = get_db()

    # TODO all spectra at once
    similarities = cosine_similarity(ms.reshape(1, -1), db).reshape(-1)
    # top 5
    index = numpy.argsort(similarities)[-5:]
    return numpy.flip(names[index], axis=0)

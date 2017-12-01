import numpy


def get_db():
    # TODO improve, e.g. memory maping
    # TODO make sure that peptides are unique
    npz = numpy.load('data/db.npz')
    # first array are peptides
    # second are mz values
    # third are binned values
    return npz['names'], npz['mzs'], npz['binneds']

import numpy


def get_db():
    # TODO improve, e.g. memory maping
    # TODO make sure that peptides are unique
    npz = numpy.load('data/db.npz')
    return npz['names'], npz['db']

import numpy
from pyteomics import mass, mgf
from scipy.stats import binned_statistic


def read_mgf(mgf_file):
    with mgf.read(mgf_file) as reader:
        spectra = list(reader)
    return spectra


# TODO add y and a ionts
def b_ionts(sequence):
    return [sequence[:i] for i in range(1, len(sequence))]


# TODO for theoretical peptide precompute with charge 1, 2, 3, ...
def compute_mass_spectrum(sequence, charge=1):
    # TODO sometimes sequence contains '+' and other characters INGORE them
    # TODO ignore peptides which contains modifications in db generation
    spectrum = numpy.zeros(len(sequence) - 1)
    for i, iont in enumerate(b_ionts(sequence)):
        spectrum[i] = mass.calculate_mass(sequence=iont, ion_type='b',
                                          charge=charge)
    return spectrum


# TODO compute mz range from spectra given as test data
def bin_spectrum(mz, intensity=None, bins=13000, mz_range=(0, 1300)):
    intensity = intensity if intensity is not None else numpy.ones_like(mz)
    binned, _, _ = binned_statistic(mz, intensity, 'sum', bins, mz_range)
    return binned

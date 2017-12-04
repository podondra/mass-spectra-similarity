import numpy
from pyteomics import mass, mgf
from scipy.stats import binned_statistic


ALLOWED_AMINO_ACIDS = 'ARNDCFQEGHILKMPSTWYV'


def read_mgf(mgf_file):
    with mgf.read(mgf_file) as reader:
        spectra = list(reader)
    return spectra


def b_ionts(sequence):
    return [sequence[:i] for i in range(1, len(sequence))]


# TODO charge for theoretical spectra?
def compute_mass_spectrum(sequence, charge=1):
    # TODO sometimes sequence contains '+' and other characters
    sequence = ''.join([c for c in sequence if c in ALLOWED_AMINO_ACIDS])
    spectrum = numpy.zeros(len(sequence) - 1)
    for i, iont in enumerate(b_ionts(sequence)):
        spectrum[i] = mass.calculate_mass(sequence=iont, ion_type='b',
                                          charge=charge)
    return spectrum


# TODO if binned to small number of bins then theoretical spectrum might
# have intensity of 2, is it right?
# TODO what mz range? compute it?
def bin_spectrum(mz, intensity=None, bins=13000, mz_range=(0, 1300)):
    intensity = intensity if intensity is not None else numpy.ones_like(mz)
    binned, _, _ = binned_statistic(mz, intensity, 'sum', bins, mz_range)
    return binned

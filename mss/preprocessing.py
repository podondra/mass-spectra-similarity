import numpy
from pyteomics import mass
from scipy.stats import binned_statistic


# TODO only for database generation
ALLOWED_AMINO_ACIDS = 'ARNDCFQEGHILKMPSTWYV'


# TODO only for database generation
def b_ionts(sequence):
    return [sequence[:i] for i in range(1, len(sequence))]


# TODO charge for theoretical spectra?
# TODO only for database generation
def compute_mass_spectrum(sequence, charge=1):
    # TODO sometimes sequence contains '+' and other characters
    sequence = ''.join([c for c in sequence if c in ALLOWED_AMINO_ACIDS])
    return [mass.calculate_mass(sequence=iont, ion_type='b', charge=charge)
            for iont in b_ionts(sequence)]


# TODO if binned to small number of bins then theoretical spectrum might
# have intensity of 2, is it right?
def bin_spectrum(m_z, intensity=None, bins=13000, m_z_range=(0, 1300)):
    intensity = intensity if intensity is not None else numpy.zeros(len(m_z))
    # TODO what m_z range? compute it?
    binned, _, _ = binned_statistic(m_z, intensity, statistic='sum',
                                    bins=bins, range=m_z_range)
    return binned

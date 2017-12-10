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


def compute_mass_spectrum(sequence, charge=1):
    spectrum = numpy.zeros(len(sequence) - 1)
    for i, iont in enumerate(b_ionts(sequence)):
        spectrum[i] = mass.calculate_mass(sequence=iont, ion_type='b',
                                          charge=charge)
    return spectrum


# mz_range is given from statistic by test data opal_annotated.mgf
#   and amethyst_annotated.mgf
def bin_spectrum(mz, intensity=None, bins=3871, mz_range=(150, 4021)):
    intensity = intensity if intensity is not None else numpy.ones_like(mz)
    binned, _, _ = binned_statistic(mz, intensity, 'sum', bins, mz_range)
    return binned

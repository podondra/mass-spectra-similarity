from pyteomics import mass
from scipy.stats import binned_statistic


ALLOWED_AMINO_ACIDS = 'ARNDCFQEGHILKMPSTWYV'


def b_ionts(sequence):
    return (sequence[:i] for i in range(1, len(sequence)))


def compute_spectrum(spectrum):
    # TODO charge?
    charge = spectrum['params']['charge'][0]
    orig_sequence = spectrum['params']['peptide']
    # TODO sometimes sequence contains '+' and other characters
    sequence = ''.join([c for c in orig_sequence if c in ALLOWED_AMINO_ACIDS])
    return [mass.calculate_mass(sequence=iont, ion_type='b', charge=charge)
            for iont in b_ionts(sequence)]


def bin_spectrum(m_z, intensity, bins=13000, m_z_range=(0, 1300)):
    # TODO what m_z_range? compute it?
    binned, _, _ = binned_statistic(m_z, intensity, statistic='sum',
                                    bins=bins, range=m_z_range)
    return binned



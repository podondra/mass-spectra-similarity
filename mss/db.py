import numpy
from pyteomics import fasta
from .spectra import bin_spectrum, compute_mass_spectrum


def generate_peptides(protein):
    peptides = set()
    peptide = ''
    for i in range(len(protein) - 1):
        peptide += protein[i]
        if (protein[i] == 'K' or protein[i] == 'R') and protein[i + 1] != 'P':
            if len(peptide) > 0:
                peptides.add(peptide)
            peptide = ''
    return peptides


# TODO implement database generation
# TODO add view for db generation
# TODO come up with right location of db
def generate_db(fasta_file, bins=13000):
    peptides = set()
    with fasta.read(fasta_file) as db:
        for _, protein in db:
            peptides |= generate_peptides(protein)

    mzs = list()
    for peptide in peptides:
        mzs.append(compute_mass_spectrum(peptide))

    # TODO dtype
    intensity_matrix = numpy.zeros((len(peptides), bins))
    for i, intensity in enumerate(mzs):
        intensity_matrix[i, :] = bin_spectrum(mzs[i], bins=bins)

    peptides_vector = numpy.array(list(peptides))
    mzs_vector = numpy.array(mzs)
    return peptides_vector, mzs_vector, intensity_matrix


def get_db(db_file):
    # TODO improve, e.g. memory maping
    # TODO make sure that peptides are unique
    npz = numpy.load(db_file)
    # first array is peptides, second is mz values, third is binned intensities
    return npz['peptides'], npz['mzs'], npz['intensity_matrix']

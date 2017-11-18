from .preprocessing import compute_spectrum


def detect_similar(spectrum):
    mass_spectrum = compute_spectrum(spectrum)
    return mass_spectrum

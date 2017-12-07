# Mass Spectra Similarity (Bioinformatics)

MI-VMM project at FIT Czech Technical University.

## Assigment

Project's goal is to implement application which searches peptide sequence
in protein sequence database according to similarity to input mass spectrum.

### Input

Mass spectrum and protein sequence database.

### Output

Set of peptide sequences similar to input mass spectra sorted according to
similarity.

## Links

- [An Introduction to Bioinformatics Algorithms](
    http://bix.ucsd.edu/bioalgorithms/
    )
- [IonSource](http://www.ionsource.com/)
- [Protein ID With MS/MS Data](
    http://www.ionsource.com/tutorial/protID/spectralmatching_mascot.htm
    )

## Flask App

To install the application in *editable* mode:

`$ pip install -e .`

To start the app:

`$ export FLASK_APP=mss`
`$ flask run`

Debug mode:

`$ export FLASK_DEBUG=1`
`$ flask run`

## MongoDB

To start database (use `-d` to demonize it):

`docker run -p 27017:27017 --name some-mongo mongo`

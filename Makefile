TARGET = report

all: pdf

pdf: $(TARGET).tex $(TARGET).bib
	pdflatex $(TARGET)
	bibtex $(TARGET)
	pdflatex $(TARGET)
	pdflatex $(TARGET)

clean:
	$(RM) $(TARGET).pdf $(TARGET).aux $(TARGET).log $(TARGET).bbl \
	    $(TARGET).blg

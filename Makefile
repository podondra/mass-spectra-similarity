TARGET = report

all: pdf

pdf: $(TARGET).tex
	pdfcslatex $(TARGET)
	pdfcslatex $(TARGET)

clean:
	$(RM) $(TARGET).pdf $(TARGET).aux $(TARGET).log

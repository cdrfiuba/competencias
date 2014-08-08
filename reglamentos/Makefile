LABERINTO = laberinto
MINISUMO = minisumo
VELOCISTAS = velocistas

all: minisumo velocistas laberinto clean

minisumo:
	pdflatex $(MINISUMO).tex
	pdflatex $(MINISUMO).tex

velocistas:
	pdflatex $(VELOCISTAS)
	pdflatex $(VELOCISTAS)

laberinto:
	pdflatex $(LABERINTO)
	pdflatex $(LABERINTO)

clean:
	rm -rf *.aux *.out *.log

cleanpdf: clean
	rm -rf $(MINISUMO).pdf $(LABERINTO).pdf $(VELOCISTAS).pdf

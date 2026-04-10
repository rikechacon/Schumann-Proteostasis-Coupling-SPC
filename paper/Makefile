# Makefile para compilar el manuscrito LaTeX
# Uso: make, make clean, make view

TEX = manuscript.tex
PDF = manuscript.pdf
BIB = references.bib

# Compilador
LATEX = pdflatex
BIBTEX = bibtex

# Opciones
OPTIONS = -interaction=nonstopmode

all: $(PDF)

$(PDF): $(TEX) $(BIB)
	$(LATEX) $(OPTIONS) $(TEX)
	$(BIBTEX) $(TEX:.tex=)
	$(LATEX) $(OPTIONS) $(TEX)
	$(LATEX) $(OPTIONS) $(TEX)

view: $(PDF)
	xdg-open $(PDF) 2>/dev/null || open $(PDF) 2>/dev/null || start $(PDF)

clean:
	rm -f *.aux *.log *.out *.blg *.bbl *.toc *.lof *.lot *.fls *.fdb_latexmk

.PHONY: all view clean

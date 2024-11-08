DOCNAME = project-report

# Default target
all: black conda-export update-pdf

# Run Black on all Python files
black:
	@echo "Running Black on Python files..."
	@echo "$$(poetry run black . 2>&1)" | sed 's/^/    /'
	@echo

# Export Poetry dependencies to Conda format
conda-export:
	@echo "Running poetry2conda to export latest state of pyproject.toml to environment.yamls..."
	@poetry run poetry2conda pyproject.toml  environment.yaml
	@echo

# Update pdf and explicitly commit it (normally ignored via .gitignore)
update-pdf:
	@echo "Building PDF"
	@cd ./tex; pdflatex -interaction=nonstopmode $(DOCNAME).tex > /dev/null; mv $(DOCNAME).pdf ../$(DOCNAME).pdf
	@git add $(DOCNAME).pdf -f
	@echo "Staging $(DOCNAME).pdf for commit (please complete commit manually)\n"

# Help 
help:
	@echo "Available targets:"
	@echo "  make all  - runs all of the below"
	@echo "  make black  - Run Black on all Python files"
	@echo "  make conda-export  - Export Poetry dependencies to Conda format"
	@echo "  make update-doc  - Update PDF from tex source file"

.PHONY: help all black conda-export update-pdf
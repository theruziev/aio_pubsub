# Minimal makefile for Sphinx documentation
#

# You can set these variables from the command line.
SPHINXOPTS    =
SPHINXBUILD   = sphinx-build
SOURCEDIR     = docs
BUILDDIR      = $(SOURCEDIR)/_build

# Put it first so that "make" without argument is like "make help".
help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

.PHONY: help Makefile

# Catch-all target: route all unknown targets to Sphinx using the new
# "make mode" option.  $(O) is meant as a shortcut for $(SPHINXOPTS).
%: Makefile
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)


cov-report = true

lint:
	pipenv run flake8 async_pubsub
	pipenv run black -l 100 --check async_pubsub tests

format:
	pipenv run black -l 100 async_pubsub tests

install-dev:
	pipenv install --skip-lock -d

test:
	pipenv run coverage run -m pytest tests
	@if [ $(cov-report) = true ]; then\
    pipenv run coverage combine;\
    pipenv run coverage report;\
	fi

freeze:
	pipenv lock -d


_release:
	scripts/make_release.sh

release: test _release


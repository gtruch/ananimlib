# Minimal makefile for Sphinx documentation
#

# You can set these variables from the command line, and also
# from the environment for the first two.
SPHINXOPTS    ?=
SPHINXBUILD   ?= sphinx-build
SOURCEDIR     = .
BUILDDIR      = _build

PYTHON        = python
PYTHONOPTS	  = -m

FIGURES       = quickstart_ex1 quickstart_ex2 quickstart_ex3 quickstart_ex4 \
                quickstart_ex5 quickstart_ex5_1 quickstart_ex6 quickstart_ex6_1 \
				quickstart_ex7 quickstart_ex8 tutorial_snip1 tutorial_snip2 \
				tutorial_snip3 tutorial_snip4 tutorial_snip5 tutorial_snip6

# Put it first so that "make" without argument is like "make help".
help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

# Catch-all target: route all unknown targets to Sphinx using the new
# "make mode" option.  $(O) is meant as a shortcut for $(SPHINXOPTS).
html: $(addprefix images/,$(addsuffix .gif,$(FIGURES)))
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

images/%.gif : code/%.py
	$(PYTHON) code/build_fig.py $< $@




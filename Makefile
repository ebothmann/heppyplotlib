.PHONY: docs

docs:
	# Initial command for docs directory generation:
	# sphinx-apidoc -o docs -F -H heppyplotlib -A "Enrico Bothmann" -V 0.1.0 heppyplotlib
	sphinx-apidoc -f -o docs heppyplotlib

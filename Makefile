.PHONY: test clean install
vepath = ./venv
binpath = $(vepath)/bin

install:
	python setup.py install
uninstall:
	pip uninstall Straddle
test: 
	test -d $(vepath) || virtualenv $(vepath)
	. $(vepath)/bin/activate
	$(binpath)/pip install pytest
	$(binpath)/pytest
clean:
	rm -rf $(vepath)
	find . -name "*.pyc" | xargs -r rm
	find . -name "__pycache__" | xargs -r rm -rf
	rm -f MANIFEST
	rm -rf *.egg-info/
	rm -rf dist/
	rm -rf build/

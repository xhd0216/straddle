.PHONY: test
vepath = ./venv
binpath = $(vepath)/bin


test:
	test -d $(vepath) || virtualenv $(vepath) 
	. $(vepath)/bin/activate
	$(binpath)/pip install pytest
	$(binpath)/pytest
clean:
	rm -rf $(vepath)
	find . -name "*.pyc" | xargs rm
	find . -name "__pycache__" | xargs rm -rf
	rm -f MANIFEST
	rm -rf *.egg-info/
	rm -rf dist/

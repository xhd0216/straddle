.PHONY: test
vepath = ./ve
binpath = $(vepath)/bin


test:
	test -d $(vepath) || virtualenv $(vepath) 
	. $(vepath)/bin/activate
	$(binpath)/pip install pytest
	$(binpath)/pytest
clean:
	rm -rf $(vepath)
	find . -name "*.pyc" | xargs rm
	rm -rf __pycache__

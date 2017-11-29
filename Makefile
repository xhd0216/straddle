vepath = ./ve
binpath = $(vepath)/bin


test:
	test -d $(vepath) || virtualenv $(vepath) 
	. $(vepath)/bin/activate
	$(binpath)/pip install pytest
	$(binpath)/pytest
clean:
	rm -rf $(vepath)

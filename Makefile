PYTHON_FILES = $(wildcard *.py)

check:
	pep8 *.py

clean:
	rm -f *.pyc *~

tests:
	nosetests

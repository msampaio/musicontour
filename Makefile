PYTHON_FILES = $(wildcard *.py)
DIST_FILES = gui.py contour.py plot.py utils.py COPYING README RELEASE
VERSION = 0.1
DIR = contour-module-$(VERSION)
SERVER = genos.mus.br:www/villa-lobos/download/

check:
	pep8 *.py

clean: clean-dist
	rm -f *.pyc *~

tests:
	nosetests test_*.py

dist: tar zip

zip: join
	zip -r contour-module-$(VERSION).zip $(DIR)

tar: join
	tar czvf contour-module-$(VERSION).tar.gz $(DIR)

join: clean-dist
	@mkdir $(DIR)
	cp $(DIST_FILES) $(DIR)
	ls $(DIR)

clean-dist:
	rm -rf $(DIR)
	rm -rf *.tar.gz
	rm -rf *.zip

push: dist
	rsync -a --progress contour-module-$(VERSION).zip contour-module-$(VERSION).tar.gz $(SERVER)

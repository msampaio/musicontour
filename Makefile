PYTHON_FILES = $(wildcard *.py)
VERSION = 0.2
DIR = contour-module-$(VERSION)
SERVER = genos.mus.br:www/villa-lobos/download/
SRC_DIR = contour
TEST_DIR = tests
GUI_DIR = gui
WEB_DIR = web
MAIN_FILE = MusiContour.py
DIST_FILES = $(MAIN_FILE) $(GUI_DIR) $(SRC_DIR) COPYING README RELEASE

.PHONY: doc tests

check:
	pep8 *.py $(SRC_DIR)/*.py $(TEST_DIR)/*.py $(GUI_DIR)/*.py

clean: clean-dist
	rm -f *.pyc *~
	rm -f $(SRC_DIR)/*~
	rm -f $(SRC_DIR)/*.pyc
	rm -f $(TEST_DIR)/*~
	rm -f $(TEST_DIR)/*.pyc
	rm -f $(GUI_DIR)/*~
	rm -f $(GUI_DIR)/*.pyc
	rm -f $(WEB_DIR)/*~
	rm -f $(WEB_DIR)/*.pyc

tests:
	py.test tests

dist: tar zip

zip: join
	zip -r contour-module-$(VERSION).zip $(DIR)

tar: join
	tar czvf contour-module-$(VERSION).tar.gz $(DIR)

join: clean-dist
	@mkdir $(DIR)
	cp -r $(DIST_FILES) $(DIR)
	ls $(DIR)

clean-dist:
	rm -rf $(DIR)
	rm -rf *.tar.gz
	rm -rf *.zip

push: dist
	rsync -a --progress contour-module-$(VERSION).zip contour-module-$(VERSION).tar.gz $(SERVER)

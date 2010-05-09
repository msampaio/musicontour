PYTHON_FILES = $(wildcard *.py)
VERSION = 0.2
DIR = contour-module-$(VERSION)
SERVER = genos.mus.br:www/villa-lobos/download/
SRC_DIR = contour_module
TEST_DIR = tests
GUI_DIR = gui
DIST_FILES = gui_tk.py $(SRC_DIR) COPYING README RELEASE

check:
	pep8 *.py $(SRC_DIR)/*.py $(TEST_DIR)/*.py

clean: clean-dist
	rm -f *.pyc *~
	rm -f $(SRC_DIR)/*~
	rm -f $(SRC_DIR)/*.pyc
	rm -f $(TEST_DIR)/*~
	rm -f $(TEST_DIR)/*.pyc
	rm -f $(GUI_DIR)/*~
	rm -f $(GUI_DIR)/*.pyc

regression_tests:
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

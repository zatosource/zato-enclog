
.PHONY: test

ENV_NAME=enclog-env
BIN_DIR=$(CURDIR)/$(ENV_NAME)/bin

default: test

# In case of any errors with virtualenv make sure you have virtualenv==12.0 installed (that exact one).

install2:
	virtualenv -p python $(CURDIR)/$(ENV_NAME)
	$(MAKE) _install

install3:
	virtualenv -p python3 $(CURDIR)/$(ENV_NAME)
	$(MAKE) _install

_install:
	$(BIN_DIR)/pip install -r $(CURDIR)/requirements.txt
	$(BIN_DIR)/python $(CURDIR)/setup.py develop
	$(BIN_DIR)/pip install -e $(CURDIR)/.

clean:
	rm -rf $(CURDIR)/$(ENV_NAME)
	rm -rf $(CURDIR)/build
	rm -rf $(CURDIR)/dist
	rm -rf $(CURDIR)/src/zato_enclog.egg-info
	find $(CURDIR) -name '*.pyc' -exec rm {} \;

test:
	$(MAKE) clean
	$(MAKE) install2
	$(MAKE) _test
	$(MAKE) clean
	$(MAKE) install3
	$(MAKE) _test

_test:
	$(BIN_DIR)/nosetests $(CURDIR)/test/zato/enclog/* --with-coverage --cover-tests --cover-erase --cover-package=zato --nocapture
	$(MAKE) flake8

flake8:
	$(BIN_DIR)/flake8 $(CURDIR)/src --count
	$(BIN_DIR)/flake8 $(CURDIR)/test --count

SHELL := /bin/bash

.PHONY: install-deps save-deps clean-pyc clean-build isort lint

define ACTIVATE_VENV
	source .venv/bin/activate
endef

install-deps:
	$(ACTIVATE_VENV) && pip install -r requirements.txt

save-deps:
	$(ACTIVATE_VENV) && pip freeze > requirements.txt

clean-pyc:
	find . -name '*.pyc' -exec rm --force {} +
	find . -name '*.pyo' -exec rm --force {} +
	find . -name '*~' -exec rm --force {} +

clean-build:
	rm --force --recursive build/
	rm --force --recursive dist/
	rm --force --recursive *.egg-info

isort:
	sh -c "isort --skip-glob=.tox --recursive . "

lint:
	flake8 --exclude=.tox
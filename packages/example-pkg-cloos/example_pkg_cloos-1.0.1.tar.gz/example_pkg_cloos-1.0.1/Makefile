.PHONY: help
help: ## show help
	@grep -h '##\ [[:alnum:]]' $(MAKEFILE_LIST) | sed -E 's/(.*):.*##(.*)/\1: \2/' | column -s: -t

.PHONY: venv
venv: ## install/upgrade virtualenv and create venv
	pip install --upgrade virtualenv
	virtualenv venv

.PHONY: install
install: ## install/upgrade packaging tools
	pip install --upgrade setuptools twine wheel

.PHONY: develop
develop: ## install package in 'development mode'
	python setup.py develop

.PHONY: test
test: ## run tests
	tox

.PHONY: clean
clean: ## cleanup
	@echo "Cleaning up distutils stuff"
	rm -rf build
	rm -rf dist
	rm -rf *.egg-info/
	@echo "Cleaning up byte compiled python stuff"
	find . -type f -regex ".*\.py[co]$$" -delete
	find . -type d -name "__pycache__" -delete
	@echo "Cleaning up test stuff"
	rm -rf .pytest_cache
	rm -rf .tox

.PHONY: build
build: clean ## build
	python setup.py sdist bdist_wheel

.PHONY: upload_test
upload_test: build ## upload to https://test.pypi.org
	twine upload --repository-url https://test.pypi.org/legacy/ dist/*

.PHONY: upload
upload: build ## upload to https://pypi.org
	twine upload dist/*

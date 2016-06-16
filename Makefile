
help:
	@echo "usage: make <command>"
	@echo ""
	@echo "Available commands:"
	@echo "  clean - remove all build, test, coverage and Python artifacts"
	@echo "  clean-build - remove build artifacts"
	@echo "  clean-pyc - remove Python file artifacts"
	@echo "  lint - check style with flake8"
	@echo "  dist - package"
	@echo "  install - install the package to the active Python's site-packages"

clean: clean-build clean-pyc

clean-build:
	rm -fr build/
	rm -fr dist/
	rm -fr .eggs/
	find . -name '*.egg-info' -exec rm -fr {} +
	find . -name '*.egg' -exec rm -f {} +

clean-pyc:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

lint:
	flake8 --ignore=E501 dock2nc scripts/dock2nc

dist: clean
	python setup.py sdist
	python setup.py bdist_wheel
	ls -l dist

install: clean
	python setup.py install
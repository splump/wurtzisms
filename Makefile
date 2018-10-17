.PHONY: build

build-requirements:
	pip install setuptools wheel twine

build:
	python3 setup.py sdist bdist_wheel

upload: build
	python3 setup.py upload

.PHONY: build
build:
	python3 setup.py sdist bdist_wheel

upload: build
	twine upload dist/*

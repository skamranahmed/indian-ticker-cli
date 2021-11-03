clean:
	rm -rf build dist ind_ticker.egg-info

install:clean
	pip install -e .

build:clean
	python3 setup.py sdist bdist_wheel

publish-test:build
	stty sane
	twine upload -r testpypi dist/*

publish:build
	stty sane
	twine upload --repository-url https://upload.pypi.org/legacy/ dist/*
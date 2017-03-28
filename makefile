register: *.py
	@# python setup.py register
	@# did not run above, ran below without .pypirc in place, still worked?
	@# twine register dist/sentidict-0.0.1.tar.gz
build: *.py
	pandoc -o README.rst README.markdown
	@# this build the dist for twine (or setuptools) to upload
	@# python setup.py sdist
	@# the bdist_wheel didnt work with distutils, use setuptools in setup.py
	python setup.py sdist bdist_wheel
pypi: dist/*
	@# python setup.py sdist upload
	twine upload dist/*
docs:
	cd docs; make html
tag: *.py
	@# git tag 0.1 -m "release 0.1"
	git push --tags origin master
test:
	nose2

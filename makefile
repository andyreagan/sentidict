pypi: *.py
	pandoc -o README.rst README.markdown
	@# python setup.py register
	@# twine register dist/sentidict-0.0.1.tar.gz
	@# python setup.py sdist
	python setup.py sdist upload
	@# twine upload dist/*

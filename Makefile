testdata:
	cd tests; \
	python generate_fixtures.py

test:
	PYTHONPATH=. pytest

online:
	PYTHONPATH=. pytest --online

dist:
	python setup.py sdist

.PHONY: dist

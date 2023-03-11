testdata:
	cd tests; \
	python generate_fixtures.py

testdata-format:
	cat tests/test_data/bellingcat-raw.json | jq > tests/test_data/bellingcat-raw-cleaned.json
	cat tests/test_data/defmon-raw.json | jq > tests/test_data/defmon-raw-cleaned.json
	cat tests/test_data/geoconfirmed-raw.json | jq > tests/test_data/geoconfirmed-raw-cleaned.json
	cat tests/test_data/texty-raw.json | jq > tests/test_data/texty-raw-cleaned.json

test:
	PYTHONPATH=. pytest

online:
	PYTHONPATH=. pytest --online

dist:
	python setup.py sdist

.PHONY: dist

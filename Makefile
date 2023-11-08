.PHONY: test
test:
	coverage run -m pytest -s
	coverage report -m


.PHONY: format
format:
	blue .

.PHONY: mypy
mypy:
	mypy src/bluemoss

.PHONY: clean
clean:
	rm -rf .nox
	rm -rf .cache
	rm -rf `find . -name __pycache__`
	rm -rf .tests_cache
	rm -rf .mypy_cache
	rm -rf .pytest_cache
	rm -rf htmlcov
	rm -rf *.egg-info
	rm -f .coverage
	rm -f .coverage.*
	rm -rf build
	rm -rf dist
	rm -f coverage.xml

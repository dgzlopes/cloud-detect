.PHONY: test
test:
	pytest

.PHONY: lint
lint:
	pre-commit run --all-files

.PHONY: clean
clean:
	find . -name '*.pyc' -delete
	find . -name '__pycache__' -delete

.PHONY: publish
publish:
	rm -fr build dist
	python3 -m pip install --upgrade build twine
	python3 -m build
	twine upload dist/*
	rm -fr build dist

.PHONY: super-clean
super-clean: clean
	rm -rf build dist .venv venv

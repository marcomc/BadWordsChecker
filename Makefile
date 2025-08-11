# Makefile for MP3BadWordsChecker

.PHONY: venv install test lint run clean

venv:
	python3 -m venv venv

install: venv
	./venv/bin/python3 -m pip install --upgrade pip
	./venv/bin/python3 -m pip install -r requirements.txt

test:
	./venv/bin/python3 -m pytest

lint:
	./venv/bin/python3 -m ruff check .
	./venv/bin/python3 -m mypy .

run:
	./venv/bin/python3 -m badwordschecker.cli

clean:
	rm -rf venv __pycache__ .pytest_cache .mypy_cache
	find . -name "*.pyc" -delete
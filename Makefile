init:
	pip install -r requirements.txt

test: 
	python -m pytest --cov=search_engine

.PHONY: test


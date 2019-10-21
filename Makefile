init:
	pip install -r requirements.txt

test: init
	python -m pytest
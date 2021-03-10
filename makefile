all: test

test:
	python3 -m doctest identify.py
	python3 identify.py

clean:
	rm -rf __pycache__

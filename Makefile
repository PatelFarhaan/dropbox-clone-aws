.PHONY: install run test clean

install:
	pip3 install -r requirements.txt

run:
	python3 app.py

test:
	python3 -m pytest -v

clean:
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name '*.pyc' -delete 2>/dev/null || true
	rm -rf tmp/

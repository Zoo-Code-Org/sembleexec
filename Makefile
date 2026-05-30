.PHONY: install build build-mcp build-onedir test clean

install:
	uv sync

build:
	uv run python build.py

build-mcp:
	uv run python build.py --with-mcp

build-onedir:
	uv run python build.py --onedir

test:
	uv run python test_build.py

clean:
	rm -rf dist/ build/ __pycache__/

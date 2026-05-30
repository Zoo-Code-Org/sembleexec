# semble-executable

Packages [semble](https://github.com/MinishLab/semble) as a standalone executable binary using PyInstaller. No Python installation required to run the resulting binary.

## Prerequisites

- Python 3.10+ (for building only)
- [uv](https://docs.astral.sh/uv/getting-started/installation/) (recommended) or pip

## Quick Start

```bash
# Install dependencies
uv sync

# Build the executable
uv run python build.py

# The binary is at: dist/semble
```

## What Gets Built

The output is a single `semble` binary (or `semble.exe` on Windows) in `dist/` that includes:
- The semble CLI and all its dependencies (model2vec, tree-sitter, bm25s, etc.)
- Tree-sitter language grammars
- The potion-code-16M model (downloaded at first run if not bundled)

## Usage

The executable works exactly like the installed `semble` CLI:

```bash
# Search a local repo
./dist/semble search "authentication flow" ./my-project

# Search a remote repo
./dist/semble search "save model" https://github.com/MinishLab/model2vec

# Find related code
./dist/semble find-related src/auth.py 42 ./my-project

# Run as MCP server (requires --with-mcp build flag)
./dist/semble --content all
```

## Build Options

```bash
# One-file mode (default) - single portable binary
uv run python build.py --onefile

# One-dir mode - faster startup, directory with all files
uv run python build.py --onedir

# Include MCP server support
uv run python build.py --with-mcp

# Specify output name
uv run python build.py --name semble-search
```

## Platform Support

Build on each target platform to get a native binary:
- macOS (Intel & Apple Silicon)
- Linux (x86_64)
- Windows (x86_64)

Cross-compilation is not supported by PyInstaller; build on the target OS.

## CI/CD

See `.github/workflows/build.yml` for automated builds on all platforms.

## License

MIT (same as semble)

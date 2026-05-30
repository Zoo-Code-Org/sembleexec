# semble-executable

Packages [semble](https://github.com/MinishLab/semble) into standalone executables using PyInstaller. No Python installation required to run the resulting binaries.

## Platforms

| Platform | Architecture | Single-file | Fast-start archive |
|----------|-------------|-------------|-------------------|
| Linux | x64 | `semble-linux-x64` | `semble-linux-x64-fast.tar.gz` |
| Linux | ARM64 | `semble-linux-arm64` | `semble-linux-arm64-fast.tar.gz` |
| macOS | Apple Silicon (ARM64) | `semble-macos-arm64` | `semble-macos-arm64-fast.tar.gz` |
| Windows | x64 | `semble-windows-x64.exe` | `semble-windows-x64-fast.zip` |

**Single-file** — one portable binary, no extraction needed. Slower startup (~6s) due to decompression on each run.

**Fast-start** — a compressed archive containing the binary + pre-extracted dependencies. ~20x faster startup, recommended for repeated use or MCP server mode.

## Download

Grab the latest binary from the [Releases](../../releases) page, or download the build artifact from the Actions tab.

## Usage

The executable works exactly like the `semble` CLI:

```bash
# Single-file: make it executable and run (Linux/macOS)
chmod +x semble-macos-arm64
./semble-macos-arm64 search "authentication flow" ./my-project

# Fast-start: extract and run
tar -xzf semble-macos-arm64-fast.tar.gz -C semble/
./semble/semble search "authentication flow" ./my-project

# Search a remote repo
./semble-macos-arm64 search "save model" https://github.com/MinishLab/model2vec

# Find related code
./semble-macos-arm64 find-related src/auth.py 42 ./my-project

# Run as MCP server (fast-start recommended)
./semble/semble
```

## Building Locally

Requires Python 3.10+ and [uv](https://docs.astral.sh/uv/getting-started/installation/).

```bash
# Install dependencies
uv sync --extra mcp

# Build the executable
uv run python build.py --with-mcp

# Binary is at dist/semble (~29 MB)
./dist/semble search "query" .
```

### Build options

```bash
uv run python build.py --onefile        # Single portable binary (default)
uv run python build.py --onedir         # Directory mode (faster startup)
uv run python build.py --name my-semble # Custom binary name
uv run python build.py --with-mcp       # Include MCP server support
```

## CI/CD

The GitHub Actions workflow (`.github/workflows/build.yml`) builds on every push to `main` and on PRs. To create a release with downloadable binaries:

```bash
git tag v0.1.0
git push --tags
```

This triggers the release job which uploads all 6 platform binaries plus SHA-256 checksums.

## How It Works

PyInstaller bundles the CPython interpreter, semble, and all dependencies (model2vec, tree-sitter grammars, numpy, etc.) into a single self-contained binary. The code runs at the same speed as a normal Python install — the benefit is zero-install portability.

## License

MIT (same as semble)

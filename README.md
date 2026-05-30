# semble-executable

Packages [semble](https://github.com/MinishLab/semble) into standalone executables using PyInstaller. No Python installation required to run the resulting binaries.

## Platforms

| Platform | Architecture | Artifact |
|----------|-------------|----------|
| Linux | x64 | `semble-linux-x64` |
| Linux | ARM64 | `semble-linux-arm64` |
| macOS | Intel (x64) | `semble-macos-x64` |
| macOS | Apple Silicon (ARM64) | `semble-macos-arm64` |
| Windows | x64 | `semble-windows-x64.exe` |

## Download

Grab the latest binary from the [Releases](../../releases) page, or download the build artifact from the Actions tab.

## Usage

The executable works exactly like the `semble` CLI:

```bash
# Make it executable (Linux/macOS)
chmod +x semble-macos-arm64

# Search a local repo
./semble-macos-arm64 search "authentication flow" ./my-project

# Search a remote repo
./semble-macos-arm64 search "save model" https://github.com/MinishLab/model2vec

# Find related code
./semble-macos-arm64 find-related src/auth.py 42 ./my-project

# Run as MCP server
./semble-macos-arm64
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

"""Build script to package semble as a standalone executable using PyInstaller."""

import argparse
import importlib.util
import platform
import subprocess
import sys
from pathlib import Path


def find_package_path(package_name: str) -> Path:
    """Find the installed path of a Python package."""
    spec = importlib.util.find_spec(package_name)
    if spec is None or spec.origin is None:
        raise RuntimeError(f"Package '{package_name}' is not installed.")
    return Path(spec.origin).parent


def find_tree_sitter_languages() -> list[str]:
    """Find tree-sitter language .so/.dylib/.dll files to bundle."""
    try:
        ts_lang_pack_path = find_package_path("tree_sitter_language_pack")
    except RuntimeError:
        print("Warning: tree_sitter_language_pack not found, skipping language bundling.")
        return []

    datas = []
    # Include the entire package to capture all grammar .so files
    datas.append(f"--add-data={ts_lang_pack_path}:tree_sitter_language_pack")
    return datas


def find_semble_data() -> list[str]:
    """Find semble package data (agents/*.md files) to bundle."""
    try:
        semble_path = find_package_path("semble")
    except RuntimeError:
        raise RuntimeError("semble is not installed. Run: uv sync")

    datas = []
    agents_dir = semble_path / "agents"
    if agents_dir.exists():
        datas.append(f"--add-data={agents_dir}:semble/agents")
    return datas


def find_model2vec_data() -> list[str]:
    """Find model2vec package data to bundle."""
    try:
        model2vec_path = find_package_path("model2vec")
    except RuntimeError:
        return []

    datas = []
    # Include the package extras metadata
    datas.append(f"--add-data={model2vec_path}:model2vec")
    return datas


def build_executable(
    onefile: bool = True,
    with_mcp: bool = False,
    name: str = "semble",
) -> None:
    """Run PyInstaller to create the semble executable."""
    # Use our own entry_point.py which imports semble.cli
    entry_point = Path(__file__).parent / "entry_point.py"

    if not entry_point.exists():
        raise RuntimeError(f"Cannot find entry_point.py at {entry_point}")

    # Base PyInstaller command
    cmd = [
        sys.executable, "-m", "PyInstaller",
        str(entry_point),
        "--name", name,
        "--noconfirm",
        "--clean",
        "--additional-hooks-dir", str(Path(__file__).parent / "hooks"),
    ]

    # One-file vs one-dir
    if onefile:
        cmd.append("--onefile")
    else:
        cmd.append("--onedir")

    # Hidden imports that PyInstaller might miss
    hidden_imports = [
        "semble",
        "semble.cli",
        "semble.index",
        "semble.cache",
        "semble.stats",
        "semble.types",
        "semble.utils",
        "model2vec",
        "model2vec.utils",
        "vicinity",
        "bm25s",
        "numpy",
        "pathspec",
        "tree_sitter",
        "tree_sitter_language_pack",
        "orjson",
    ]

    if with_mcp:
        hidden_imports.extend([
            "semble.mcp",
            "mcp",
            "watchfiles",
        ])

    for imp in hidden_imports:
        cmd.extend(["--hidden-import", imp])

    # Collect submodules for packages that have dynamic imports
    cmd.extend(["--collect-submodules", "tree_sitter_language_pack"])
    cmd.extend(["--collect-submodules", "semble"])
    cmd.extend(["--collect-submodules", "model2vec"])
    cmd.extend(["--collect-submodules", "vicinity"])
    cmd.extend(["--collect-submodules", "bm25s"])

    # Collect data files
    cmd.extend(["--collect-data", "tree_sitter_language_pack"])
    cmd.extend(["--collect-data", "semble"])
    cmd.extend(["--collect-data", "model2vec"])

    # Add semble agent markdown files
    cmd.extend(find_semble_data())

    # Add model2vec data
    cmd.extend(find_model2vec_data())

    # Add tree-sitter language grammars
    cmd.extend(find_tree_sitter_languages())

    # Platform-specific options
    # Note: universal2 requires a fat Python interpreter; skip if not available
    if platform.system() == "Darwin" and platform.machine() == "x86_64":
        # Only set target-arch if running on Intel; on ARM, let it default
        pass

    print(f"Running: {' '.join(cmd)}")
    subprocess.run(cmd, check=True)

    # Report result
    if onefile:
        suffix = ".exe" if platform.system() == "Windows" else ""
        binary = Path("dist") / f"{name}{suffix}"
    else:
        binary = Path("dist") / name

    if binary.exists():
        size_mb = binary.stat().st_size / (1024 * 1024)
        print(f"\nBuild successful!")
        print(f"  Binary: {binary}")
        print(f"  Size: {size_mb:.1f} MB")
    else:
        print(f"\nBuild completed. Output in dist/")


def main() -> None:
    """Parse arguments and run the build."""
    parser = argparse.ArgumentParser(
        description="Build semble as a standalone executable."
    )
    mode_group = parser.add_mutually_exclusive_group()
    mode_group.add_argument(
        "--onefile",
        action="store_true",
        default=True,
        help="Build a single portable binary (default).",
    )
    mode_group.add_argument(
        "--onedir",
        action="store_true",
        help="Build a directory with all files (faster startup).",
    )
    parser.add_argument(
        "--with-mcp",
        action="store_true",
        help="Include MCP server dependencies in the build.",
    )
    parser.add_argument(
        "--name",
        default="semble",
        help="Output binary name (default: semble).",
    )
    args = parser.parse_args()

    onefile = not args.onedir
    build_executable(onefile=onefile, with_mcp=args.with_mcp, name=args.name)


if __name__ == "__main__":
    main()

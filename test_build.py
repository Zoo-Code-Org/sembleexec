"""Smoke test for the built semble executable."""

import platform
import subprocess
import sys
from pathlib import Path


def main() -> int:
    """Run basic smoke tests against the built binary."""
    suffix = ".exe" if platform.system() == "Windows" else ""
    binary = Path("dist") / f"semble{suffix}"

    if not binary.exists():
        print(f"ERROR: Binary not found at {binary}")
        print("Run 'uv run python build.py' first.")
        return 1

    print(f"Testing binary: {binary}")
    print(f"Size: {binary.stat().st_size / (1024 * 1024):.1f} MB")
    print()

    # Test 1: --help flag
    print("Test 1: semble search --help")
    result = subprocess.run(
        [str(binary), "search", "--help"],
        capture_output=True,
        text=True,
        timeout=30,
    )
    if result.returncode != 0:
        print(f"  FAILED (exit code {result.returncode})")
        print(f"  stderr: {result.stderr}")
        return 1
    if "Search a codebase" not in result.stdout and "query" not in result.stdout:
        print(f"  FAILED (unexpected output)")
        print(f"  stdout: {result.stdout}")
        return 1
    print("  PASSED")

    # Test 2: search against this project directory
    print("Test 2: semble search 'build executable' .")
    result = subprocess.run(
        [str(binary), "search", "build executable", "."],
        capture_output=True,
        text=True,
        timeout=60,
    )
    if result.returncode != 0:
        print(f"  FAILED (exit code {result.returncode})")
        print(f"  stderr: {result.stderr}")
        return 1
    print("  PASSED")
    print(f"  Output preview: {result.stdout[:200]}")

    # Test 3: init --help
    print("Test 3: semble init --help")
    result = subprocess.run(
        [str(binary), "init", "--help"],
        capture_output=True,
        text=True,
        timeout=30,
    )
    if result.returncode != 0:
        print(f"  FAILED (exit code {result.returncode})")
        print(f"  stderr: {result.stderr}")
        return 1
    print("  PASSED")

    print("\nAll smoke tests passed!")
    return 0


if __name__ == "__main__":
    sys.exit(main())

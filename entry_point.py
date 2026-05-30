"""Entry point for the semble executable.

This wrapper ensures the semble CLI is properly invoked when packaged with PyInstaller.
"""

import sys


def main() -> None:
    """Invoke semble's CLI main function."""
    try:
        from semble.cli import main as semble_main
        semble_main()
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()

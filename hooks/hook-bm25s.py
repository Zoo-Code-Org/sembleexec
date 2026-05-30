"""PyInstaller hook for bm25s.

Ensures bm25s submodules are discovered.
"""

from PyInstaller.utils.hooks import collect_submodules

hiddenimports = collect_submodules("bm25s")

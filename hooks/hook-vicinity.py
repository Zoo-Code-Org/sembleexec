"""PyInstaller hook for vicinity.

Ensures vicinity submodules are discovered.
"""

from PyInstaller.utils.hooks import collect_submodules

hiddenimports = collect_submodules("vicinity")

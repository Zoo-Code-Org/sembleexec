"""PyInstaller hook for semble.

Ensures all semble submodules and data files are collected.
"""

from PyInstaller.utils.hooks import collect_data_files, collect_submodules

hiddenimports = collect_submodules("semble")
datas = collect_data_files("semble")

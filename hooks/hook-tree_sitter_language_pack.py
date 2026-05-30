"""PyInstaller hook for tree_sitter_language_pack.

Tree-sitter language pack contains compiled grammar .so/.dylib/.dll files
that are loaded dynamically. We need to collect all of them.
"""

from PyInstaller.utils.hooks import collect_data_files, collect_dynamic_libs, collect_submodules

hiddenimports = collect_submodules("tree_sitter_language_pack")
datas = collect_data_files("tree_sitter_language_pack")
binaries = collect_dynamic_libs("tree_sitter_language_pack")

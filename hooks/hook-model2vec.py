"""PyInstaller hook for model2vec.

Ensures model2vec metadata and data files are bundled.
"""

from PyInstaller.utils.hooks import collect_data_files, collect_submodules

hiddenimports = collect_submodules("model2vec")
datas = collect_data_files("model2vec")

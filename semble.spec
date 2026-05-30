# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_data_files
from PyInstaller.utils.hooks import collect_submodules

datas = [('/Users/navedmerchant/code/sembleexec/.venv/lib/python3.13/site-packages/semble/agents', 'semble/agents'), ('/Users/navedmerchant/code/sembleexec/.venv/lib/python3.13/site-packages/model2vec', 'model2vec'), ('/Users/navedmerchant/code/sembleexec/.venv/lib/python3.13/site-packages/tree_sitter_language_pack', 'tree_sitter_language_pack')]
hiddenimports = ['semble', 'semble.cli', 'semble.index', 'semble.cache', 'semble.stats', 'semble.types', 'semble.utils', 'model2vec', 'model2vec.utils', 'vicinity', 'bm25s', 'numpy', 'pathspec', 'tree_sitter', 'tree_sitter_language_pack', 'orjson']
datas += collect_data_files('tree_sitter_language_pack')
datas += collect_data_files('semble')
datas += collect_data_files('model2vec')
hiddenimports += collect_submodules('tree_sitter_language_pack')
hiddenimports += collect_submodules('semble')
hiddenimports += collect_submodules('model2vec')
hiddenimports += collect_submodules('vicinity')
hiddenimports += collect_submodules('bm25s')


a = Analysis(
    ['/Users/navedmerchant/code/sembleexec/entry_point.py'],
    pathex=[],
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=['/Users/navedmerchant/code/sembleexec/hooks'],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='semble',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

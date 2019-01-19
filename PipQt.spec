# -*- mode: python -*-
import os

block_cipher = None


a = Analysis(
    ["PipQt.py"],
    pathex=[os.getcwd()],
    binaries=[],
    datas=[],
    hiddenimports=[],
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)
exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name="PipQt",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    icon="icons\\main_icon.ico",
)
coll = COLLECT(
    exe, a.binaries, a.zipfiles, a.datas, strip=False, upx=True, name="PipQt"
)

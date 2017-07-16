# -*- mode: python -*-
import os
from distutils.sysconfig import get_python_lib
block_cipher = None


a = Analysis(['PipQt.py'],
             pathex=[os.getcwd(),
                     os.path.join(get_python_lib(), 'PyQt5\\Qt\\bin')],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
          cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          exclude_binaries=True,
          name='PipQt',
          debug=False,
          strip=False,
          upx=True,
          console=True, icon='icons\\main_icon.ico')
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name='PipQt')

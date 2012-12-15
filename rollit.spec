# -*- mode: python -*-
from kivy.tools.packaging.pyinstaller_hooks import install_hooks
install_hooks(globals())
import os
a = Analysis(['main.py'],
             pathex=['Z:\\home\\ndogg\\Projects\\diceroller'],
             hiddenimports=['simpleparse'],
             )
pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts,
          exclude_binaries=1,
          name=os.path.join('build\\pyi.win32\\rollit', 'rollit.exe'),
          debug=False,
          strip=None,
          upx=True,
          console=False , icon='icon.ico')
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=None,
               upx=True,
               name=os.path.join('dist', 'rollit')
               )

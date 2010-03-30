# -*- mode: python -*-
a = Analysis([os.path.join(HOMEPATH,'support\\_mountzlib.py'), os.path.join(HOMEPATH,'support\\useUnicode.py'), 'z:/home/pankaj/programming/python/billiards/src/billiards/billiards.py'],
             pathex=['Z:\\mnt\\data\\Program Installers\\Programs\\Programming\\py\\py26win'])
pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts,
          exclude_binaries=1,
          name=os.path.join('build\\pyi.win32\\billiards_pyinstaller', 'billiards.exe'),
          debug=False,
          strip=False,
          upx=True,
          console=False )
data = Tree(root='z:\\home\\pankaj\\programming\\python\\billiards\\src\\billiards\\data', prefix='data', excludes=None)
coll = COLLECT( exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               data,
               strip=False,
               upx=True,
               name=os.path.join('dist', 'billiards'))

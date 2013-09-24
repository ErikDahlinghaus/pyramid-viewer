# -*- mode: python -*-
a = Analysis(['main.pyw'],
             pathex=['C:\\Users\\ericd\\workspace\\CoristaPyramidManipulator\\src'],
             hiddenimports=[],
             hookspath=None)
a.datas += [('icon.png','C:\\Users\\ericd\\workspace\\CoristaPyramidManipulator\\src\\icon.png','DATA')]
pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name=os.path.join('dist', 'main.exe'),
          debug=False,
          strip=None,
          upx=True,
          console=False , icon='favicon.ico')
app = BUNDLE(exe,
             name=os.path.join('dist', 'main.exe.app'))

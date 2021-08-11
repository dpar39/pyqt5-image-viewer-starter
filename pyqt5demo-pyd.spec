# -*- mode: python ; coding: utf-8 -*-


block_cipher = None

def get_ext_paths(root_dir, exclude_files, exts = ['.pyd', '.so']):
    """get filepaths for compilation"""
    paths = []
    for root, dirs, files in os.walk(root_dir):
        for filename in files:
            ext = os.path.splitext(filename)[1]
            if not ext in exts:
                continue
            if filename in exclude_files:
                continue
            file_path = os.path.join(root, filename)
            paths.append((file_path, root_dir))
    for p in paths:
        print (p)
    return paths
 


a = Analysis(['main.py'],
             pathex=['.'],
             binaries=get_ext_paths('gui', []),
             datas=[],
             hiddenimports=['PyQt5', 'PyQt5.QtCore', 'PyQt5.QtGui', 'PyQt5.QtWidgets', 'json', 'numpy'],
             hookspath=[],
             hooksconfig={},
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)

exe = EXE(pyz,
          a.scripts, 
          [],
          exclude_binaries=True,
          name='pyqt5demo',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=False,
          disable_windowed_traceback=False,
          target_arch=None,
          codesign_identity=None,
          entitlements_file=None , icon='resources\\lena.ico')
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas, 
               strip=False,
               upx=True,
               upx_exclude=[],
               name='pyqt5demo')

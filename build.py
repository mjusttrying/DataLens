import os
import sys
import PyInstaller.__main__
from PyInstaller.utils.hooks import collect_all

def build():
    # Collect all PyQt6 dependencies
    binaries = []
    datas = []
    hiddenimports = []
    
    packages = ['PyQt6', 'PyQt6.QtCore', 'PyQt6.QtGui', 'PyQt6.QtWidgets']
    for package in packages:
        deps = collect_all(package)
        binaries.extend(deps[0])
        datas.extend(deps[1])
        hiddenimports.extend(deps[2])

    # Add the data to the spec file
    spec_content = f'''# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['run.py'],
    pathex=[],
    binaries={binaries},
    datas={datas},
    hiddenimports=hiddenimports + ['gpt4all', 'PyQt6', 'PyQt6.QtCore', 'PyQt6.QtGui', 'PyQt6.QtWidgets'],
    hookspath=[],
    hooksconfig={{}},
    runtime_hooks=[],
    excludes=['_tkinter', 'tkinter', 'tcl'],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='DataLens',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='resources/icon.icns'
)

app = BUNDLE(
    exe,
    name='DataLens.app',
    icon='app_icon.icns',
    bundle_identifier='com.datalens.app',
    info_plist={{
        'LSMinimumSystemVersion': '10.12.0',
        'NSHighResolutionCapable': 'True'
    }}
)
'''

    with open('DataLens.spec', 'w') as f:
        f.write(spec_content)

    # Run PyInstaller
    PyInstaller.__main__.run([
        'DataLens.spec',
        '--clean',
        '--noconfirm'
    ])

if __name__ == '__main__':
    build()

# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['main.py'],
    pathex=['.'],
    binaries=[],
    datas=[
        ('openai.key', '.'),
        ('resources/assets/*', 'resources/assets'),  # images etc.
        ('resources/styles/*', 'resources/styles'),
        ('resources/**/*', 'resources'),
    ],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='Skills Wizard',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,  # 👈 important pour éviter le terminal
    icon='resources/assets/mon_icon.icns'
)



coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='Skills Wizard'
)

app = BUNDLE(
    exe,
    name='Skills Wizard.app',
    icon='resources/assets/mon_icon.icns',
    bundle_identifier='com.skillswizard.app'
)

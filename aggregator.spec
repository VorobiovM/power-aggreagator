# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['src/power_aggregator/__main__.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('src/power_aggregator/data/baselines/*.json', 'data/baselines'),
        ('src/power_aggregator/data/aggregators/*.json', 'data/aggregators'),
        ('src/power_aggregator/pictures/*.png', 'pictures'),
        ('favicon.png', 'favicon.png')
    ],
    hiddenimports=[],
    hookspath=[],
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
    name='aggregator',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon="favicon.ico",
)

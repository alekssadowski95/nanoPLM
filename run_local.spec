# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['run_local.py'],
    pathex=[],
    binaries=[],
    datas=[('nanoplm/templates/*', 'nanoplm/templates'), ('nanoplm/static/*', 'nanoplm/static'), ('nanoplm/static/bootstrap-5.3.3-dist/css/*', 'nanoplm/static/bootstrap-5.3.3-dist/css'), ('nanoplm/static/bootstrap-5.3.3-dist/js/*', 'nanoplm/static/bootstrap-5.3.3-dist/js'), ('nanoplm/static/bootstrap-icons-1.11.3/*', 'nanoplm/static/bootstrap-icons-1.11.3'), ('nanoplm/static/bootstrap-icons-1.11.3/font/*', 'nanoplm/static/bootstrap-icons-1.11.3/font'), ('nanoplm/static/bootstrap-icons-1.11.3/font/fonts/*', 'nanoplm/static/bootstrap-icons-1.11.3/font/fonts'), ('nanoplm/site.db', 'nanoplm'), ('LICENSE', '.')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)
splash = Splash(
    'nanoplm/static/nanoplm-splash.jpg',
    binaries=a.binaries,
    datas=a.datas,
    text_pos=None,
    text_size=12,
    minify_script=True,
    always_on_top=True,
)

exe = EXE(
    pyz,
    a.scripts,
    splash,
    [],
    exclude_binaries=True,
    name='run_local',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['nanoplm\\static\\nanoplm-logo.ico'],
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    splash.binaries,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='run_local',
)

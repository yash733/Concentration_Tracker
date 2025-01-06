# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['simple_tracker.py'],
    pathex=[],
    binaries=[],
    datas=[('Face_Detect_timer\\haarcascade_frontalface_alt.xml', 'Face_Detect_timer'), ('Face_Detect_timer\\requirements.txt', 'Face_Detect_timer')],
    hiddenimports=['cv2', 'keyboard'],
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
    name='FaceTimer',
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
)

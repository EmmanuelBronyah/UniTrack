# -*- mode: python ; coding: utf-8 -*-

import os

# ----------------------
# Paths
# ----------------------
PROJECT_ROOT = os.getcwd()
SRC_DIR = os.path.join(PROJECT_ROOT, "src")

MAIN_SCRIPT = os.path.join(SRC_DIR, "main.py")
ICON_FILE = os.path.join(PROJECT_ROOT, "assets", "icons", "icon.ico")
RESOURCES_FILE = os.path.join(PROJECT_ROOT, "resources.py")

# Datas: prefilled database and any other static files
DATA_FILES = [
    (SRC_DIR, "src"), (os.path.join(SRC_DIR, "data", "unitrack.db"), "data"), (RESOURCES_FILE, "src")
]


a = Analysis(
    [MAIN_SCRIPT],
    pathex=[SRC_DIR],
    binaries=[],
    datas=DATA_FILES,
    hiddenimports=[
        "sqlalchemy",
        "sqlalchemy.orm",
        "sqlalchemy.ext.declarative",
        "sqlalchemy.exc",
        "dotenv",
        "platformdirs",
        "shutil",
        "pathlib",
        "passlib",
        "passlib.context",
        "passlib.handlers.bcrypt",
        "resources",
        "pandas",
    ],
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
    [],
    exclude_binaries=True,
    name='UniTrack',
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
    icon=ICON_FILE,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='UniTrack',
)

# -*- mode: python ; coding: utf-8 -*-
"""
PyInstaller配置文件 - Windows平台
用于打包PicX GUI为独立可执行文件，包含内嵌的libvips
"""

import os
import sys
from pathlib import Path

# 获取项目根目录
root_dir = Path(__file__).parent

# libvips路径
libvips_bin = root_dir / "libs" / "libvips" / "bin"

# 收集libvips DLL文件
libvips_binaries = []
if libvips_bin.exists():
    for dll in libvips_bin.glob("*.dll"):
        libvips_binaries.append((str(dll), 'libs/libvips/bin'))
    print(f"找到 {len(libvips_binaries)} 个libvips DLL文件")
else:
    print("警告: libvips目录不存在，将不包含libvips支持")
    print(f"请运行 setup_libvips.py 下载libvips")

# 收集额外数据文件
datas = [
    ('config', 'config'),
]

# 如果assets目录存在，添加它
if (root_dir / 'assets').exists():
    datas.append(('assets', 'assets'))

# 如果有libvips，添加到数据文件
if libvips_bin.exists():
    datas.append(('libs/libvips/bin', 'libs/libvips/bin'))

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=libvips_binaries,
    datas=datas,
    hiddenimports=[
        'pyvips',
        'PIL._tkinter_finder',
        'PIL.Image',
        'PIL.ImageTk',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='PicX-GUI',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,  # 不显示控制台窗口（设为True可查看调试信息）
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='assets/icons/app.ico' if (root_dir / 'assets' / 'icons' / 'app.ico').exists() else None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='PicX-GUI',
)

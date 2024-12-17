# -*- mode: python ; coding: utf-8 -*-

import os
import sys
from selenium.webdriver.chrome.service import Service
import tkinter

# 获取当前目录和 tcl/tk DLL 路径
current_dir = os.path.dirname(os.path.abspath(SPECPATH))
tcl_tk_dir = os.path.join(os.path.dirname(os.path.dirname(tkinter.__file__)), 'DLLs')

# 获取 ChromeDriver 路径
chrome_driver_path = os.path.join(current_dir, 'chrome', 'chromedriver.exe')

# 准备二进制文件列表
binaries = []
if os.path.exists(chrome_driver_path):
    binaries.append((chrome_driver_path, 'chrome/chromedriver.exe'))

# 添加 tcl/tk DLL
for dll in ['tcl86t.dll', 'tk86t.dll', '_tkinter.pyd']:
    dll_path = os.path.join(tcl_tk_dir, dll)
    if os.path.exists(dll_path):
        binaries.append((dll_path, '.'))

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=binaries,
    datas=[],
    hiddenimports=['PIL._tkinter_finder', 'tkinter', 'tkinter.ttk'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        # 科学计算和数据分析相关
        'matplotlib', 'numpy', 'pandas', 'scipy', 'sympy',
        # Jupyter 相关
        'IPython', 'jupyter', 'notebook', 'ipykernel',
        # 其他大型库
        'cv2', 'sklearn', 'tensorflow', 'torch', 'theano',
        # 测试相关
        'pytest', 'unittest', 'nose',
        # 文档相关
        'sphinx', 'docutils',
        # 数据库相关
        'sqlalchemy', 'mysql', 'postgresql', 'sqlite3',
        # Web 框架
        'django', 'flask', 'fastapi',
        # 其他不需要的模块
        'asyncio', 'multiprocessing', 'concurrent', 'distutils',
        'lib2to3', 'pydoc_data', 'test', 'tests', 'site-packages'
    ],
    noarchive=False,
    optimize=2  # 使用最高级别的优化
)

# 清理不需要的二进制文件
a.binaries = [b for b in a.binaries if not any(x in b[0].lower() for x in [
    'libopenblas',  # 数学计算库
    'mkl_',         # Intel MKL
    'svml_',        # Short Vector Math Library
    'libiomp',      # Intel OpenMP
    'libffi',       # Foreign Function Interface
])]

# 添加 tcl/tk 运行时文件
tcl_tk_path = os.path.join(os.path.dirname(os.path.dirname(tkinter.__file__)), 'tcl')
if os.path.exists(tcl_tk_path):
    a.datas += Tree(tcl_tk_path, prefix='tcl', excludes=['*.lib', '*.a', '*.pdb', '*.def'])

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='windsurf-vip-free',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,  # 禁用 strip
    upx=True,    # 保持 UPX 压缩
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

# 在Windows上内嵌libvips到PicX GUI

## 方案概述

在Windows上将libvips内嵌到打包的应用程序中有两种主要方案：

### 方案一：捆绑预编译的libvips Windows二进制文件（推荐）

这是最简单且最可靠的方案，适合大多数用户。

### 方案二：使用conda-pack打包完整Python环境

适合需要完整控制环境的场景。

---

## 方案一：捆绑libvips Windows二进制文件（推荐）

### 步骤1：下载libvips Windows预编译包

从libvips官方下载页面获取Windows预编译包：
https://github.com/libvips/libvips/releases

有两个版本可选：
- **`vips-dev-w64-web-x.y.z.zip`** - 轻量版（~10MB），仅包含安全的基本格式支持
- **`vips-dev-w64-all-x.y.z.zip`** - 完整版（~50MB），支持所有格式

**推荐使用`vips-dev-w64-all-x.y.z.zip`**，因为PicX需要处理TIFF等格式。

### 步骤2：项目结构调整

```
picx-gui/
├── main.py
├── requirements.txt
├── gui/
│   └── ...
├── libs/                          # 新增：存放libvips
│   └── libvips/
│       ├── bin/                   # libvips DLL文件
│       │   ├── libvips-42.dll
│       │   ├── libglib-2.0-0.dll
│       │   └── ... (其他依赖DLL)
│       └── lib/                   # lib文件（可选）
├── assets/
└── config/
```

### 步骤3：创建libvips加载脚本

创建 `gui/utils/libvips_loader.py`：

```python
"""libvips Windows加载器，用于在打包后自动加载内嵌的libvips。"""
import os
import sys
import platform


def setup_libvips_path():
    """
    设置libvips DLL搜索路径。
    
    在Windows上，需要将libvips的bin目录添加到DLL搜索路径中。
    """
    if platform.system() != "Windows":
        return
    
    # 获取应用程序根目录
    if getattr(sys, 'frozen', False):
        # PyInstaller打包后的路径
        application_path = sys._MEIPASS
    else:
        # 开发环境路径
        application_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    
    # libvips bin目录路径
    libvips_bin = os.path.join(application_path, "libs", "libvips", "bin")
    
    if os.path.exists(libvips_bin):
        # 将libvips bin目录添加到PATH
        os.environ["PATH"] = libvips_bin + os.pathsep + os.environ.get("PATH", "")
        
        # Python 3.8+ 需要显式添加DLL目录
        if hasattr(os, 'add_dll_directory'):
            os.add_dll_directory(libvips_bin)
        
        print(f"libvips已加载: {libvips_bin}")
        return True
    else:
        print(f"警告: libvips目录不存在: {libvips_bin}")
        return False


def check_pyvips():
    """检查pyvips是否可用。"""
    try:
        import pyvips
        print(f"pyvips版本: {pyvips.__version__}")
        return True
    except ImportError:
        print("警告: pyvips未安装")
        return False
    except Exception as e:
        print(f"警告: pyvips加载失败: {e}")
        return False
```

### 步骤4：修改main.py

在应用启动时加载libvips：

```python
"""PicX GUI - 应用入口点"""
import sys

# 首先加载libvips（Windows）
from gui.utils.libvips_loader import setup_libvips_path, check_pyvips
setup_libvips_path()

# 然后导入其他模块
import customtkinter as ctk
from gui.app import PicXApp


def main():
    """主入口函数"""
    # 检查pyvips是否可用
    pyvips_available = check_pyvips()
    
    try:
        app = PicXApp(pyvips_available=pyvips_available)
        app.mainloop()
    except KeyboardInterrupt:
        print("\n应用被用户中断")
        sys.exit(0)
    except Exception as e:
        print(f"致命错误: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
```

### 步骤5：PyInstaller打包配置

创建 `build_windows.spec`：

```python
# -*- mode: python ; coding: utf-8 -*-

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

# 收集额外数据文件
datas = [
    ('config', 'config'),
    ('assets', 'assets'),
]

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
    console=False,  # 不显示控制台窗口
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
```

### 步骤6：创建构建脚本

创建 `build_windows.bat`：

```batch
@echo off
echo ========================================
echo PicX GUI Windows 打包脚本
echo ========================================

REM 检查libvips是否存在
if not exist "libs\libvips\bin" (
    echo 错误: 未找到libvips！
    echo 请先下载libvips Windows预编译包并解压到 libs\libvips\
    echo 下载地址: https://github.com/libvips/libvips/releases
    pause
    exit /b 1
)

echo 正在清理旧的构建文件...
if exist "build" rmdir /s /q build
if exist "dist" rmdir /s /q dist

echo 正在使用PyInstaller打包...
pyinstaller build_windows.spec

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ========================================
    echo 打包完成！
    echo 可执行文件位于: dist\PicX-GUI\
    echo ========================================
    pause
) else (
    echo.
    echo ========================================
    echo 打包失败！请检查错误信息。
    echo ========================================
    pause
    exit /b 1
)
```

### 步骤7：创建自动下载libvips的脚本（可选）

创建 `setup_libvips.py`：

```python
"""自动下载并配置libvips Windows预编译包"""
import os
import sys
import urllib.request
import zipfile
from pathlib import Path

LIBVIPS_VERSION = "8.15.5"  # 修改为最新版本
LIBVIPS_URL = f"https://github.com/libvips/libvips/releases/download/v{LIBVIPS_VERSION}/vips-dev-w64-all-{LIBVIPS_VERSION}.zip"
LIBVIPS_DIR = Path("libs/libvips")


def download_libvips():
    """下载libvips Windows预编译包"""
    print(f"正在下载libvips {LIBVIPS_VERSION}...")
    print(f"URL: {LIBVIPS_URL}")
    
    # 创建临时目录
    temp_dir = Path("temp")
    temp_dir.mkdir(exist_ok=True)
    
    zip_file = temp_dir / f"libvips-{LIBVIPS_VERSION}.zip"
    
    # 下载文件
    try:
        urllib.request.urlretrieve(LIBVIPS_URL, zip_file)
        print(f"下载完成: {zip_file}")
    except Exception as e:
        print(f"下载失败: {e}")
        return False
    
    # 解压文件
    print("正在解压...")
    try:
        with zipfile.ZipFile(zip_file, 'r') as zip_ref:
            # 解压到临时目录
            extract_dir = temp_dir / f"vips-dev-{LIBVIPS_VERSION}"
            zip_ref.extractall(extract_dir)
        
        # 移动到目标目录
        vips_root = extract_dir / f"vips-dev-{LIBVIPS_VERSION}"
        
        # 创建目标目录
        LIBVIPS_DIR.mkdir(parents=True, exist_ok=True)
        
        # 复制bin目录
        import shutil
        if (vips_root / "bin").exists():
            if (LIBVIPS_DIR / "bin").exists():
                shutil.rmtree(LIBVIPS_DIR / "bin")
            shutil.copytree(vips_root / "bin", LIBVIPS_DIR / "bin")
            print(f"已复制bin目录到: {LIBVIPS_DIR / 'bin'}")
        
        # 复制lib目录（可选）
        if (vips_root / "lib").exists():
            if (LIBVIPS_DIR / "lib").exists():
                shutil.rmtree(LIBVIPS_DIR / "lib")
            shutil.copytree(vips_root / "lib", LIBVIPS_DIR / "lib")
            print(f"已复制lib目录到: {LIBVIPS_DIR / 'lib'}")
        
        print("libvips安装完成！")
        
        # 清理临时文件
        shutil.rmtree(temp_dir)
        
        return True
        
    except Exception as e:
        print(f"解压失败: {e}")
        return False


def check_libvips():
    """检查libvips是否已安装"""
    if (LIBVIPS_DIR / "bin").exists():
        dll_count = len(list((LIBVIPS_DIR / "bin").glob("*.dll")))
        print(f"libvips已安装，找到 {dll_count} 个DLL文件")
        return True
    return False


def main():
    """主函数"""
    print("=" * 50)
    print("PicX GUI - libvips Windows 配置工具")
    print("=" * 50)
    
    if check_libvips():
        response = input("libvips已存在，是否重新下载？(y/N): ")
        if response.lower() != 'y':
            print("已取消")
            return
    
    success = download_libvips()
    
    if success:
        print("\n配置完成！现在可以运行 build_windows.bat 进行打包。")
    else:
        print("\n配置失败！请手动下载libvips并解压到 libs/libvips/")
        print(f"下载地址: {LIBVIPS_URL}")


if __name__ == "__main__":
    main()
```

---

## 使用流程

### 开发环境设置

1. **下载libvips**（自动）：
   ```bash
   python setup_libvips.py
   ```

   或**手动下载**：
   - 访问 https://github.com/libvips/libvips/releases
   - 下载 `vips-dev-w64-all-x.y.z.zip`
   - 解压后将 `bin` 目录复制到 `libs/libvips/bin`

2. **安装Python依赖**：
   ```bash
   pip install -r requirements.txt
   ```

3. **运行应用**：
   ```bash
   python main.py
   ```

### 打包发布

1. **确保libvips已配置**：
   ```bash
   dir libs\libvips\bin
   ```
   应该看到大量的 `.dll` 文件

2. **运行打包脚本**：
   ```bash
   build_windows.bat
   ```

3. **测试打包后的应用**：
   ```bash
   cd dist\PicX-GUI
   PicX-GUI.exe
   ```

4. **分发**：
   整个 `dist\PicX-GUI` 文件夹可以直接压缩分发，用户无需安装任何依赖。

---

## 方案优势

✅ **完全独立** - 用户无需安装Python、libvips或任何依赖  
✅ **体积适中** - 完整打包约60-80MB（包含libvips全部格式支持）  
✅ **兼容性好** - 支持Windows 7及以上所有版本  
✅ **性能优秀** - libvips原生性能，无虚拟化开销  
✅ **易于维护** - 可以轻松更新libvips版本  

---

## 注意事项

1. **libvips版本选择**
   - 建议使用最新稳定版（当前8.15.x）
   - 使用 `all` 版本以支持TIFF等格式

2. **DLL依赖**
   - libvips依赖多个DLL（glib、expat等）
   - 必须将整个bin目录一起打包

3. **Python版本**
   - Python 3.8+ 需要使用 `os.add_dll_directory()`
   - Python 3.7 及以下使用 `os.environ["PATH"]` 即可

4. **打包大小优化**
   - 如果不需要所有格式支持，可以使用 `web` 版本（更小）
   - 可以使用UPX压缩（PyInstaller默认启用）

5. **代码签名**（可选）
   - Windows可能会警告未签名的应用
   - 建议购买代码签名证书并签名

---

## 故障排查

### 问题1：找不到libvips DLL
**解决方案**：
- 确认 `libs/libvips/bin` 目录存在
- 检查 `libvips_loader.py` 中的路径配置
- 运行时查看控制台输出的加载信息

### 问题2：pyvips导入失败
**解决方案**：
- 确认 `pyvips` 已在 `requirements.txt` 中
- 检查libvips版本与pyvips版本兼容性
- 使用 `python -c "import pyvips; print(pyvips.__version__)"` 测试

### 问题3：打包后无法启动
**解决方案**：
- 使用 `console=True` 重新打包查看错误信息
- 检查 `hiddenimports` 是否包含所有必要模块
- 确认所有DLL文件都在打包目录中

---

## 替代方案

### 方案二：使用conda-pack

如果你使用conda环境，可以使用 `conda-pack` 打包整个环境：

```bash
# 安装conda-pack
conda install -c conda-forge conda-pack

# 打包环境
conda pack -n your_env_name -o picx-gui-env.tar.gz
```

但这种方案生成的包会更大（200-500MB），不推荐。

---

## 下一步

完成libvips集成后，你的PicX GUI将：
1. ✅ 支持所有图片格式（包括TIFF、HEIC等）
2. ✅ 快速处理大图（内存效率高）
3. ✅ 无需用户手动安装依赖
4. ✅ 一键安装运行

需要我创建这些配置文件和脚本吗？

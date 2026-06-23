"""Build script for PicX GUI - Flet version."""
import os
import sys
import shutil
import subprocess
from pathlib import Path


def clean_build():
    """Clean build directories."""
    print("Cleaning build directories...")
    
    dirs_to_clean = ["build", "dist", "*.egg-info"]
    for pattern in dirs_to_clean:
        for path in Path(".").glob(pattern):
            if path.is_dir():
                shutil.rmtree(path)
                print(f"  Removed: {path}")
                

def install_dependencies():
    """Install required dependencies."""
    print("Installing dependencies...")
    
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], check=True)
        print("  Dependencies installed successfully")
    except subprocess.CalledProcessError as e:
        print(f"  Error installing dependencies: {e}")
        return False
        
    return True


def run_tests():
    """Run unit tests."""
    print("Running tests...")
    
    try:
        result = subprocess.run([sys.executable, "-m", "pytest", "tests/", "-v"], check=True)
        print("  Tests passed")
        return True
    except subprocess.CalledProcessError as e:
        print(f"  Tests failed: {e}")
        return False


def build_desktop():
    """Build desktop application."""
    print("Building desktop application...")
    
    try:
        # 使用flet打包
        subprocess.run([
            sys.executable, "-m", "flet", "pack",
            "main.py",
            "--name", "PicX-GUI",
            "--icon", "assets/icon.ico",
            "--add-data", "assets;assets",
        ], check=True)
        print("  Desktop application built successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"  Error building desktop application: {e}")
        return False


def build_web():
    """Build web application."""
    print("Building web application...")
    
    try:
        # 使用flet打包为web应用
        subprocess.run([
            sys.executable, "-m", "flet", "pack",
            "main.py",
            "--name", "PicX-GUI-Web",
            "--web",
        ], check=True)
        print("  Web application built successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"  Error building web application: {e}")
        return False


def create_installer():
    """Create installer script."""
    print("Creating installer script...")
    
    installer_content = """@echo off
echo PicX GUI Installer
echo ==================
echo.

REM Check Python installation
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    echo Please install Python 3.8 or later
    pause
    exit /b 1
)

REM Install dependencies
echo Installing dependencies...
pip install -r requirements.txt

REM Create desktop shortcut
echo Creating desktop shortcut...
set SCRIPT_DIR=%~dp0
set SHORTCUT_PATH=%USERPROFILE%\\Desktop\\PicX GUI.lnk

REM Create VBS script to create shortcut
echo Set oWS = WScript.CreateObject("WScript.Shell") > CreateShortcut.vbs
echo sLinkFile = "%SHORTCUT_PATH%" >> CreateShortcut.vbs
echo Set oLink = oWS.CreateShortcut(sLinkFile) >> CreateShortcut.vbs
echo oLink.TargetPath = "%SCRIPT_DIR%main.py" >> CreateShortcut.vbs
echo oLink.WorkingDirectory = "%SCRIPT_DIR%" >> CreateShortcut.vbs
echo oLink.Save >> CreateShortcut.vbs

cscript CreateShortcut.vbs
del CreateShortcut.vbs

echo.
echo Installation completed!
echo You can now run PicX GUI from the desktop shortcut or by running:
echo   python main.py
echo.
pause
"""
    
    with open("install.bat", "w", encoding="utf-8") as f:
        f.write(installer_content)
        
    print("  Installer script created: install.bat")


def create_readme():
    """Create README file."""
    print("Creating README file...")
    
    readme_content = """# PicX GUI - Flet版本

PicX图片优化工具的现代化GUI界面，基于Flet框架构建。

## 功能特性

- **单图压缩** - 完整控制单张图片优化
- **批量处理** - 并行处理整个文件夹
- **大图切片** - 为超大图片生成切片
- **环境诊断** - 检查系统配置
- **预设管理** - 使用内置或自定义预设

## 安装

### 方式1：直接运行

1. 克隆仓库
   ```bash
   git clone https://github.com/username/picx-gui-flet.git
   cd picx-gui-flet
   ```

2. 安装依赖
   ```bash
   pip install -r requirements.txt
   ```

3. 运行应用
   ```bash
   python main.py
   ```

### 方式2：使用安装脚本（Windows）

1. 双击运行 `install.bat`
2. 按照提示完成安装
3. 从桌面快捷方式启动应用

## 开发

### 运行测试

```bash
python -m pytest tests/ -v
```

### 构建可执行文件

```bash
python build.py
```

## 项目结构

```
flet_version/
├── main.py                    # 主入口点
├── build.py                   # 构建脚本
├── requirements.txt           # 依赖配置
├── gui/
│   ├── app.py                 # 主应用类
│   ├── tabs/                  # 功能标签页
│   ├── widgets/               # 自定义组件
│   ├── styles/                # 主题配置
│   ├── locales/               # 国际化
│   └── utils/                 # 工具类
├── tests/                     # 单元测试
└── assets/                    # 资源文件
```

## 快捷键

- `Ctrl+O` - 打开文件
- `Ctrl+Shift+O` - 打开目录
- `Ctrl+S` - 保存
- `Ctrl+1-5` - 切换标签页
- `Ctrl+T` - 切换主题
- `Ctrl+L` - 切换语言
- `F1` - 帮助
- `F5` - 刷新

## 许可证

MIT License
"""
    
    with open("README.md", "w", encoding="utf-8") as f:
        f.write(readme_content)
        
    print("  README file created: README.md")


def main():
    """Main build function."""
    print("PicX GUI - Build Script")
    print("=" * 50)
    
    # 清理构建目录
    clean_build()
    
    # 安装依赖
    if not install_dependencies():
        print("Failed to install dependencies")
        return
        
    # 运行测试
    if not run_tests():
        print("Tests failed")
        return
        
    # 创建安装脚本
    create_installer()
    
    # 创建README
    create_readme()
    
    # 构建桌面应用
    build_desktop()
    
    # 构建web应用
    build_web()
    
    print("=" * 50)
    print("Build completed successfully!")
    print("\nGenerated files:")
    print("  - install.bat (Windows installer)")
    print("  - README.md (Documentation)")
    print("  - dist/ (Built applications)")


if __name__ == "__main__":
    main()
# PicX GUI

[PicX](https://github.com/ingeniousfrog/picx) 的现代化图形用户界面，一个 Python 图片优化工具包。

[English](README.md) | 中文

## 功能特性

- **单图压缩** - 完整控制单张图片优化
- **目录批量处理** - 并行处理整个文件夹
- **大图切片** - 为超大图片生成切片和清单文件
- **环境诊断** - 检查系统配置
- **预设管理** - 使用内置或自定义预设
- **现代化界面** - 基于 CustomTkinter，支持深色/浅色主题

## 安装

### 快速开始（Windows）

1. **克隆仓库**
   ```bash
   git clone https://github.com/ingeniousfrog/picx-gui.git
   cd picx-gui
   ```

2. **下载并配置 libvips**（推荐，获取完整功能）
   ```bash
   python setup_libvips.py
   ```
   此脚本会自动下载并配置 libvips（约 50MB）

3. **安装 Python 依赖**
   ```bash
   pip install -r requirements.txt
   ```

4. **运行应用**
   ```bash
   python main.py
   ```

### 备选方案：不使用 libvips

如果不需要处理大图或 TIFF 格式：

```bash
pip install -r requirements.txt
python main.py
```

应用将使用 Pillow 后端进行基础图像处理。

### macOS/Linux

**macOS:**
```bash
brew install vips
pip install -r requirements.txt
python main.py
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt-get install libvips libvips-dev
pip install -r requirements.txt
python main.py
```

## 构建可执行文件

### Windows

**快速构建：**
```bash
build.bat
```

**高级构建（包含 libvips）：**
```bash
# 1. 下载并配置 libvips
python setup_libvips.py

# 2. 使用 libvips 支持进行构建
build.bat
```

可执行文件将生成在 `dist\PicX-GUI\PicX-GUI.exe`

**包大小：**
- 包含 libvips：约 60-80MB（完整格式支持）
- 不含 libvips：约 40-50MB（基础格式支持）

### macOS

```bash
# 使脚本可执行
chmod +x build.sh

# 运行构建
./build.sh
```

### Linux

```bash
# 使脚本可执行
chmod +x build.sh

# 运行构建
./build.sh
```

### 分发

压缩整个 `dist\PicX-GUI\` 文件夹（macOS 上为 `dist\PicX-GUI.app`）即可分发。用户可以直接运行应用程序，无需安装 Python 或任何依赖。

## 开发

安装开发依赖：

```bash
pip install -e ".[dev]"
```

运行测试：

```bash
pytest
```

## 构建可执行文件

使用 PyInstaller 创建独立可执行文件：

```bash
pyinstaller --onefile --windowed --name "PicX GUI" main.py
```

## 许可证

MIT License - 详见 LICENSE 文件

## 致谢

- PicX CLI 工具：https://github.com/ingeniousfrog/picx
- CustomTkinter：https://github.com/TomSchimansky/CustomTkinter

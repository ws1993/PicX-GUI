# PicX GUI

A modern graphical user interface for [PicX](https://github.com/ingeniousfrog/picx), a Python image optimization toolkit.

English | [中文](README_CN.md)

## Features

- **Single Image Compression** - Optimize individual images with full control
- **Batch Directory Processing** - Process entire folders with parallel jobs
- **Large Image Tiling** - Generate tiles and manifests for huge images
- **Environment Diagnostics** - Check your system setup
- **Preset Management** - Use built-in or create custom presets
- **Modern UI** - CustomTkinter-based interface with dark/light mode

## Installation

### Quick Start (Windows)

1. **Clone the repository**
   ```bash
   git clone https://github.com/ingeniousfrog/picx-gui.git
   cd picx-gui
   ```

2. **Download and configure libvips** (recommended for full functionality)
   ```bash
   python setup_libvips.py
   ```
   This script automatically downloads and configures libvips (~50MB)

3. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   python main.py
   ```

### Alternative: Without libvips

If you don't need large image or TIFF support:

```bash
pip install -r requirements.txt
python main.py
```

The application will use Pillow backend for basic image processing.

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

## Building Executables

### Windows

**Quick Build:**
```bash
build.bat
```

**Advanced Build (with libvips):**
```bash
# 1. Download and configure libvips
python setup_libvips.py

# 2. Build with libvips support
build.bat
```

The executable will be created in `dist\PicX-GUI\PicX-GUI.exe`

**Package size:**
- With libvips: ~60-80MB (full format support)
- Without libvips: ~40-50MB (basic format support)

### macOS

```bash
# Make script executable
chmod +x build.sh

# Run build
./build.sh
```

### Linux

```bash
# Make script executable
chmod +x build.sh

# Run build
./build.sh
```

### Distribution

Compress the entire `dist\PicX-GUI\` folder (or `dist\PicX-GUI.app` on macOS) and distribute. Users can run the application directly without installing Python or any dependencies.

## Development

Install development dependencies:

```bash
pip install -e ".[dev]"
```

Run tests:

```bash
pytest
```

## Building Executables

Create standalone executables with PyInstaller:

```bash
pyinstaller --onefile --windowed --name "PicX GUI" main.py
```

## License

MIT License - see LICENSE file for details.

## Credits

- PicX CLI tool: https://github.com/ingeniousfrog/picx
- CustomTkinter: https://github.com/TomSchimansky/CustomTkinter

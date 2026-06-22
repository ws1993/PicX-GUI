# PicX GUI 快速开始指南

## Windows 用户快速开始

### 方法一：完整功能版（推荐，包含libvips）

1. **下载并配置libvips**
   ```bash
   python setup_libvips.py
   ```
   这个脚本会自动下载并配置libvips（约50MB）

2. **安装Python依赖**
   ```bash
   pip install -r requirements.txt
   ```

3. **运行应用**
   ```bash
   python main.py
   ```

### 方法二：基础版（不包含libvips）

如果不需要处理大图或TIFF格式：

1. **安装Python依赖**
   ```bash
   pip install -r requirements.txt
   ```

2. **运行应用**
   ```bash
   python main.py
   ```

---

## 打包为可执行文件

### 准备打包

1. **确保libvips已配置**（如需完整功能）
   ```bash
   dir libs\libvips\bin
   ```
   应该看到许多 `.dll` 文件

2. **确保所有依赖已安装**
   ```bash
   pip install -r requirements.txt
   ```

### 执行打包

运行打包脚本：
```bash
build_windows.bat
```

打包完成后，可执行文件位于：`dist\PicX-GUI\PicX-GUI.exe`

### 分发应用

整个 `dist\PicX-GUI\` 文件夹可以压缩后分发：
- 用户无需安装Python
- 用户无需安装任何依赖
- 双击 `PicX-GUI.exe` 即可运行

打包大小参考：
- **仅Pillow后端**：约 40-50MB
- **包含libvips**：约 60-80MB

---

## 功能说明

### 已实现的功能 ✅

#### 单图压缩 Tab
- 完整支持PicX的所有12个参数
- 预设模式（web/blog/avatar/lossless）
- 格式转换（webp/jpg/png/avif/tiff）
- 质量调节（1-100）
- 尺寸调整（最大宽度/高度）
- 目标体积压缩
- 后端选择（auto/pillow/pyvips）
- 元数据处理

### 待实现的功能 🔲

- 目录批量处理 Tab
- 大图切片 Tab
- 环境诊断 Tab
- 预设管理 Tab

---

## 后端说明

PicX GUI支持两种图片处理后端：

### Pillow（必需）
- **用途**：基础图片处理
- **支持格式**：PNG, JPG, WebP等常见格式
- **安装**：`pip install Pillow`
- **特点**：轻量级，适合一般使用

### pyvips（可选，推荐）
- **用途**：大图和特殊格式处理
- **支持格式**：TIFF, HEIC, AVIF等
- **安装**：需要libvips + pyvips
- **特点**：内存效率高，处理速度快

**推荐配置**：同时使用两个后端，PicX会根据图片类型自动选择最佳后端。

---

## 常见问题

### Q1: setup_libvips.py下载很慢怎么办？

**A**: 可以手动下载：
1. 访问：https://github.com/libvips/libvips/releases
2. 下载：`vips-dev-w64-all-8.15.5.zip`（约50MB）
3. 解压后将 `bin` 目录复制到 `libs\libvips\bin\`

### Q2: 打包后的exe无法运行？

**A**: 尝试以下步骤：
1. 检查是否有杀毒软件拦截
2. 用 `console=True` 重新打包查看错误信息
3. 确认所有DLL文件都在 `dist\PicX-GUI\` 目录中

### Q3: 没有libvips可以使用吗？

**A**: 可以！应用会自动降级到Pillow后端：
- ✅ 可以处理PNG、JPG、WebP等常见格式
- ✅ 基础压缩和格式转换功能正常
- ❌ 无法处理大图（超过16383像素）
- ❌ 无法处理TIFF等特殊格式

### Q4: 如何更新libvips版本？

**A**: 修改 `setup_libvips.py` 中的版本号：
```python
LIBVIPS_VERSION = "8.15.5"  # 改为新版本号
```
然后重新运行脚本。

---

## 开发者信息

### 项目结构
```
PicX-GUI/
├── main.py                    # 应用入口
├── setup_libvips.py          # libvips配置工具
├── build_windows.bat         # 打包脚本
├── build_windows.spec        # PyInstaller配置
├── requirements.txt          # Python依赖
├── gui/                      # GUI代码
│   ├── app.py               # 主窗口
│   ├── tabs/                # 功能Tab
│   ├── widgets/             # 通用组件
│   ├── utils/               # 工具类
│   └── styles/              # 主题和样式
├── libs/                     # 第三方库
│   └── libvips/             # libvips（打包时包含）
│       └── bin/             # DLL文件
├── config/                   # 配置文件
└── assets/                   # 资源文件
```

### 技术栈
- **GUI**: CustomTkinter 5.2+
- **图像处理**: PicX 0.1.1+, Pillow 10.0+, pyvips 2.2+
- **打包**: PyInstaller 6.0+
- **Python**: 3.8+

### 贡献
欢迎提交Issue和Pull Request！

---

## 许可证

MIT License - 详见 LICENSE 文件

---

## 相关链接

- **PicX CLI**: https://github.com/ingeniousfrog/picx
- **libvips**: https://www.libvips.org/
- **CustomTkinter**: https://github.com/TomSchimansky/CustomTkinter

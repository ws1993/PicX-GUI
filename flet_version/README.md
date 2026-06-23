# PicX GUI - Flet版本

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

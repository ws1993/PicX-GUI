# PicX-GUI Flet 重构计划

## 1. 项目概述

### 1.1 重构目标
将 PicX-GUI 从 CustomTkinter (Tkinter) 迁移到 Flet 框架，实现：
- 现代化 UI 界面，提升用户体验
- 跨平台支持（桌面、Web、移动端）
- 统一代码库，降低维护成本
- 更好的性能和响应性

### 1.2 当前技术栈
- GUI 框架：CustomTkinter 5.3.0+
- 图像处理：Pillow + pyvips
- 拖放支持：tkinterdnd2
- 打包工具：PyInstaller

### 1.3 目标技术栈
- GUI 框架：Flet (最新版本)
- 图像处理：Pillow + pyvips (保持不变)
- 拖放支持：Flet 内置支持
- 打包工具：Flet 内置打包 + PyInstaller

## 2. 重构范围

### 2.1 需要重构的模块

#### 核心模块 (15个文件)
1. **main.py** - 应用入口点
2. **gui/app.py** - 主应用程序窗口
3. **gui/tabs/single_image_optimized.py** - 单图压缩模块
4. **gui/tabs/batch.py** - 批量处理模块
5. **gui/tabs/tile.py** - 大图切片模块
6. **gui/tabs/doctor.py** - 环境诊断模块
7. **gui/tabs/presets.py** - 预设管理模块
8. **gui/widgets/file_selector.py** - 文件选择器组件
9. **gui/widgets/progress_item.py** - 进度条组件
10. **gui/widgets/drop_zone.py** - 拖放区域组件
11. **gui/widgets/image_preview.py** - 图片预览组件
12. **gui/styles/theme.py** - 主题配置
13. **gui/styles/theme_modern.py** - 现代主题
14. **gui/locales/__init__.py** - 国际化配置
15. **gui/utils/task_manager.py** - 任务管理器

#### 配置文件 (3个文件)
1. **requirements.txt** - 依赖配置
2. **config/default.json** - 默认配置
3. **themes/breeze.json** - 主题配置

### 2.2 组件映射表

| CustomTkinter 组件 | Flet 对应组件 | 使用位置 | 重构复杂度 |
|-------------------|-------------|---------|-----------|
| CTk | ft.app + ft.Page | main.py | 低 |
| CTkFrame | ft.Container, ft.Card | 所有模块 | 低 |
| CTkLabel | ft.Text | 所有模块 | 低 |
| CTkButton | ft.Button, ft.FilledButton等 | 所有模块 | 低 |
| CTkEntry | ft.TextField | 文件选择器 | 低 |
| CTkSlider | ft.Slider | 单图压缩 | 低 |
| CTkCheckBox | ft.Checkbox | 批量处理 | 低 |
| CTkRadioButton | ft.Radio, ft.RadioGroup | 预设管理 | 低 |
| CTkProgressBar | ft.ProgressBar | 进度条组件 | 低 |
| CTkScrollableFrame | ft.ListView, ft.Column | 所有模块 | 中 |
| CTkSwitch | ft.Switch | 设置模块 | 低 |
| CTkOptionMenu | ft.Dropdown | 所有模块 | 低 |
| CTkTabview | ft.Tabs | 主窗口 | 中 |
| CTkScrollableFrame | ft.ListView | 批量处理 | 中 |

## 3. 详细实施计划

### 3.1 阶段一：基础架构搭建 (第1-2周)

#### 目标
- 搭建 Flet 开发环境
- 创建基础项目结构
- 实现核心框架

#### 具体任务
1. **环境准备** (2天)
   - 安装 Flet：`pip install 'flet[all]'`
   - 创建新的项目目录结构
   - 配置开发环境

2. **基础框架** (3天)
   - 创建 `flet_main.py` - 新的入口点
   - 实现 `flet_app.py` - 基础应用框架
   - 创建 `flet_styles/` - Flet 主题系统
   - 实现基础布局和导航

3. **核心组件库** (5天)
   - 创建 `flet_widgets/` - Flet 组件库
   - 实现 `FileSelector` 组件
   - 实现 `ProgressItem` 组件
   - 实现 `DropZone` 组件
   - 实现 `ImagePreview` 组件

#### 里程碑
- [ ] Flet 开发环境配置完成
- [ ] 基础应用框架运行正常
- [ ] 核心组件库可用

### 3.2 阶段二：核心功能重构 (第3-6周)

#### 目标
- 重构主要功能模块
- 实现功能对等
- 保持用户体验一致

#### 具体任务
1. **单图压缩模块** (1周)
   - 重构 `single_image_optimized.py`
   - 实现文件选择、参数配置、压缩执行
   - 实现实时预览和进度显示

2. **批量处理模块** (1周)
   - 重构 `batch.py`
   - 实现目录选择、批量配置
   - 实现并行处理和进度跟踪

3. **大图切片模块** (1周)
   - 重构 `tile.py`
   - 实现切片参数配置
   - 实现切片预览和导出

4. **环境诊断模块** (3天)
   - 重构 `doctor.py`
   - 实现系统检测
   - 实现诊断报告

5. **预设管理模块** (3天)
   - 重构 `presets.py`
   - 实现预设 CRUD
   - 实现预设导入导出

#### 里程碑
- [ ] 单图压缩功能完整
- [ ] 批量处理功能完整
- [ ] 大图切片功能完整
- [ ] 环境诊断功能完整
- [ ] 预设管理功能完整

### 3.3 阶段三：高级功能和优化 (第7-8周)

#### 目标
- 实现高级功能
- 性能优化
- 用户体验提升

#### 具体任务
1. **主题系统** (3天)
   - 实现深色/浅色主题切换
   - 实现自定义主题配置
   - 优化主题响应性

2. **国际化支持** (2天)
   - 重构国际化系统
   - 支持多语言切换
   - 优化文本显示

3. **拖放功能** (3天)
   - 实现 Flet 原生拖放
   - 支持文件/文件夹拖放
   - 优化拖放反馈

4. **性能优化** (4天)
   - 优化大文件处理
   - 实现懒加载
   - 优化内存使用

5. **键盘快捷键** (2天)
   - 实现快捷键系统
   - 支持自定义快捷键
   - 优化快捷键提示

#### 里程碑
- [ ] 主题系统完整
- [ ] 国际化支持完整
- [ ] 拖放功能完整
- [ ] 性能优化完成
- [ ] 键盘快捷键完整

### 3.4 阶段四：测试和打包 (第9-10周)

#### 目标
- 全面测试
- 打包和分发
- 文档更新

#### 具体任务
1. **功能测试** (3天)
   - 单元测试编写
   - 集成测试
   - 用户验收测试

2. **兼容性测试** (2天)
   - Windows 测试
   - macOS 测试
   - Linux 测试
   - Web 测试

3. **打包和分发** (3天)
   - 配置 Flet 打包
   - 创建安装程序
   - 测试分发包

4. **文档更新** (2天)
   - 更新 README
   - 更新用户手册
   - 更新开发文档

#### 里程碑
- [ ] 所有测试通过
- [ ] 跨平台兼容性验证
- [ ] 打包和分发完成
- [ ] 文档更新完成

## 4. 技术实现方案

### 4.1 项目结构

```
picx-gui-flet/
├── main.py                    # Flet 入口点
├── app.py                     # 主应用类
├── requirements.txt           # 依赖配置
├── pyproject.toml             # 项目配置
├── config/
│   └── default.json           # 默认配置
├── themes/
│   └── breeze.json            # 主题配置
├── gui/
│   ├── __init__.py
│   ├── app.py                 # 主应用窗口
│   ├── tabs/
│   │   ├── __init__.py
│   │   ├── single_image.py    # 单图压缩
│   │   ├── batch.py           # 批量处理
│   │   ├── tile.py            # 大图切片
│   │   ├── doctor.py          # 环境诊断
│   │   └── presets.py         # 预设管理
│   ├── widgets/
│   │   ├── __init__.py
│   │   ├── file_selector.py   # 文件选择器
│   │   ├── progress_item.py   # 进度条
│   │   ├── drop_zone.py       # 拖放区域
│   │   └── image_preview.py   # 图片预览
│   ├── styles/
│   │   ├── __init__.py
│   │   ├── theme.py           # 主题配置
│   │   └── colors.py          # 颜色配置
│   ├── locales/
│   │   ├── __init__.py
│   │   ├── zh_CN.py           # 中文
│   │   └── en_US.py           # 英文
│   └── utils/
│       ├── __init__.py
│       ├── config.py          # 配置管理
│       ├── task_manager.py    # 任务管理
│       └── validators.py      # 验证器
├── tests/
│   ├── __init__.py
│   ├── test_app.py
│   ├── test_tabs.py
│   └── test_widgets.py
└── assets/
    ├── icon.ico
    └── images/
```

### 4.2 核心代码示例

#### 4.2.1 主入口点 (main.py)
```python
"""PicX GUI - Flet version."""
import flet as ft
from gui.app import PicXApp

def main(page: ft.Page):
    """Main entry point."""
    page.title = "PicX - 图片优化工具"
    page.window.width = 1200
    page.window.height = 800
    page.window.min_width = 800
    page.window.min_height = 600
    
    # 创建应用实例
    app = PicXApp(page)
    app.build()

if __name__ == "__main__":
    ft.app(target=main)
```

#### 4.2.2 主应用类 (gui/app.py)
```python
"""Main application class."""
import flet as ft
from gui.tabs.single_image import SingleImageTab
from gui.tabs.batch import BatchTab
from gui.tabs.tile import TileTab
from gui.tabs.doctor import DoctorTab
from gui.tabs.presets import PresetsTab

class PicXApp:
    """PicX GUI Application."""
    
    def __init__(self, page: ft.Page):
        self.page = page
        self.page.theme_mode = ft.ThemeMode.LIGHT
        self._setup_theme()
        
    def _setup_theme(self):
        """Setup application theme."""
        self.page.theme = ft.Theme(
            color_scheme_seed=ft.Colors.AMBER,
            visual_density=ft.VisualDensity.COMFORTABLE,
        )
        
    def build(self):
        """Build the application UI."""
        # 创建标签页
        self.tabs = ft.Tabs(
            selected_index=0,
            animation_duration=300,
            tabs=[
                ft.Tab(text="单图压缩", icon=ft.Icons.IMAGE),
                ft.Tab(text="批量处理", icon=ft.Icons.COLLECTIONS),
                ft.Tab(text="大图切片", icon=ft.Icons.GRID_ON),
                ft.Tab(text="环境诊断", icon=ft.Icons.BUILD),
                ft.Tab(text="预设管理", icon=ft.Icons.SETTINGS),
            ],
            on_change=self._on_tab_change,
        )
        
        # 创建内容区域
        self.content = ft.Container(
            content=ft.Column([]),
            expand=True,
        )
        
        # 布局
        self.page.add(
            ft.Column([
                self._create_header(),
                self.tabs,
                self.content,
                self._create_status_bar(),
            ], expand=True)
        )
        
        # 加载默认标签页
        self._load_tab(0)
        
    def _create_header(self):
        """Create application header."""
        return ft.Container(
            content=ft.Row([
                ft.Column([
                    ft.Text("PicX", size=24, weight=ft.FontWeight.BOLD),
                    ft.Text("图片优化工具", size=14, color=ft.Colors.GREY_600),
                ], spacing=4),
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            bgcolor=ft.Colors.GREY_900,
            padding=20,
        )
        
    def _create_status_bar(self):
        """Create status bar."""
        return ft.Container(
            content=ft.Text("就绪", size=12),
            bgcolor=ft.Colors.GREY_100,
            padding=10,
        )
        
    def _on_tab_change(self, e):
        """Handle tab change."""
        self._load_tab(e.control.selected_index)
        
    def _load_tab(self, index):
        """Load tab content."""
        tabs = [
            SingleImageTab(self.page),
            BatchTab(self.page),
            TileTab(self.page),
            DoctorTab(self.page),
            PresetsTab(self.page),
        ]
        
        if index < len(tabs):
            self.content.content = tabs[index].build()
            self.page.update()
```

#### 4.2.3 文件选择器组件 (gui/widgets/file_selector.py)
```python
"""File selector widget."""
import flet as ft
from typing import Callable, Optional, List

class FileSelector(ft.UserControl):
    """File selector widget."""
    
    def __init__(
        self,
        mode: str = "file",  # file, directory, save
        label_text: str = "选择文件:",
        file_types: Optional[List[dict]] = None,
        on_change: Optional[Callable[[str], None]] = None,
    ):
        super().__init__()
        self.mode = mode
        self.label_text = label_text
        self.file_types = file_types or []
        self.on_change = on_change
        self.file_path = ""
        
    def build(self):
        """Build the widget."""
        self.path_field = ft.TextField(
            label=self.label_text,
            read_only=True,
            expand=True,
        )
        
        browse_button = ft.ElevatedButton(
            "浏览...",
            icon=ft.Icons.FOLDER_OPEN,
            on_click=self._on_browse,
        )
        
        return ft.Row([
            self.path_field,
            browse_button,
        ], alignment=ft.MainAxisAlignment.START)
        
    async def _on_browse(self, e):
        """Handle browse button click."""
        if self.mode == "file":
            file_picker = ft.FilePicker(
                on_result=self._on_file_picked,
            )
            self.page.overlay.append(file_picker)
            self.page.update()
            await file_picker.pick_files(
                allowed_extensions=self.file_types,
            )
        elif self.mode == "directory":
            dir_picker = ft.FilePicker(
                on_result=self._on_dir_picked,
            )
            self.page.overlay.append(dir_picker)
            self.page.update()
            await dir_picker.get_directory_path()
            
    def _on_file_picked(self, e):
        """Handle file picked."""
        if e.files:
            self.file_path = e.files[0].path
            self.path_field.value = self.file_path
            self.update()
            if self.on_change:
                self.on_change(self.file_path)
                
    def _on_dir_picked(self, e):
        """Handle directory picked."""
        if e.path:
            self.file_path = e.path
            self.path_field.value = self.file_path
            self.update()
            if self.on_change:
                self.on_change(self.file_path)
```

## 5. 风险评估和应对策略

### 5.1 技术风险

#### 风险1：组件兼容性问题
- **可能性**：中
- **影响**：高
- **应对策略**：
  - 提前进行组件兼容性测试
  - 准备替代方案
  - 建立组件映射文档

#### 风险2：性能问题
- **可能性**：低
- **影响**：中
- **应对策略**：
  - 进行性能基准测试
  - 优化关键路径
  - 实现懒加载

#### 风险3：跨平台兼容性
- **可能性**：中
- **影响**：中
- **应对策略**：
  - 分阶段测试各平台
  - 建立自动化测试
  - 准备平台特定代码

### 5.2 项目风险

#### 风险1：时间超期
- **可能性**：中
- **影响**：中
- **应对策略**：
  - 设置缓冲时间
  - 优先核心功能
  - 分阶段交付

#### 风险2：资源不足
- **可能性**：低
- **影响**：高
- **应对策略**：
  - 提前规划资源
  - 外包非核心部分
  - 使用现成组件

### 5.3 应对措施

1. **技术风险应对**
   - 建立技术预研机制
   - 定期技术评审
   - 建立技术储备

2. **项目风险应对**
   - 严格的项目管理
   - 定期进度检查
   - 灵活调整计划

## 6. 资源需求

### 6.1 人力资源

| 角色 | 人数 | 职责 | 技能要求 |
|------|------|------|----------|
| 项目经理 | 1 | 项目规划和管理 | 项目管理经验 |
| 高级开发工程师 | 2 | 核心模块开发 | Python, Flet, GUI开发 |
| 初级开发工程师 | 1 | 辅助开发和测试 | Python基础 |
| 测试工程师 | 1 | 质量保证 | 测试经验 |
| UI/UX设计师 | 1 | 界面设计 | UI/UX设计 |

### 6.2 硬件资源

| 资源 | 数量 | 用途 |
|------|------|------|
| 开发电脑 | 4台 | 开发工作 |
| 测试设备 | 3台 | 跨平台测试 |
| 服务器 | 1台 | 持续集成 |

### 6.3 软件资源

| 软件 | 用途 |
|------|------|
| Python 3.8+ | 开发环境 |
| Flet | GUI框架 |
| PyInstaller | 打包工具 |
| Git | 版本控制 |
| VS Code | 开发工具 |
| pytest | 测试框架 |

## 7. 质量保证

### 7.1 代码质量

1. **代码规范**
   - 遵循 PEP 8 规范
   - 使用类型注解
   - 编写文档字符串

2. **代码审查**
   - 每次提交必须审查
   - 使用自动化工具
   - 定期代码重构

3. **单元测试**
   - 测试覆盖率 > 80%
   - 自动化测试
   - 持续集成

### 7.2 测试策略

1. **单元测试**
   - 测试每个组件
   - 测试业务逻辑
   - 测试工具函数

2. **集成测试**
   - 测试模块集成
   - 测试用户流程
   - 测试错误处理

3. **用户验收测试**
   - 功能测试
   - 性能测试
   - 兼容性测试

### 7.3 持续集成

```yaml
# .github/workflows/ci.yml
name: CI

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ${{ matrix.os }}
    strategy:
      matrix:
        os: [ubuntu-latest, windows-latest, macos-latest]
        python-version: [3.8, 3.9, '3.10', '3.11']
    
    steps:
    - uses: actions/checkout@v2
    
    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v2
      with:
        python-version: ${{ matrix.python-version }}
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
        pip install -r requirements-dev.txt
    
    - name: Run tests
      run: |
        pytest tests/ -v --cov=gui --cov-report=xml
    
    - name: Upload coverage
      uses: codecov/codecov-action@v2
      with:
        file: ./coverage.xml
```

## 8. 交付物清单

### 8.1 代码交付物
- [ ] Flet 版本源代码
- [ ] 单元测试代码
- [ ] 集成测试代码
- [ ] 配置文件

### 8.2 文档交付物
- [ ] 用户手册
- [ ] 开发文档
- [ ] API 文档
- [ ] 部署指南

### 8.3 工具交付物
- [ ] 安装程序
- [ ] 打包脚本
- [ ] 部署脚本
- [ ] 监控工具

## 9. 成功标准

### 9.1 功能标准
- 所有原有功能完整实现
- 新功能按计划实现
- 用户体验提升

### 9.2 质量标准
- 代码测试覆盖率 > 80%
- 无严重 bug
- 性能不低于原版本

### 9.3 时间标准
- 按计划时间完成
- 关键里程碑按时达成
- 项目按时交付

## 10. 后续维护

### 10.1 维护计划
- 定期更新依赖
- 修复发现的问题
- 添加新功能

### 10.2 版本规划
- v1.0：基础功能
- v1.1：性能优化
- v1.2：新功能
- v2.0：重大更新

### 10.3 社区支持
- 建立用户社区
- 收集用户反馈
- 持续改进

---

**文档版本**：1.0  
**创建日期**：2026-06-22  
**最后更新**：2026-06-22  
**作者**：PicX-GUI 开发团队
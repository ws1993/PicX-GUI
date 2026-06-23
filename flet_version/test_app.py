"""Test script for PicX GUI - Flet version."""
import sys
import os

# 添加当前目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import flet as ft
from gui.app import PicXApp


def test_app():
    """Test the application."""
    print("测试 PicX GUI - Flet 版本")
    print("=" * 50)
    
    # 检查模块导入
    try:
        from gui.tabs.single_image import SingleImageTab
        from gui.tabs.batch import BatchTab
        from gui.tabs.tile import TileTab
        from gui.tabs.doctor import DoctorTab
        from gui.tabs.presets import PresetsTab
        print("✓ 所有标签页模块导入成功")
    except Exception as e:
        print(f"✗ 标签页模块导入失败: {e}")
        return False
    
    # 检查组件导入
    try:
        from gui.widgets.file_selector import FileSelector
        from gui.widgets.progress_item import ProgressItem
        from gui.widgets.drop_zone import DropZone
        from gui.widgets.image_preview import ImagePreview
        print("✓ 所有组件模块导入成功")
    except Exception as e:
        print(f"✗ 组件模块导入失败: {e}")
        return False
    
    # 检查主题导入
    try:
        from gui.styles.theme import COLORS, FONTS, SIZES, SPACING
        print("✓ 主题模块导入成功")
    except Exception as e:
        print(f"✗ 主题模块导入失败: {e}")
        return False
    
    print("=" * 50)
    print("所有模块导入测试通过！")
    print("\n启动应用程序...")
    
    # 启动应用
    def main(page: ft.Page):
        page.title = "PicX - 图片优化工具"
        page.window.width = 1200
        page.window.height = 800
        page.window.min_width = 800
        page.window.min_height = 600
        
        # 设置主题
        page.theme_mode = ft.ThemeMode.LIGHT
        page.theme = ft.Theme(
            color_scheme_seed=ft.Colors.AMBER,
            visual_density=ft.VisualDensity.COMFORTABLE,
        )
        
        # 创建应用实例
        app = PicXApp(page)
        app.build()
    
    try:
        ft.app(target=main)
        return True
    except Exception as e:
        print(f"✗ 应用启动失败: {e}")
        return False


if __name__ == "__main__":
    success = test_app()
    if success:
        print("应用测试完成！")
    else:
        print("应用测试失败！")
        sys.exit(1)
"""Unit tests for PicX GUI - Flet version."""
import sys
import os
import unittest

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class TestThemeManager(unittest.TestCase):
    """Test ThemeManager class."""
    
    def test_theme_manager_initialization(self):
        """Test ThemeManager initialization."""
        from gui.styles.theme import ThemeManager
        
        # 创建模拟的page对象
        class MockPage:
            def __init__(self):
                self.theme_mode = None
                self.theme = None
                
            def update(self):
                pass
        
        page = MockPage()
        manager = ThemeManager(page)
        
        self.assertFalse(manager.is_dark_mode)
        self.assertIsNotNone(manager.current_colors)
        
    def test_theme_toggle(self):
        """Test theme toggle functionality."""
        from gui.styles.theme import ThemeManager
        
        class MockPage:
            def __init__(self):
                self.theme_mode = None
                self.theme = None
                
            def update(self):
                pass
        
        page = MockPage()
        manager = ThemeManager(page)
        
        # 初始状态应该是浅色主题
        self.assertFalse(manager.is_dark_mode)
        
        # 切换到深色主题
        is_dark = manager.toggle_theme()
        self.assertTrue(is_dark)
        self.assertTrue(manager.is_dark_mode)
        
        # 再次切换回浅色主题
        is_dark = manager.toggle_theme()
        self.assertFalse(is_dark)
        self.assertFalse(manager.is_dark_mode)
        
    def test_get_color(self):
        """Test get_color method."""
        from gui.styles.theme import ThemeManager, COLORS
        
        class MockPage:
            def __init__(self):
                self.theme_mode = None
                self.theme = None
                
            def update(self):
                pass
        
        page = MockPage()
        manager = ThemeManager(page)
        
        # 测试获取颜色
        primary_color = manager.get_color("primary")
        self.assertEqual(primary_color, COLORS["primary"])
        
        # 测试获取不存在的颜色
        unknown_color = manager.get_color("unknown")
        self.assertIsNone(unknown_color)


class TestLocaleManager(unittest.TestCase):
    """Test LocaleManager class."""
    
    def test_locale_manager_initialization(self):
        """Test LocaleManager initialization."""
        from gui.locales import LocaleManager
        
        manager = LocaleManager("zh_CN")
        
        self.assertEqual(manager.language, "zh_CN")
        self.assertIsNotNone(manager.current_locale)
        
    def test_set_language(self):
        """Test set_language method."""
        from gui.locales import LocaleManager
        
        manager = LocaleManager("zh_CN")
        
        # 初始语言应该是中文
        self.assertEqual(manager.language, "zh_CN")
        
        # 切换到英文
        manager.set_language("en_US")
        self.assertEqual(manager.language, "en_US")
        
        # 测试无效语言代码
        manager.set_language("invalid")
        self.assertEqual(manager.language, "en_US")  # 应该保持不变
        
    def test_get_text(self):
        """Test get method."""
        from gui.locales import LocaleManager
        
        manager = LocaleManager("zh_CN")
        
        # 测试获取中文文本
        app_name = manager.get("app_name")
        self.assertEqual(app_name, "PicX - 图片优化工具")
        
        # 测试获取不存在的键
        unknown_text = manager.get("unknown_key", "default")
        self.assertEqual(unknown_text, "default")
        
    def test_get_available_languages(self):
        """Test get_available_languages method."""
        from gui.locales import LocaleManager
        
        manager = LocaleManager()
        languages = manager.get_available_languages()
        
        self.assertIn("zh_CN", languages)
        self.assertIn("en_US", languages)
        
    def test_get_language_name(self):
        """Test get_language_name method."""
        from gui.locales import LocaleManager
        
        manager = LocaleManager()
        
        # 测试获取语言名称
        self.assertEqual(manager.get_language_name("zh_CN"), "中文")
        self.assertEqual(manager.get_language_name("en_US"), "English")
        
        # 测试未知语言代码
        self.assertEqual(manager.get_language_name("unknown"), "unknown")


class TestKeyboardShortcutManager(unittest.TestCase):
    """Test KeyboardShortcutManager class."""
    
    def test_shortcut_manager_initialization(self):
        """Test KeyboardShortcutManager initialization."""
        from gui.utils.keyboard_shortcuts import KeyboardShortcutManager
        
        class MockPage:
            def __init__(self):
                self.on_keyboard_event = None
                
        page = MockPage()
        manager = KeyboardShortcutManager(page)
        
        self.assertTrue(manager.enabled)
        self.assertEqual(len(manager.shortcuts), 0)
        
    def test_register_shortcut(self):
        """Test register_shortcut method."""
        from gui.utils.keyboard_shortcuts import KeyboardShortcutManager
        
        class MockPage:
            def __init__(self):
                self.on_keyboard_event = None
                
        page = MockPage()
        manager = KeyboardShortcutManager(page)
        
        # 注册快捷键
        manager.register_shortcut(
            "test",
            key="T",
            ctrl=True,
            action=lambda e: None,
            description="Test shortcut",
        )
        
        self.assertIn("test", manager.shortcuts)
        self.assertEqual(manager.shortcuts["test"].key, "T")
        self.assertTrue(manager.shortcuts["test"].ctrl)
        
    def test_unregister_shortcut(self):
        """Test unregister_shortcut method."""
        from gui.utils.keyboard_shortcuts import KeyboardShortcutManager
        
        class MockPage:
            def __init__(self):
                self.on_keyboard_event = None
                
        page = MockPage()
        manager = KeyboardShortcutManager(page)
        
        # 注册快捷键
        manager.register_shortcut(
            "test",
            key="T",
            ctrl=True,
            action=lambda e: None,
            description="Test shortcut",
        )
        
        self.assertIn("test", manager.shortcuts)
        
        # 注销快捷键
        manager.unregister_shortcut("test")
        self.assertNotIn("test", manager.shortcuts)
        
    def test_enable_disable(self):
        """Test enable and disable methods."""
        from gui.utils.keyboard_shortcuts import KeyboardShortcutManager
        
        class MockPage:
            def __init__(self):
                self.on_keyboard_event = None
                
        page = MockPage()
        manager = KeyboardShortcutManager(page)
        
        # 初始状态应该是启用的
        self.assertTrue(manager.enabled)
        
        # 禁用
        manager.disable()
        self.assertFalse(manager.enabled)
        
        # 启用
        manager.enable()
        self.assertTrue(manager.enabled)


class TestSingleImageTab(unittest.TestCase):
    """Test SingleImageTab class."""
    
    def test_single_image_tab_initialization(self):
        """Test SingleImageTab initialization."""
        from gui.tabs.single_image import SingleImageTab
        
        class MockPage:
            def __init__(self):
                self.overlay = []
                
            def update(self):
                pass
                
            def open(self, dialog):
                pass
                
            def close(self, dialog):
                pass
        
        page = MockPage()
        tab = SingleImageTab(page)
        
        self.assertEqual(tab.page, page)
        self.assertEqual(tab.input_path, "")
        self.assertEqual(tab.output_path, "")
        
    def test_presets(self):
        """Test presets configuration."""
        from gui.tabs.single_image import SingleImageTab
        
        class MockPage:
            def __init__(self):
                self.overlay = []
                
            def update(self):
                pass
                
            def open(self, dialog):
                pass
                
            def close(self, dialog):
                pass
        
        page = MockPage()
        tab = SingleImageTab(page)
        
        # 检查预设配置
        self.assertIn("Custom", tab.PRESETS)
        self.assertIn("web", tab.PRESETS)
        self.assertIn("blog", tab.PRESETS)
        self.assertIn("avatar", tab.PRESETS)
        self.assertIn("lossless", tab.PRESETS)
        
        # 检查预设内容
        web_preset = tab.PRESETS["web"]
        self.assertEqual(web_preset["format"], "webp")
        self.assertEqual(web_preset["quality"], 82)
        self.assertEqual(web_preset["max_width"], 1920)


class TestBatchTab(unittest.TestCase):
    """Test BatchTab class."""
    
    def test_batch_tab_initialization(self):
        """Test BatchTab initialization."""
        from gui.tabs.batch import BatchTab
        
        class MockPage:
            def __init__(self):
                self.overlay = []
                
            def update(self):
                pass
                
            def open(self, dialog):
                pass
                
            def close(self, dialog):
                pass
        
        page = MockPage()
        tab = BatchTab(page)
        
        self.assertEqual(tab.page, page)
        self.assertEqual(tab.source_dir, "")
        self.assertEqual(tab.output_dir, "")
        self.assertEqual(len(tab.files), 0)
        self.assertFalse(tab.is_processing)
        self.assertFalse(tab.stop_processing)


if __name__ == "__main__":
    unittest.main()
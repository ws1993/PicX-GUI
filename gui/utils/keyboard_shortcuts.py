"""Keyboard shortcuts manager."""
import flet as ft
from typing import Dict, Callable, Any


class KeyboardShortcut:
    """Keyboard shortcut definition."""
    
    def __init__(
        self,
        key: str,
        ctrl: bool = False,
        alt: bool = False,
        shift: bool = False,
        action: Callable[[ft.KeyboardEvent], Any] = None,
        description: str = "",
    ):
        self.key = key
        self.ctrl = ctrl
        self.alt = alt
        self.shift = shift
        self.action = action
        self.description = description
        
    def matches(self, event: ft.KeyboardEvent) -> bool:
        """Check if event matches this shortcut."""
        return (
            event.key == self.key and
            event.ctrl == self.ctrl and
            event.alt == self.alt and
            event.shift == self.shift
        )
        
    def __str__(self):
        parts = []
        if self.ctrl:
            parts.append("Ctrl")
        if self.alt:
            parts.append("Alt")
        if self.shift:
            parts.append("Shift")
        parts.append(self.key)
        return " + ".join(parts)


class KeyboardShortcutManager:
    """Manager for keyboard shortcuts."""
    
    def __init__(self, page: ft.Page):
        self.page = page
        self.shortcuts: Dict[str, KeyboardShortcut] = {}
        self.enabled = True
        
        # 注册键盘事件处理
        self.page.on_keyboard_event = self._on_keyboard_event
        
    def register_shortcut(
        self,
        name: str,
        key: str,
        ctrl: bool = False,
        alt: bool = False,
        shift: bool = False,
        action: Callable[[ft.KeyboardEvent], Any] = None,
        description: str = "",
    ):
        """Register a keyboard shortcut."""
        shortcut = KeyboardShortcut(
            key=key,
            ctrl=ctrl,
            alt=alt,
            shift=shift,
            action=action,
            description=description,
        )
        self.shortcuts[name] = shortcut
        
    def unregister_shortcut(self, name: str):
        """Unregister a keyboard shortcut."""
        if name in self.shortcuts:
            del self.shortcuts[name]
            
    def enable(self):
        """Enable keyboard shortcuts."""
        self.enabled = True
        
    def disable(self):
        """Disable keyboard shortcuts."""
        self.enabled = False
        
    def _on_keyboard_event(self, event: ft.KeyboardEvent):
        """Handle keyboard event."""
        if not self.enabled:
            return
            
        # 查找匹配的快捷键
        for name, shortcut in self.shortcuts.items():
            if shortcut.matches(event):
                if shortcut.action:
                    shortcut.action(event)
                break
                
    def get_shortcuts_info(self) -> Dict[str, str]:
        """Get information about all registered shortcuts."""
        return {
            name: str(shortcut)
            for name, shortcut in self.shortcuts.items()
        }
        
    def get_shortcut_description(self, name: str) -> str:
        """Get description of a shortcut."""
        if name in self.shortcuts:
            return self.shortcuts[name].description
        return ""


def create_default_shortcuts(page: ft.Page) -> KeyboardShortcutManager:
    """Create default keyboard shortcuts."""
    manager = KeyboardShortcutManager(page)
    
    # 文件操作
    manager.register_shortcut(
        "open_file",
        key="O",
        ctrl=True,
        action=lambda e: print("打开文件"),
        description="打开文件",
    )
    
    manager.register_shortcut(
        "open_directory",
        key="O",
        ctrl=True,
        shift=True,
        action=lambda e: print("打开目录"),
        description="打开目录",
    )
    
    manager.register_shortcut(
        "save",
        key="S",
        ctrl=True,
        action=lambda e: print("保存"),
        description="保存",
    )
    
    # 编辑操作
    manager.register_shortcut(
        "undo",
        key="Z",
        ctrl=True,
        action=lambda e: print("撤销"),
        description="撤销",
    )
    
    manager.register_shortcut(
        "redo",
        key="Y",
        ctrl=True,
        action=lambda e: print("重做"),
        description="重做",
    )
    
    # 视图操作
    manager.register_shortcut(
        "refresh",
        key="F5",
        action=lambda e: print("刷新"),
        description="刷新",
    )
    
    manager.register_shortcut(
        "toggle_theme",
        key="T",
        ctrl=True,
        action=lambda e: print("切换主题"),
        description="切换主题",
    )
    
    manager.register_shortcut(
        "toggle_language",
        key="L",
        ctrl=True,
        action=lambda e: print("切换语言"),
        description="切换语言",
    )
    
    # 标签页切换
    manager.register_shortcut(
        "tab_single",
        key="1",
        ctrl=True,
        action=lambda e: print("单图压缩"),
        description="切换到单图压缩",
    )
    
    manager.register_shortcut(
        "tab_batch",
        key="2",
        ctrl=True,
        action=lambda e: print("批量处理"),
        description="切换到批量处理",
    )
    
    manager.register_shortcut(
        "tab_tile",
        key="3",
        ctrl=True,
        action=lambda e: print("大图切片"),
        description="切换到大图切片",
    )
    
    manager.register_shortcut(
        "tab_doctor",
        key="4",
        ctrl=True,
        action=lambda e: print("环境诊断"),
        description="切换到环境诊断",
    )
    
    manager.register_shortcut(
        "tab_presets",
        key="5",
        ctrl=True,
        action=lambda e: print("预设管理"),
        description="切换到预设管理",
    )
    
    # 帮助
    manager.register_shortcut(
        "help",
        key="F1",
        action=lambda e: print("帮助"),
        description="显示帮助",
    )
    
    manager.register_shortcut(
        "quit",
        key="Q",
        ctrl=True,
        action=lambda e: print("退出"),
        description="退出应用",
    )
    
    return manager
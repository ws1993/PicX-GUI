"""Configuration management for PicX GUI."""
import json
import os
from pathlib import Path
from typing import Dict, Any, Optional


class ConfigManager:
    """Manages application configuration."""
    
    DEFAULT_CONFIG = {
        "theme": "light",
        "window": {
            "width": 1200,
            "height": 800,
            "x": None,
            "y": None
        },
        "last_paths": {
            "input_file": "",
            "input_dir": "",
            "output_dir": ""
        },
        "defaults": {
            "format": "webp",
            "quality": 82,
            "backend": "auto",
            "strip_meta": True
        },
        "recent_tasks": []
    }
    
    def __init__(self, config_dir: Optional[str] = None):
        """
        Initialize ConfigManager.
        
        Args:
            config_dir: Configuration directory path. Defaults to 'config' in project root.
        """
        if config_dir:
            self.config_dir = Path(config_dir)
        else:
            # Default to 'config' directory in project root
            project_root = Path(__file__).parent.parent.parent
            self.config_dir = project_root / "config"
            
        self.config_file = self.config_dir / "user_config.json"
        self.config = self._load_config()
        
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from file."""
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    user_config = json.load(f)
                    
                # Merge with defaults (user config takes precedence)
                config = self.DEFAULT_CONFIG.copy()
                self._deep_merge(config, user_config)
                return config
            except Exception as e:
                print(f"Error loading config: {e}")
                return self.DEFAULT_CONFIG.copy()
        else:
            return self.DEFAULT_CONFIG.copy()
            
    def _deep_merge(self, base: dict, override: dict):
        """Deep merge two dictionaries."""
        for key, value in override.items():
            if key in base and isinstance(base[key], dict) and isinstance(value, dict):
                self._deep_merge(base[key], value)
            else:
                base[key] = value
                
    def save(self):
        """Save configuration to file."""
        try:
            self.config_dir.mkdir(parents=True, exist_ok=True)
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error saving config: {e}")
            
    def get(self, key_path: str, default: Any = None) -> Any:
        """
        Get a configuration value using dot notation.
        
        Args:
            key_path: Dot-separated path (e.g., 'window.width')
            default: Default value if key not found
            
        Returns:
            Configuration value
        """
        keys = key_path.split('.')
        value = self.config
        
        for key in keys:
            if isinstance(value, dict) and key in value:
                value = value[key]
            else:
                return default
                
        return value
        
    def set(self, key_path: str, value: Any):
        """
        Set a configuration value using dot notation.
        
        Args:
            key_path: Dot-separated path (e.g., 'window.width')
            value: Value to set
        """
        keys = key_path.split('.')
        config = self.config
        
        for key in keys[:-1]:
            if key not in config:
                config[key] = {}
            config = config[key]
            
        config[keys[-1]] = value
        
    def get_theme(self) -> str:
        """Get current theme."""
        return self.get('theme', 'light')
        
    def set_theme(self, theme: str):
        """Set current theme."""
        self.set('theme', theme)
        
    def get_window_geometry(self) -> Dict[str, int]:
        """Get window geometry."""
        return {
            'width': self.get('window.width', 1200),
            'height': self.get('window.height', 800),
            'x': self.get('window.x'),
            'y': self.get('window.y')
        }
        
    def set_window_geometry(self, width: int, height: int, x: Optional[int] = None, y: Optional[int] = None):
        """Set window geometry."""
        self.set('window.width', width)
        self.set('window.height', height)
        if x is not None:
            self.set('window.x', x)
        if y is not None:
            self.set('window.y', y)
            
    def get_last_path(self, path_type: str) -> str:
        """Get last used path."""
        return self.get(f'last_paths.{path_type}', '')
        
    def set_last_path(self, path_type: str, path: str):
        """Set last used path."""
        self.set(f'last_paths.{path_type}', path)
        
    def get_defaults(self) -> Dict[str, Any]:
        """Get default compression settings."""
        return self.get('defaults', {})
        
    def set_defaults(self, **kwargs):
        """Set default compression settings."""
        for key, value in kwargs.items():
            self.set(f'defaults.{key}', value)
            
    def add_recent_task(self, task_info: Dict[str, Any]):
        """
        Add a task to recent tasks history.
        
        Args:
            task_info: Dictionary with task information
        """
        recent = self.get('recent_tasks', [])
        
        # Add timestamp
        from datetime import datetime
        task_info['timestamp'] = datetime.now().isoformat()
        
        # Add to beginning of list
        recent.insert(0, task_info)
        
        # Keep only last 50 tasks
        self.set('recent_tasks', recent[:50])
        
    def get_recent_tasks(self, limit: int = 10) -> list:
        """Get recent tasks."""
        return self.get('recent_tasks', [])[:limit]
        
    def clear_recent_tasks(self):
        """Clear recent tasks history."""
        self.set('recent_tasks', [])


# Global config instance
_config_instance = None


def get_config() -> ConfigManager:
    """Get the global configuration instance."""
    global _config_instance
    if _config_instance is None:
        _config_instance = ConfigManager()
    return _config_instance


def save_config():
    """Save the global configuration."""
    config = get_config()
    config.save()

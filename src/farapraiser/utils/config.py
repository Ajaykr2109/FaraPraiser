"""Configuration management for FaraPraiser."""

import json
import os
from pathlib import Path
from typing import Dict, Any


class Config:
    """Application configuration manager."""
    
    DEFAULT_CONFIG = {
        "llm": {
            "provider": "ollama",  # or "lmstudio"
            "ollama_url": "http://localhost:11434",
            "lmstudio_url": "http://localhost:1234/v1",
            "model": "auto",  # auto-detect based on hardware
            "timeout": 60,
            "max_tokens": 1024,
        },
        "ui": {
            "theme": "light",
            "font_size": 11,
            "max_variants": 5,
        },
        "export": {
            "default_format": "docx",
            "include_metadata": True,
        },
        "tones": [
            "formal",
            "academic",
            "casual",
            "technical",
            "simplified",
        ],
    }
    
    def __init__(self):
        """Initialize configuration."""
        self.config_dir = Path.home() / ".farapraiser"
        self.config_file = self.config_dir / "config.json"
        self.config = self._load_config()
    
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from file or use defaults."""
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    user_config = json.load(f)
                    # Merge with defaults
                    config = self.DEFAULT_CONFIG.copy()
                    self._deep_update(config, user_config)
                    return config
            except Exception as e:
                print(f"Error loading config: {e}. Using defaults.")
        return self.DEFAULT_CONFIG.copy()
    
    def _deep_update(self, base: Dict, update: Dict) -> None:
        """Recursively update nested dictionaries."""
        for key, value in update.items():
            if isinstance(value, dict) and key in base and isinstance(base[key], dict):
                self._deep_update(base[key], value)
            else:
                base[key] = value
    
    def save(self) -> None:
        """Save configuration to file."""
        try:
            self.config_dir.mkdir(parents=True, exist_ok=True)
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=2)
        except Exception as e:
            print(f"Error saving config: {e}")
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value by dot-separated key."""
        keys = key.split('.')
        value = self.config
        for k in keys:
            if isinstance(value, dict):
                value = value.get(k, default)
            else:
                return default
        return value
    
    def set(self, key: str, value: Any) -> None:
        """Set configuration value by dot-separated key."""
        keys = key.split('.')
        config = self.config
        for k in keys[:-1]:
            if k not in config or not isinstance(config[k], dict):
                config[k] = {}
            config = config[k]
        config[keys[-1]] = value
        self.save()

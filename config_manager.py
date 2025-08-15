import json
import os
from typing import Dict, Any

class ConfigManager:
    def __init__(self):
        self.config_file = os.path.join(os.path.dirname(__file__), 'config.json')
        self.default_config = {
            'enabled': False,
            'hotkey': 'ctrl+shift+u',
            'overlay_position': 'top-right',
            'overlay_duration': 2.0,
            'smiley': False,
            'yu': False, 
            'stutter': False,
            'nouwu': False
        }
        self.config = self.load_config()
    
    def load_config(self) -> Dict[str, Any]:
        """Load configuration from file or create default"""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as f:
                    config = json.load(f)
                # Merge with default config to handle missing keys
                merged_config = self.default_config.copy()
                merged_config.update(config)
                return merged_config
            except (json.JSONDecodeError, IOError):
                return self.default_config.copy()
        return self.default_config.copy()
    
    def save_config(self):
        """Save current configuration to file"""
        try:
            with open(self.config_file, 'w') as f:
                json.dump(self.config, f, indent=2)
        except IOError:
            pass  # Fail silently
    
    def get(self, key: str, default=None):
        """Get configuration value"""
        return self.config.get(key, default)
    
    def set(self, key: str, value: Any):
        """Set configuration value and save"""
        self.config[key] = value
        self.save_config()
    
    def is_enabled(self) -> bool:
        """Check if uwuifier is enabled"""
        return self.config.get('enabled', False)
    
    def toggle_enabled(self) -> bool:
        """Toggle enabled state and return new state"""
        new_state = not self.is_enabled()
        self.set('enabled', new_state)
        return new_state

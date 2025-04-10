import os
import yaml
from typing import Dict, Any, Optional


class ConfigManager:
    """
    Configuration Manager for the Cryptocurrency QA Framework.
    
    This class is responsible for loading and managing configuration settings
    from YAML files. It supports environment-specific configurations and
    provides a centralized access point for all configuration parameters.
    """
    
    def __init__(self, config_path: str = None):
        """
        Initialize the ConfigManager with the specified configuration file.
        
        Args:
            config_path: Path to the configuration file. If None, uses the default path.
        """
        if config_path is None:
            # Get the directory of the current file
            current_dir = os.path.dirname(os.path.abspath(__file__))
            # Go up one level to the project root
            project_root = os.path.dirname(current_dir)
            # Default config path
            config_path = os.path.join(project_root, 'config', 'default.yaml')
        
        self.config_path = config_path
        self.config = self._load_config()
    
    def _load_config(self) -> Dict[str, Any]:
        """
        Load configuration from the YAML file.
        
        Returns:
            Dict containing configuration parameters.
        """
        try:
            with open(self.config_path, 'r') as file:
                config = yaml.safe_load(file)
            return config
        except Exception as e:
            print(f"Error loading configuration: {e}")
            return {}
    
    def get_api_config(self) -> Dict[str, Any]:
        """
        Get API-specific configuration.
        
        Returns:
            Dict containing API configuration parameters.
        """
        return self.config.get('api', {})
    
    def get_web_config(self) -> Dict[str, Any]:
        """
        Get Web UI testing specific configuration.
        
        Returns:
            Dict containing Web UI configuration parameters.
        """
        return self.config.get('web', {})
    
    def get_performance_config(self) -> Dict[str, Any]:
        """
        Get performance testing specific configuration.
        
        Returns:
            Dict containing performance testing configuration parameters.
        """
        return self.config.get('performance', {})
    
    def get_value(self, key: str, default: Any = None) -> Any:
        """
        Get a specific configuration value by key.
        
        Args:
            key: The configuration key to retrieve.
            default: Default value to return if key is not found.
            
        Returns:
            The configuration value or default if not found.
        """
        keys = key.split('.')
        value = self.config
        
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        
        return value
    
    def update_config(self, key: str, value: Any) -> None:
        """
        Update a configuration value.
        
        Args:
            key: The configuration key to update.
            value: The new value.
        """
        keys = key.split('.')
        config = self.config
        
        # Navigate to the nested dictionary
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]
        
        # Update the value
        config[keys[-1]] = value

import json
import os

class ConfigHandler:
    def __init__(self, config_file="Blocker/data/config.json"):
        self.config_file = config_file
        self.default_config = {
            "upstream_dns": {
                "name": "Google",
                "address": "8.8.8.8"
            },
            "custom_dns": "",
            "whitelist": [],
            "blacklist": [],
            "auto_update": False
        }
        self.config = self.load_config()

    def load_config(self):
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as f:
                    config = json.load(f)
                    print(f"Loaded configuration: {config}")
                    return config
            except Exception as e:
                print(f"Error loading configuration: {e}")
                return self.default_config.copy()  
        else:
            print("Configuration file not found. Creating a new one with default values.")
            self.config = self.default_config.copy()  
            self.save_config()  
            return self.config  # Return default config

    def save_config(self):
        try:
            os.makedirs(os.path.dirname(self.config_file), exist_ok=True)
            with open(self.config_file, 'w') as f:
                json.dump(self.config, f, indent=4)
            print(f"Configuration saved: {self.config}")
        except Exception as e:
            print(f"Error saving configuration: {e}")


    def update_config(self, key, value):
        if key in self.config:
            self.config[key] = value
        elif key == "auto_update":
            self.config["auto_update"] = value
        elif key == "custom_dns":
            self.config["custom_dns"] = value
        else:
            print(f"Invalid configuration key: {key}")
        self.save_config()


    def update_upstream_dns(self, name, address):
        self.config["upstream_dns"] = {"name": name, "address": address}
        self.save_config()

    def add_to_list(self, key, value):
        if key in ["whitelist", "blacklist"] and value not in self.config[key]:
            self.config[key].append(value)
            self.save_config()

    def remove_from_list(self, key, value):
        if key in ["whitelist", "blacklist"] and value in self.config[key]:
            self.config[key].remove(value)
            self.save_config()

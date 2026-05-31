from src.core.config import read_config

def open_tools():
    config = read_config()
    if config.get("is_on_tools", True):
        print("Tools are enabled. You can access them with 'zap tools'.")
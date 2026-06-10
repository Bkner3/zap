from os import makedirs
from os.path import join
from src.utils.sys_utils import get_user_path

class PathManager:
    _paths = {}
    _initialized = False

    @classmethod
    def setup(cls, root):
        """Initializes the paths and creates the folders. Should only be called once."""
        if cls._initialized:
            return

        user_root = get_user_path()

        cls._paths = {
            # USER DATA
            "bin": join(user_root, "bin"),
            "data": join(user_root, "data"),
            "sl": join(user_root, "sl"),

            # FILES (user)
            "installed_file": join(user_root, "data", "installed.json"),
            "config_file": join(user_root, "data", "config.json"),
            "log_file": join(user_root, "data", "zap.log"),

            # ROOT (runtime)
            "root": root,
            "core": join(root, "zapp", "core"),
            "ext": join(root, "zapp", "ext"),
            "download": join(root, "zapp", "down"),
            "tmp": join(root, "zapp", "tmp"),

            # Files (runtime)
            "repos_file": join(root, "zapp", "repos.json"),
            "tmp_packages": join(root, "zapp", "tmp", "Packages_tmp.json")
        }

        # Creates folders automatically (directories only, not files)
        for key, path in cls._paths.items():
            if not path.endswith(".json") and not path.endswith(".log"):
                makedirs(path, exist_ok=True)
        
        cls._initialized = True

    @classmethod
    def get(cls, key):
        """Returns a specific path without needing the root variable."""
        if not cls._initialized:
            raise ValueError("The PathManager has not been initialized! Call PathManager.setup(root) at the beginning of the program.")
        if key not in cls._paths:
            raise KeyError(f"The path '{key}' does not exist in the PathManager.")
            
        return cls._paths[key]
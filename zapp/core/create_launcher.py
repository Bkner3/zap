from platform import system
import os

def create_launcher(name, executable_path, sl_path):
    if system() == "Windows":
        bat_file = os.path.join(sl_path, f"{name}.bat")
        with open(bat_file, "w") as f:
            f.write(f'@"{executable_path}" %*')
    
    elif system() == "Linux":
        link = os.path.join(sl_path, name)
        if os.path.exists(link):
            os.remove(link)
        os.symlink(executable_path, link)
        os.chmod(executable_path, 0o755)
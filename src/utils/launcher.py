from platform import system
from src.utils.write_logs import log_info, log_warning
import os

def create_launcher(name, executable_path, symlinks_path):
    if system() == "Windows":
        bat_file = os.path.join(symlinks_path, f"{name}.bat")
        with open(bat_file, "w") as f:
            f.write(f'@"{executable_path}" %*')
        log_info(f"Writing the log: {bat_file}")
    elif system() == "Linux":
        link = os.path.join(symlinks_path, name)
        
        # lexists detects even broken symbolic links
        if os.path.lexists(link):
            log_info("Removing a broken link.")
            os.remove(link)

        log_info(f"Creating a symbolic link {link}")    
        os.symlink(executable_path, link)
        
        # Tries to set execution permissions, but won't crash if it fails
        try:
            os.chmod(executable_path, 0o755)
        except PermissionError:
            print(f"Warning: Could not change permissions for {executable_path}")
            log_warning(f"Warning: Could not change permissions for {executable_path}")

def remove_launcher(name, symlinks_path, system):
    
    #Removes only the package launcher/shortcut based on the system.

    launcher_path = (
        os.path.join(symlinks_path, f"{name}.bat")
        if system == "Windows"
        else os.path.join(symlinks_path, name)
    )

    if system == "Windows":
        if os.path.exists(launcher_path):
            os.remove(launcher_path)
            log_info(f"Removing the symlink named: {name}")
        else:
            print(f"Launcher not found: {name}.bat")
            log_warning(f"Launcher not found: {name}.bat")

    elif system == "Linux":
        if os.path.lexists(launcher_path):
            os.remove(launcher_path)
            log_info(f"Removing the symlink named: {name}")
        else:
            print(f"Symlink not found: {name}")
            log_warning(f"Symlink not found: {name}")
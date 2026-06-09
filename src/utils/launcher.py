from platform import system
import os

def create_launcher(name, executable_path, symlinks_path):
    if system() == "Windows":
        bat_file = os.path.join(symlinks_path, f"{name}.bat")
        with open(bat_file, "w") as f:
            f.write(f'@"{executable_path}" %*')
    
    elif system() == "Linux":
        link = os.path.join(symlinks_path, name)
        
        # lexists detects even broken symbolic links
        if os.path.lexists(link):
            os.remove(link)
            
        os.symlink(executable_path, link)
        
        # Tries to set execution permissions, but won't crash if it fails
        try:
            os.chmod(executable_path, 0o755)
        except PermissionError:
            print(f"Warning: Could not change permissions for {executable_path}")

def remove_launcher(name, symlinks_path, system):
    """
    Removes only the package launcher/shortcut based on the system.
    """
    launcher_path = (
        os.path.join(symlinks_path, f"{name}.bat")
        if system == "Windows"
        else os.path.join(symlinks_path, name)
    )

    if system == "Windows":
        if os.path.exists(launcher_path):
            os.remove(launcher_path)
        else:
            print(f"Launcher not found: {name}.bat")

    elif system == "Linux":
        if os.path.lexists(launcher_path):
            os.remove(launcher_path)
        else:
            print(f"Symlink not found: {name}")
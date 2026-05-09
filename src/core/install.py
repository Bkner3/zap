from src.core.downloader import only_download
from src.utils.move_files import move_files
from src.utils.create_launcher import create_launcher
from src.utils.zip_utils import extract_zip
from src.zap_path import PathManager
from os import listdir, makedirs, path, remove

def install(packages):
    only_download(packages)
    ext_path = PathManager.get("ext")
    bin_path = PathManager.get("bin")
    symlinks_path = PathManager.get("sl")

    for file in listdir(ext_path):
        print(f"Installing {file}...")
        pfile = path.join(ext_path, file)
        name = path.splitext(file)[0]

        final_folder = path.join(bin_path, name)
        final_file = path.join(final_folder, file)

        if not path.exists(final_folder):
            makedirs(final_folder)

        move_files(pfile, final_folder)
        extract_zip(final_file, final_folder)
        print(f"Extracted {name}.")
        remove(final_file)
        
        executable = path.join(final_folder, f"{name}.exe")
        create_launcher(name, executable, symlinks_path)
        print(f"Created launcher for {name}.")
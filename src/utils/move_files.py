from os import path, makedirs
from shutil import move

def move_files(origin, destination):
    if not path.exists(destination):
        makedirs(destination)
    move(origin, path.join(destination, path.basename(origin)))
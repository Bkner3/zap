from os import makedirs
from zipfile import ZipFile

def extract_zip(file_to_extract, path_to_extract):
    makedirs(path_to_extract, exist_ok=True)
    with ZipFile(file_to_extract, 'r') as zip_ref:
        zip_ref.extractall(path_to_extract)
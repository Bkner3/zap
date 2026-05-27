from os import makedirs
from zipfile import ZipFile
from tqdm import tqdm


def extract_zip(file_to_extract, path_to_extract):
    makedirs(path_to_extract, exist_ok=True)

    with ZipFile(file_to_extract, 'r') as zip_ref:
        files = zip_ref.infolist()

        with tqdm(total=len(files), desc="Extracting", ascii=" ━",  unit="B", ncols=100, colour="white") as pbar:
            for file in files:
                zip_ref.extract(file, path_to_extract)
                pbar.update(1)
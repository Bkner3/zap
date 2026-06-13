from os import makedirs
from zipfile import ZipFile
from tqdm import tqdm
from src.utils.write_logs import log_info

def extract_zip(file_to_extract, path_to_extract):
    makedirs(path_to_extract, exist_ok=True)
    log_info(f"File to extract: {file_to_extract}; Path to extract: {path_to_extract} ")
    
    with ZipFile(file_to_extract, 'r') as zip_ref:
        files = zip_ref.infolist()

        with tqdm(total=len(files), desc="Extracting", ascii=" ━", unit_scale=True,  unit="B", ncols=100, colour="white", bar_format="{desc} {percentage:3.0f}% |{bar}| {n_fmt}/{total_fmt} @ {rate_fmt}",) as pbar:
            for file in files:
                zip_ref.extract(file, path_to_extract)
                pbar.update(1)
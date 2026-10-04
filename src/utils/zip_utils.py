from os import makedirs
from zipfile import ZipFile, BadZipFile
from tqdm import tqdm

from src.utils.write_logs import log_info, log_error


def extract_zip(file_to_extract, path_to_extract):
    makedirs(path_to_extract, exist_ok=True)

    log_info(f"File to extract: {file_to_extract}; " f"Path to extract: {path_to_extract}")

    try:
        with ZipFile(file_to_extract, "r") as zip_ref:
            files = zip_ref.infolist()

            with tqdm(total=len(files), desc="Extracting", ascii=" ━", unit="B", unit_scale=True, ncols=100, colour="white", bar_format="{desc} {percentage:3.0f}% |{bar}| ""{n_fmt}/{total_fmt} @ {rate_fmt}",) as pbar:

                for file in files:
                    zip_ref.extract(file, path_to_extract)
                    pbar.update(1)

        log_info(f"Successfully extracted {file_to_extract}")
        return True

    except FileNotFoundError:
        log_error(f"ZIP file not found: {file_to_extract}")
        return False

    except BadZipFile:
        log_error(f"Invalid or corrupted ZIP file: {file_to_extract}")
        return False

    except Exception as error:
        log_error(f"Error extracting {file_to_extract}: {error}")
        return False
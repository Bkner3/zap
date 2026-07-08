from threading import Thread
from shutil import move
from pathlib import Path

import os
import sys
import requests

from tqdm import tqdm
from colorama import Fore, Style

from src.zap_path import PathManager
from src.utils.json_utils import read_json
from src.utils.zip_utils import extract_zip
from src.core.search import search_repo_packages
from src.utils.write_logs import log_info, log_debug, log_error, log_warning
import hashlib

CHUNK_SIZE = 4096


def get_context():
    log_info("Setting and returning the download context.")
    return {
        "repos": read_json(PathManager.get("repos_file")).get("repos", []),
        "ext": PathManager.get("ext"),
        "download": PathManager.get("download"),
        "tmp": PathManager.get("tmp"),
        "tmp_packages": PathManager.get("tmp_packages"),
    }


def download(url, output_name, file_type, cfg):
    base_dir = cfg["download"] if file_type == "Index" else cfg["ext"]
    output_path = os.path.join(base_dir, output_name)
    headers = {"User-Agent": "ZAP-PackageManager"}
    
    try:
        with requests.get(url, stream=True, headers=headers) as response:
            if response.status_code != 200:
                if file_type != "Index":
                    log_error(f"Failed to download: {url}")
                    print(Fore.RED + f"Failed to download: {url}")
                return None

            log_info(f"Output Directory: {output_path}")
            total = int(response.headers.get("content-length", 0))
            
            with open(output_path, "wb") as file, tqdm(
                total=total if total > 0 else None,
                unit="B",
                unit_scale=True,
                desc=output_name,
                ncols=100,
                ascii=" ━",
                colour="white",
                bar_format="{desc} {percentage:3.0f}% |{bar}| {n_fmt}/{total_fmt} @ {rate_fmt}",
            ) as progress:

                for chunk in response.iter_content(CHUNK_SIZE):
                    if not chunk:
                        continue
                    file.write(chunk)
                    progress.update(len(chunk))

            content_type = response.headers.get("Content-Type", "")
            if "application/json" in content_type:
                log_info(f"Processing downloaded file as API/JSON: {output_path}")
                return read_json(output_path)
                    
        log_info(f"This url ({url}) was downloaded")
        return output_path

    except requests.RequestException:
        print(Fore.RED + f"Error downloading: {url}")
        return None


def download_index(cfg):
    log_info("Starting repository index update")
    print(Style.BRIGHT + Fore.BLUE + "Starting repository index update")

    repos = cfg["repos"]
    tmp_path = cfg["tmp"]

    if not repos:
        log_warning("No repositories configured.")
        print(Fore.YELLOW + "No repositories configured.")
        return

    for repo_url in repos:
        repo_name = (
            repo_url.replace("http://", "")
            .replace("https://", "")
            .rstrip("/")
        )

        index_url = f"{repo_url.rstrip('/')}/index.zip"
        log_info(f"Updating: {index_url}")
        print(f"\nUpdating: {index_url}")

        zip_path = download(
            index_url,
            f"{repo_name}.zip",
            "Index",
            cfg
        )
        log_debug(f"Index zip path: {zip_path}")

        if not zip_path:
            log_warning("Skipping repository: {repo_url}")
            print(Fore.YELLOW + f"Skipping repository: {repo_url}")
            continue

        extract_zip(zip_path, tmp_path)
        log_info(f"Removing: {zip_path}")
        os.remove(zip_path)

        index_file = os.path.join(tmp_path, "index.json")
        
        if not os.path.exists(index_file):
            continue

        data = read_json(index_file)
        log_info(f"Reading a repo name")
        final_name = f"{data.get('repo', 'unknown')}.json"
        final_path = os.path.join(tmp_path, final_name)

        if os.path.exists(final_path):
            os.remove(final_path)

        os.rename(index_file, final_path)
        log_info(f"Renaming {index_file} to {final_path}")


def only_download(packages, process):
    cfg = get_context()
    if process == "update":
        pass
    else:
        download_index(cfg)

    data = search_repo_packages(packages)
    packages_to_download = data.get("packages", [])
    missing = data.get("missing", [])
    notsupported = data.get("os_notsupported", [])

    if not packages_to_download:
 
        print(Fore.YELLOW + "No packages found.")
        log_warning("No packages found.")
        return {"downloaded": [], "failed": packages, "missing": missing}

    threads = []
    downloaded = []
    failed = []
    print(Style.BRIGHT + Fore.BLUE + "\nStarting package download\n")
    log_info("Starting package download.")

    for package in packages_to_download:
        url = package["url"]

        name = package["name"]
        expected_hash = package["hash"]
        
        log_info(f"Name: {name}, URL: {url}")

        extension = Path(url).suffix
        output_name = f"{name}{extension}"

        thread = Thread(
            target=download_worker,
            args=(url, output_name, cfg, downloaded, failed, name, expected_hash)
        )

        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()
    
    log_info(f"Downloaded:{downloaded}, Failed: {failed}, Missing: {missing}")
    return {
        "downloaded": downloaded,
        "failed": failed,
        "missing": missing,
        "os_notsupported": notsupported 
    }


def download_to(packages, destination):

    cfg = get_context()

    ext_path = cfg["ext"]

    before = set(os.listdir(ext_path))

    only_download(packages, "package")

    after = set(os.listdir(ext_path))

    new_files = after - before

    for file_name in new_files:
        source = os.path.join(ext_path, file_name)
        target = os.path.join(destination, file_name)
        log_info(f"Moving: {source} to {target}")        
        move(source, target)


def download_worker(url, output_name, cfg, downloaded, failed, name, expected_hash):
    result = download(url, output_name, "package", cfg)
    log_info(f"Checking the integrity of {result}")
    if result and os.path.exists(result):
        with open(result, "rb") as f:
            download_file_hash = hashlib.sha256(f.read()).hexdigest().upper()

        if download_file_hash == expected_hash.upper():
            log_info(f"The {name} hash matched.")
            downloaded.append(name)
        else:
            log_error(f"SHA256 mismatch! Removing {result}")
            print(f"{Fore.RED + Style.BRIGHT}SHA256 mismatch! Removing {result}")
            failed.append(name)
            os.remove(result)
    else:
        failed.append(name)
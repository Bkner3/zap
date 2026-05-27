from threading import Thread
from shutil import move
from pathlib import Path

import os
import requests

from tqdm import tqdm
from colorama import Fore, Style

from src.zap_path import PathManager
from src.utils.json_utils import read_json
from src.utils.zip_utils import extract_zip
from src.core.search import search_repo_packages


CHUNK_SIZE = 4096


def get_context():
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

    with requests.get(url, stream=True) as response:
        if response.status_code != 200:
            if file_type != "Index":
                print(Fore.RED + f"Failed to download: {url}")
            return None

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

    return output_path


def download_index(cfg):
    print(Style.BRIGHT + Fore.BLUE + "Starting repository index update\n")

    repos = cfg["repos"]
    tmp_path = cfg["tmp"]

    if not repos:
        print(Fore.YELLOW + "No repositories configured.")
        return

    for repo_url in repos:
        repo_name = (
            repo_url.replace("http://", "")
            .replace("https://", "")
            .rstrip("/")
        )

        index_url = f"{repo_url.rstrip('/')}/index.zip"

        print(f"\nUpdating: {index_url}")

        zip_path = download(
            index_url,
            f"{repo_name}.zip",
            "Index",
            cfg
        )

        if not zip_path:
            print(Fore.YELLOW + f"Skipping repository: {repo_url}")
            continue

        extract_zip(zip_path, tmp_path)
        os.remove(zip_path)

        index_file = os.path.join(tmp_path, "index.json")

        if not os.path.exists(index_file):
            continue

        data = read_json(index_file)

        final_name = f"{data.get('repo', 'unknown')}.json"
        final_path = os.path.join(tmp_path, final_name)

        if os.path.exists(final_path):
            os.remove(final_path)

        os.rename(index_file, final_path)


def only_download(packages):
    cfg = get_context()

    download_index(cfg)
    print()

    search_repo_packages(packages)

    packages_file = cfg["tmp_packages"]

    if not os.path.exists(packages_file):
        print(Fore.YELLOW + "No packages found.")
        return

    data = read_json(packages_file)
    packages_to_download = data.get("packages", [])

    if not packages_to_download:
        print(Fore.YELLOW + "No packages found.")
        return

    threads = []

    for package in packages_to_download:
        url = package["url"]
        name = package["name"]

        extension = Path(url).suffix
        output_name = f"{name}{extension}"

        thread = Thread(
            target=download,
            args=(url, output_name, "Package", cfg)
        )

        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()


def download_to(packages, destination):
    cfg = get_context()

    ext_path = cfg["ext"]

    before = set(os.listdir(ext_path))

    only_download(packages)

    after = set(os.listdir(ext_path))

    new_files = after - before

    for file_name in new_files:
        source = os.path.join(ext_path, file_name)
        target = os.path.join(destination, file_name)

        move(source, target)
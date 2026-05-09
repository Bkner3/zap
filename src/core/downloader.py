from src.zap_path import PathManager
from src.utils.json_utils import read_json
from src.utils.zip_utils import extract_zip
from src.core.search import search_repo_packages
import os
import requests
from tqdm import tqdm
from colorama import Fore, Style
from threading import Thread
from shutil import move


def get_context():
    return {
        "repos": read_json(PathManager.get("repos_file")).get("repos"),
        "ext": PathManager.get("ext"),
        "download": PathManager.get("download"),
        "tmp": PathManager.get("tmp"),
        "tmp_packages": PathManager.get("tmp_packages")
    }


def download(url, output_name, file_type, cfg):

    base_path = cfg["ext"]
    download_path = cfg["download"]

    output = os.path.join(base_path, output_name)

    if file_type == "Index":
        output = os.path.join(download_path, output_name)

    try:
        r = requests.get(url, stream=True)
        r.raise_for_status()

    except requests.exceptions.ConnectionError:
        if file_type != "Index":
            print(Fore.RED + f"Error: could not connect to {url}")
        return None

    except requests.exceptions.HTTPError as e:
        if file_type != "Index":
            print(Fore.RED + f"Error: {e}")
        return None

    except requests.RequestException as e:
        if file_type != "Index":
            print(Fore.RED + f"Error downloading {url}: {e}")
        return None

    total = int(r.headers.get("content-length", 0))

    with open(output, "wb") as f, tqdm(
        total=total if total > 0 else None,
        unit="B",
        unit_scale=True,
        desc=output_name,
        bar_format="{desc} {percentage:3.0f}% |{bar}| {n_fmt}/{total_fmt} @ {rate_fmt}",
        ncols=100,
        colour="white",
        ascii=" ━"
    ) as bar:

        for chunk in r.iter_content(4096):
            if chunk:
                f.write(chunk)
                bar.update(len(chunk))

    return output


def download_index(cfg):
    print(Style.BRIGHT + Fore.BLUE + "Starting to download repositories index\n")

    repos = cfg["repos"]
    tmp_path = cfg["tmp"]

    for url in repos:
        name = url.replace("http://", "").replace("https://", "").rstrip("/")
        index_url = url.rstrip("/") + "/index.zip"

        print(f"Updating: {index_url}")

        temp_zip = download(index_url, f"{name}.zip", "Index", cfg)

        if not temp_zip:
            print(Fore.YELLOW + f"Repository {url} is not available, jumping to next one.")
            continue

        extract_zip(temp_zip, tmp_path)
        os.remove(temp_zip)

        index_file = os.path.join(tmp_path, "index.json")

        data = read_json(index_file)

        final_path = os.path.join(tmp_path, f"{data.get('repo', 'unknown')}.json")

        if os.path.exists(final_path):
            os.remove(final_path)

        os.rename(index_file, final_path)


def only_download(packages):
    cfg = get_context()

    download_index(cfg)
    print()

    search_repo_packages(packages)

    tmp_packages_file = cfg["tmp_packages"]

    if not os.path.exists(tmp_packages_file):
        print(Fore.YELLOW + "No packages found to download.")
        return

    data = read_json(tmp_packages_file)
    packages_to_download = data.get("packages", [])

    if not packages_to_download:
        print(Fore.YELLOW + "No packages found to download.")
        return

    threads = []

    for pkg in packages_to_download:
        url = pkg["url"]
        name = pkg["name"]

        ext = os.path.splitext(url)[1]
        output_name = f"{name}{ext}"

        t = Thread(target=download, args=(url, output_name, "Package", cfg))
        t.start()
        threads.append(t)

    for t in threads:
        t.join()


def download_to(packages, destination):
    cfg = get_context()
    ext_path = cfg["ext"]
    only_download(packages)
    for file in os.listdir(ext_path):
        move(os.path.join(ext_path, file), os.path.join(destination, file))
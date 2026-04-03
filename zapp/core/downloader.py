import requests
import tqdm
from colorama import Fore

def download(url, output_name, type, ext_path, download_path):
    output = f"{ext_path}/{output_name}"
    if type == "Index":
        output = f"{download_path}/{output_name}"

    try:
        r = requests.get(url, stream=True)
        r.raise_for_status()
    except requests.exceptions.ConnectionError:
        if not type == "Index":
            print(Fore.RED + f"Error: could not connect to {url}")
        return None
    except requests.exceptions.HTTPError as e:
        if not type == "Index":
            print(Fore.RED + f"Error: {e}")
        return None
    except requests.RequestException as e:
        if not type == "Index":
            print(Fore.RED + f"Error downloading {url}: {e}")
        return None

    total = int(r.headers.get("content-length", 0))

    with open(output, "wb") as f, tqdm.tqdm(total=total if total > 0 else None, unit="B", unit_scale=True, desc=output_name, bar_format="{desc}: {percentage:3.0f}%|{bar}| {n_fmt}/{total_fmt} {rate_fmt}", ncols=100) as bar:
        for chunk in r.iter_content(8192):
            if chunk:
                f.write(chunk)
                bar.update(len(chunk))

    return output
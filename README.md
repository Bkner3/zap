  # ZAP — Zippy Asset Packager

```
███████╗ █████╗ ██████╗
╚══███╔╝██╔══██╗██╔══██╗
  ███╔╝ ███████║██████╔╝
 ███╔╝  ██╔══██║██╔═══╝
███████╗██║  ██║██║
╚══════╝╚═╝  ╚═╝╚═╝ PM
```

### A lightweight command-line package manager written in Python.

---

## Requirements

- Python 3.x
- pip packages:
  - `requests`
  - `tqdm`
  - `colorama`

Install dependencies:
```bash
pip install requests tqdm colorama
```

---

## Usage

```bash
zap <command> [package]
```

---

## Commands

| Command      | Description                              ||
|--------------|------------------------------------------|--------------------|
| `install`    | Install a package                        |    Implemented     |
| `remove`     | Remove a package                         |    Implemented     |
| `download`   | Download a package without installing    |    Implemented     |
| `update`     | Update a specific package                | Not implemented yet|
| `update-all` | Update all installed packages            | Not implemented yet|
| `list`       | List all installed packages              |    Implemented     |
| `info`       | Show detailed information about a package| Not implemented yet|
| `help`       | Show this help message                   |    Implemented     |

---

## Directory Structure

```
zapp/
├── down/       # The download directory
├── ext/        # Used for logic 
└── tmp/        # Temporary files and package index cache

~/.zap/         # (Linux)
C:\Users\<user>\AppData\Local\Zap\   # (Windows)
├── bin/        # Installed packages
└── data/       # User data
```

---

## Configuration

Repositories are defined in `zapp/repos.json`:

```json
{
  "repos": [
    "http://localhost:8000"
  ]
}
```

---

## How It Works

1. **Update** — Downloads `index.zip` from each repository and extracts the package list
2. **Search** — Looks up the requested package name in the index and writes the URL to `Packages.tmp`
3. **Download** — Downloads the `.zip` file from the URL (multithreaded)
4. **Install** — Moves the zip to the final folder, extracts it, and removes the zip

---

##  Supported Systems

| OS      | Supported |
|---------|-----------|
| Windows | YES       |
| Linux   | YES       |
| macOS   | NO        |

---

## Roadmap

- [x] Install
- [x] Download
- [x] List
- [x] Remove
- [ ] Search
- [ ] Update
- [ ] Update-all
- [ ] Package metadata (info)
- [ ] Dependency resolution
- [ ] Install scripts

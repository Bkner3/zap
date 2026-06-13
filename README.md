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

| Command    | Description                               |                     |
| ---------- | ----------------------------------------- | ------------------- |
| `install`  | Install a package                         | Implemented         |
| `remove`   | Remove a package                          | Implemented         |
| `download` | Download a package without installing     | Implemented         |
| `update`   | Update a specific package                 | Not implemented yet |
| `list`     | List all installed packages               | Implemented         |
| `info`     | Show detailed information about a package | Not implemented yet |
| `help`     | Show this help message                    | Implemented         |

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
  "repos": ["http://localhost:8000"]
}
```

# Create a repositoriy

```
Server Structure:

The server must make the files available directly over HTTP:

http://example-server.com/

├── index.zip
├── package1.zip
└── package2.zip

The index.zip must be in the root of the repository.
```

## Index.zip structure:

```

The index.zip must have a index.json.

index.zip
└── index.json
```

## Index.json Structure

```

Example of a index:

{
  "repo": "repo-example",
  "updated": "2026-03-14",
  "packages": [
    {
      "name": "package1",
      "version": "1.0.0",
      "description": "package1 description",
      "url": "http://example-server.com/package1.zip",
      "system": "windows",
      "hash": ""
    },
    {
      "name": "package2",
      "version": "1.0.0",
      "description": "package2 description",
      "url": "http://example-server.com/package2.zip",
      "system": "windows",
      "hash": ""
    }
  ]
}
```

## Fields:

| Fields   | Description            |
| -------- | ---------------------- |
| repo     | Name of the repository |
| packages | List of Available      |
| name     | Name of the package    |
| url      | Url of the package     |

## How Zap Works

1. **Update** — Downloads `index.zip` from each repository and extracts the package list
2. **Search** — Looks up the requested package name in the index and return the url
3. **Download** — Downloads the `.zip` file from the URL (multithreaded)
4. **Install** — Moves the zip to the final folder, extracts it, and removes the zip

---

## Supported Systems

| OS      | Supported |
| ------- | --------- |
| Windows | YES       |
| Linux   | YES       |
| macOS   | NO        |

---

## Roadmap

- [x] Install
- [x] Download
- [x] List
- [x] Remove
- [ ] Update
- [ ] Update-all
- [ ] Package metadata (info)
- [ ] Dependency resolution
- [ ] Install scripts

# ZAP — Zippy Asset Packager

```text
███████╗ █████╗ ██████╗
╚══███╔╝██╔══██╗██╔══██╗
  ███╔╝ ███████║██████╔╝
 ███╔╝  ██╔══██║██╔═══╝
███████╗██║  ██║██║
╚══════╝╚═╝  ╚═╝╚═╝ PM
```

A lightweight command-line package manager written in Python.

[Official Repository](https://bkner3.github.io/zap-repository/)

> **Official Repository URL:** > `https://bkner3.github.io/zap-repository/`

---

> **Current Status**
>
> ZAP is under active development.
> Windows is fully supported.
> Linux support is experimental.
> Package dependency resolution has not been implemented yet.

---

# Features

- Install packages
- Remove packages
- Download packages without installing
- Update installed packages
- Upgrade installed packages
- List installed packages
- Automatic launcher creation
- SHA-256 package verification before installation
- HTTP-based repositories
- Multi-threaded downloads
- Self-update from GitHub releases

---

# Requirements

- Python 3.10 or later
- pip

Required Python packages:

- requests
- tqdm
- colorama

Install them with:

```bash
pip install requests tqdm colorama
```

---

# Getting Started

## Windows Installation

You can install ZAP automatically by running the PowerShell installation script:

```powershell
irm https://raw.githubusercontent.com/Bkner3/zap/refs/heads/main/setup/install.ps1 | iex
```

Or install it manually by cloning the repository:

```bash
git clone https://github.com/Bkner3/zap
cd ZAP
pip install -r requirements.txt
```

> **Warning**
> If you don't use the installation script, you need to add zap.bat along with all files and the sl directory inside the ZAP user data directory to your system path


---

# Running ZAP

ZAP includes a Windows launcher named `zap.bat`.

Run commands like this:

```bat
zap help
```

The batch file simply executes:

```bat
python zap.py %*
```

and forwards all command-line arguments to `zap.py`.

To display all available commands, run:

```bat
zap help
```

---

# Commands

Basic syntax:

```text
zap <command> [package]
```

| Command | Description |
|---------|-------------|
| install | Install a package |
| remove | Remove a package |
| download | Download a package without installing |
| repo-add | Add a repository URL |
| repo-remove | Remove a repository URL |
| update | Updates all installed packages |
| upgrade | Upgrades zap to the latest version (experimental)|
| list | List installed packages |
| info | Display package information |
| help | Show the help message |

> **Warning**
>
> `zap upgrade` is only available when running the compiled ZAP executable.
---

# Directory Structure

Linux:

```text
~/.zap/
```

Windows:

```text
C:\Users\<user>\AppData\Local\Zap\
```

Contents:

```text
bin/                Installed packages
sl/                 Launchers created by ZAP
data/               User Data
├── repos.json      Stores repository URLs
└── zap.log         Log system

runtime/
├── down/           Downloaded package archives
├── ext/            Temporary package files
└── tmp/            Temporary repository indexes
```

---

# Creating a Repository

A repository is simply an HTTP server that hosts an `index.zip` file together with one or more package archives.

Example:

```text
repository/

├── index.zip
├── package1.zip
├── package2.zip
└── tools/
    └── editor.zip
```

Packages may be stored in any directory.

The final download URL is built by combining:

```text
base_url + package.url
```

Example:

Base URL:

```text
http://localhost:8000/
```

Package URL:

```text
tools/editor.zip
```

Final download URL:

```text
http://localhost:8000/tools/editor.zip
```

---

# Hosting a Repository

For local testing, Python's built-in HTTP server can be used.

From inside the repository directory, run:

```bash
python -m http.server 8000
```

The repository will then be available at:

```text
http://localhost:8000/
```

---

# Adding a Repository Repositories are stored in: 
```text 
data/repos.json 
``` 
Example: 
```json
{ "repos": [ "http://localhost:8000" ] } 
``` 
Add a repository: 
```text 
zap repo-add http://localhost:8000 
```
Remove a repository:
```text
zap repo-remove http://localhost:8000 
``` 
Repositories added with `zap repo-add` are used automatically when installing packages. When `zap install` is executed, ZAP downloads the repository indexes, searches for the requested packages, and removes the temporary index files after the installation process is complete.

---

# Repository Structure

The repository must expose its files directly over HTTP.

Example:

```text
http://example.com/

├── index.zip
├── package1.zip
├── package2.zip
└── tools/
    └── editor.zip
```

The `index.zip` file must always be located in the root of the repository.

---

# index.zip Structure

The archive must contain `index.json` directly in its root.

Correct:

```text
index.zip
└── index.json
```

Incorrect:

```text
index.zip
└── repository/
    └── index.json
```

---

# index.json Format

Example:

```json
{
    "repo": "Example Repository",
    "base_url": "http://localhost:8000/",
    "updated": "2026-03-14",
    "packages": [
        {
            "name": "package1",
            "version": "1.0.0",
            "description": "Example package",
            "url": "package1.zip",
            "system": "Windows",
            "exec_file": "package1.exe",
            "hash": ""
        },
        {
            "name": "editor",
            "version": "2.0.0",
            "description": "Text editor",
            "url": "tools/editor.zip",
            "system": "Windows",
            "exec_file": "editor.exe",
            "hash": ""
        }
    ]
}
```

---

# JSON Fields

| Field | Description |
|-------|-------------|
| repo | Repository name |
| base_url | Base URL used to download packages |
| updated | Date the repository was last updated |
| packages | List of available packages |
| name | Package name |
| version | Package version |
| description | Package description |
| url | Relative path to the package archive |
| system | Target operating system (`Windows`, `Linux`, etc.) |
| exec_file | Relative path to the executable inside the package archive. ZAP uses this executable to create the launcher after installation. |
| hash | SHA-256 checksum of the package archive (required) |

---

# Package Archives

Packages are distributed as ZIP archives.

A package archive may contain any files required by the application.

Example:

```text
hello.zip

├── hello.exe
├── readme.txt
└── assets/
```

The executable specified in `exec_file` **must exist** inside the archive.

Example:

```json
"exec_file": "hello.exe"
```

If the executable is stored inside a folder:

```text
hello.zip

bin/
└── hello.exe
```

then:

```json
"exec_file": "bin/hello.exe"
```

The archive may be stored anywhere inside the repository, provided its location matches the `url` field in `index.json`.

---

# How ZAP Works 
1. Reads the configured repository URLs. 
2. Downloads `index.zip` from each repository. 
3. Extracts `index.json` into a temporary directory. 
4. Searches for the requested package. 
5. Downloads the package archive. 
6. Verifies the SHA-256 checksum. 
7. Extracts and installs the package. 
8. Creates a launcher using the executable specified in `exec_file`. 
9. Removes the temporary repository indexes.

> **Notes** 
> 
> - `zap update` updates installed packages. It does **not** download repository indexes. 
> - Repository indexes are downloaded automatically when running `zap install`. 
> - Temporary repository indexes are deleted automatically after the installation process. 
> - ZAP currently does **not** resolve or install package dependencies automatically. 
> - The `system` field must exactly match the value returned by Python's `platform.system()` (for example: `Windows` or `Linux`)

# Security

ZAP supports SHA-256 package verification.

During installation, the downloaded archive is compared with the checksum provided in `index.json`.

If the checksums do not match, the package is rejected and deleted.

---

# Supported Platforms

| Operating System | Status |
|------------------|--------|
| Windows | Supported |
| Linux | Experimental |
| macOS | Not supported |

---

# Roadmap

- [x] Install
- [x] Download
- [x] Remove
- [x] List
- [x] Update
- [x] Upgrade
- [x] Package metadata (`info`)
- [ ] Dependency resolution
- [ ] Installation scripts
- [ ] Repository authentication

---

# Example

```bash
# 1. Add the official repository
zap repo-add https://bkner3.github.io/zap-repository/

# 2. Install the 'hello' test package
zap install hello

# 3. List installed packages
zap list

# 4. Run the installed package
hello

# 5. Remove the test package
zap remove hello

```

---

# Issues & Support

Found a bug or have a suggestion? Feel free to open an issue on GitHub:

-> [Open an Issue](https://github.com/Bkner3/zap/issues)

Before creating a new issue, please check if it has already been reported.

# License

Copyright (c) 2026 Bernardo

Licensed under the MIT License.


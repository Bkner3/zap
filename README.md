# README.md

```text
███████╗ █████╗ ██████╗
╚══███╔╝██╔══██╗██╔══██╗
  ███╔╝ ███████║██████╔╝
 ███╔╝  ██╔══██║██╔═══╝
███████╗██║  ██║██║
╚══════╝╚═╝  ╚═╝╚═╝ PM

```

# ZAP — Zippy Asset Packager

A lightweight command-line package manager written in Python.

[Official Repository](https://bkner3.github.io/zap-repository/)

> **Official Repository URL:**
> `[https://bkner3.github.io/zap-repository/](https://bkner3.github.io/zap-repository/)`

---

> **Current Status**
> ZAP is under active development.
> **Windows:** Fully supported.
> **Linux:** Currently unavailable / under active development (the program exits immediately on Linux environments).
> **Package Dependency Resolution:** Experimental recursive resolution is implemented.

---

# Features

* Install and remove packages
* Basic recursive package dependency resolution
* Multi-version installation support
* Download packages without installing
* Update all installed packages in one command
* List installed packages and display package metadata
* Automatic launcher creation (`sl/` directory)
* SHA-256 package checksum verification before installation
* HTTP/HTTPS-based repositories
* Multi-threaded downloads
* Self-update capabilities (compiled executable)

---

# Requirements

### Windows (Standard Executable Installer)

No external dependencies required! The installer downloads the pre-compiled `zap.exe` directly.

### Source Code / Development Setup

If you run ZAP directly from source:

* Python 3.10 or later
* pip

Required Python packages:

* `requests`
* `tqdm`
* `colorama`

Install them with:

```bash
pip install -r requirements.txt

```

---

# Getting Started

## Windows Installation

You can install ZAP automatically by running the PowerShell installation script (opens a new terminal session after installation):

```powershell
irm https://raw.githubusercontent.com/Bkner3/zap/refs/heads/main/setup/install.ps1 | iex

```

Or install it using the source code:

```bash
git clone https://github.com/Bkner3/zap
cd ZAP
pip install -r requirements.txt

```

> **Warning**
> If you do not use the installation script, you must add the `sl/` launcher directory inside the ZAP user data folder to your system `PATH`.

---

# Running ZAP

ZAP includes a Windows command launcher named `zap.cmd`.

Run commands like this:

```cmd
zap help

```

When running from source, the script executes:

```cmd
python zap.py %*

```

To display all available commands, run:

```cmd
zap help

```

> **Warning**
> If you installed ZAP via the installation script, simply open a new command prompt or terminal and type `zap help`.

---

## Quick Start

After installing ZAP, open a new terminal and run:

```text
zap help

```

### Add a repository

```text
zap repo-add https://example.com/repository

```

### Install a package

```text
zap install hello

```

You can also request a specific version or version constraints:

```text
zap install hello@1.2.0
zap install "hello@>=1.2.0"

```

### List installed packages

```text
zap list

```

### Show package information

```text
zap info hello

```

### Remove a package

```text
zap remove hello

```

To remove only a specific installed version:

```text
zap remove hello@1.2.0

```

### Download without installing

```text
zap download hello

```

This downloads the package archive directly to your current working directory.

### Update installed packages

```text
zap update

```

This fetches the latest repository indexes and updates all installed packages if a newer version is available.

### Upgrade ZAP

```text
zap upgrade

```

`upgrade` checks for ZAP releases and updates the tool itself.

---

# Commands

Basic syntax:

```text
zap <command> [package]

```

| Command | Description |
| --- | --- |
| `install` | Install a package and its required dependencies |
| `remove` | Remove a package or a specific version (`name@version`) |
| `download` | Download a package archive without installing |
| `repo-add` | Add a repository URL |
| `repo-remove` | Remove a repository URL |
| `update` | Update repository indexes and upgrade all installed packages |
| `upgrade` | Upgrade ZAP to the latest version |
| `config` | Manage configuration options (logo, debug mode) |
| `list` | List installed packages |
| `info` | Display detailed package metadata |
| `version` | Print current ZAP version |
| `reset-db` | Reset local SQLite database (Advanced / Troubleshooting) |
| `help` | Show the help message |

> **Information**
> If you want to select a specific version or range, use `name@version` or operators (`=`, `>=`, `<=`, `>`, `<`).
> Example: `zap install editor@2.0.6` or `zap install "editor@>=2.0.0"`

> **Warning**
> `zap upgrade` is only supported when running the compiled ZAP executable.
> `zap download` does not download the dependencies!!!
>

---

# Configuration

ZAP configuration options can be inspected or modified using the `config` command:

```text
zap config list                # Display current settings
zap config default             # Reset configuration to defaults
zap config open                # Open ZAP data directory in file manager
zap config set <option> <val>  # Update a configuration value

```

| Option | Description |
| --- | --- |
| `show_logo` | Enable or disable the ASCII banner on startup (`true`/`false`) |
| `use_user_logo` | Enable custom ASCII banner (`true`/`false`) |
| `user_logo` | string for custom logo using /n to change the line |
| `is_on_debug` | Toggle verbose logging and debug messages |

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
bin/                Installed package files organized by version
sl/                 Command launchers created by ZAP
data/               User Data & Configuration
├── repos.json      Configured repository URLs
├── zap.db          SQLite package database
├── config.json     CLI configuration
└── zap.log         Execution logs

runtime/            Internal runtime files
├── down/           Downloaded package archives
├── ext/            Temporary extraction directory
├── tmp/            Downloaded repository indexes
└── setup/          Installer assets

```

---

# Creating a Repository

A repository is an HTTP/HTTPS server hosting an `index.zip` index along with package archives.

Example structure:

```text
repository/
├── index.zip
├── package1.zip
├── package2.zip
└── tools/
    └── editor.zip

```

Packages may be organized in subdirectories. The download URL is resolved as:

```text
base_url + package.url

```

Example:

Base URL: `http://localhost:8000/`

Package Relative Path: `tools/editor.zip`

Final Download URL: `http://localhost:8000/tools/editor.zip`

---

# Hosting a Repository

For local testing, Python's built-in HTTP server can be used:

```bash
python -m http.server 8000

```

The repository will be available at:

```text
http://localhost:8000/

```

> **Note:** HTTPS is strongly recommended for production repositories.

---

# Adding a Repository

Repositories are managed via CLI or directly in `data/repos.json`.

Example configuration file:

```json
{
  "repos": [
    "https://bkner3.github.io/zap-repository"
  ]
}

```

Add a repository via command line:

```text
zap repo-add http://localhost:8000

```

Remove a repository:

```text
zap repo-remove http://localhost:8000

```

Repositories are queried automatically during package lookup and installation. Temporary index files are discarded after processing.

---

# Repository Structure

The repository must expose files directly over HTTP/HTTPS:

```text
https://example.com/
├── index.zip
├── package1.zip
├── package2.zip
└── tools/
    └── editor.zip

```

The `index.zip` file **must** reside at the root of the repository.

---

# index.zip Structure

The `index.zip` archive must contain `index.json` directly at its root level.

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

Example configuration:

```json
{
  "repo": "Example Repository",
  "base_url": "http://localhost:8000/",
  "updated": "2026-03-14",
  "packages": [
    {
      "name": "package1",
      "version": "1.0.0",
      "author": "Author Name",
      "type": "PROGRAM",
      "description": "Example package",
      "url": "package1.zip",
      "system": "Windows",
      "exec_file": "package1.exe",
      "hash": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
    },
    {
      "name": "editor",
      "version": "2.0.0",
      "author": "Author Name",
      "type": "PROGRAM",
      "description": "Text editor",
      "url": "tools/editor.zip",
      "system": "Windows",
      "exec_file": "bin/editor.exe",
      "hash": "a591a6d40bf420404a011733cfb7b190d62c65bf0bcda32b57b277d9ad9f146e",
      "dependencies": [
        "package1@>=1.0.0"
      ]
    }
  ]
}

```

---

# JSON Fields

| Field | Description |
| --- | --- |
| `repo` | Repository display name |
| `base_url` | Base URL used to assemble package download paths |
| `updated` | Date when the repository index was last updated |
| `packages` | Array of available package objects |
| `name` | Unique package name |
| `version` | Package semver string |
| `description` | Brief package summary |
| `url` | Relative path to package ZIP archive |
| `system` | Target OS (`Windows`, `Linux`). Must match Python's `platform.system()` |
| `exec_file` | Relative path to executable inside archive used to create `sl/` launcher |
| `hash` | Required SHA-256 checksum of the package archive |
| `dependencies` | Array of dependency declarations (e.g., `pkg@1.0.0`, `pkg@>=2.0.0`) |

# Choice of Versions
To target a specific version or range, use the format package_name@operator_and_version.

Exact version: editor@2.0.0

Version operators: =, >, <, >=, <= (e.g., editor@>=2.0.0, editor@<=1.5.0)

Default behavior: If no operator or version is specified (e.g., zap install editor), ZAP will automatically install the latest available version.


---

# Package Archives

Packages are distributed as ZIP archives containing the binary assets and execution requirements.

Example layout:

```text
hello.zip
├── hello.exe
├── readme.txt
└── assets/

```

The binary designated by `exec_file` **must exist** inside the archive.

```json
"exec_file": "hello.exe"

```

If the binary is located inside a subdirectory:

```text
hello.zip
bin/
└── hello.exe

```

Set `exec_file` accordingly:

```json
"exec_file": "bin/hello.exe"

```

---

# How ZAP Works

1. Reads configured repository URLs from `repos.json`.
2. Downloads `index.zip` from repositories into `runtime/tmp/`.
3. Unpacks and reads `index.json`.
4. Evaluates package metadata, target system compatibility, and recursive dependencies.
5. Downloads the requested target archives to `runtime/down/`.
6. Validates SHA-256 checksum against metadata.
7. Safely extracts files into `bin/<package_name>/<version>/`.
8. Generates command launchers inside `sl/`.
9. Registers installation details inside SQLite database (`zap.db`).
10. Cleans up temporary files.

---

# Multi-Version Management

ZAP supports keeping multiple distinct versions of the same package installed simultaneously:

```text
bin/
└── editor/
    ├── 1.0.0/
    └── 2.0.0/

```

* Global launchers located in `sl/` default automatically to the highest installed version.
* Remove a specific version: `zap remove editor@1.0.0`.
* Removing a package without specifying a version (`zap remove editor`) removes all installed versions and cleans up the global launcher.

---

# Security

### SHA-256 Package Verification

ZAP automatically performs SHA-256 integrity verification upon downloading package archives. If the computed hash does not match the published checksum in `index.json`, installation is aborted and corrupt files are deleted immediately.

> **Security Note:**
> SHA-256 verification guarantees package integrity during transfer. It does not certify publisher trust or identity. Only configure repositories you trust.

---

# Supported Platforms

| Operating System | Status |
| --- | --- |
| **Windows** | Supported |
| **Linux** | Unavailable (Under Development) |
| **macOS** | Not Supported |

---

# Roadmap

* [x] Package installation & uninstallation
* [x] Direct archive downloading
* [x] Package listing & metadata inspection
* [x] Repository update & bulk package upgrade
* [x] Executable self-upgrade mechanism
* [x] Dynamic launcher generation
* [x] Basic recursive dependency resolution
* [ ] Advanced dependency conflict resolution & rollback
* [ ] Custom installation hook scripts
* [ ] Authenticated repository access

---

# Example

```bash
# 1. Add the official repository
zap repo-add https://bkner3.github.io/zap-repository/

# 2. Install the 'hello' test package
zap install hello

# 3. List installed packages
zap list

# 4. Run the installed package launcher
hello

# 5. Remove the test package
zap remove hello

```

---

# Issues & Support

Found a bug or have a suggestion or problem? Feel free to open an issue on GitHub:

-> [Open an Issue](https://github.com/Bkner3/zap/issues)

Before creating a new issue, please check if it has already been reported.

---

# License

Copyright (c) 2026 Bernardo

Licensed under the MIT License.

### Thanks for reading
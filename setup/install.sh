```sh
#!/bin/sh

set -e

ZAP_DIR="/opt/zap"
ZAP_BIN="/usr/local/bin/zap"
ZAP_TMP="$ZAP_DIR/runtime/tmp"

URL="https://github.com/Bkner3/zap/archive/refs/heads/main.zip"
ZIP_OUTPUT="$ZAP_TMP/zap.zip"
ZAP_SOURCE="$ZAP_TMP/zap-main"

. /etc/os-release

is_family() {
    family="$1"

    [ "$ID" = "$family" ] && return 0

    for like in ${ID_LIKE:-}; do
        [ "$like" = "$family" ] && return 0
    done

    return 1
}

if is_family debian; then
    PACKAGE_MANAGER="apt"
    pkgm_command="install -y"
    package="python3 python3-pip python3-venv unzip curl"
    PYTHON="/usr/bin/python3"
    echo "Distro: $PRETTY_NAME"

elif is_family arch; then
    PACKAGE_MANAGER="pacman"
    pkgm_command="-S --noconfirm"
    package="python python-pip unzip curl"
    PYTHON="/usr/bin/python"

elif is_family fedora; then
    PACKAGE_MANAGER="dnf"
    pkgm_command="install -y"
    package="python3 python3-pip python3-venv unzip curl"
    PYTHON="/usr/bin/python3"

elif is_family suse; then
    PACKAGE_MANAGER="zypper"
    pkgm_command="install --non-interactive"
    package="python3 python3-pip python3-venv unzip curl"
    PYTHON="/usr/bin/python3"

elif is_family alpine; then
    PACKAGE_MANAGER="apk"
    pkgm_command="add --no-interactive"
    package="python3 py3-pip py3-virtualenv unzip curl"
    PYTHON="/usr/bin/python3"

elif is_family gentoo; then
    PACKAGE_MANAGER="emerge"
    pkgm_command="--ask=n"
    package="dev-lang/python app-arch/unzip net-misc/curl"
    PYTHON="/usr/bin/python"

else
    echo "Distro not supported: $PRETTY_NAME"
    echo "ID: $ID"
    echo "ID_LIKE: ${ID_LIKE:-not defined}"
    exit 1
fi

if [ "$(id -u)" -eq 0 ]; then
    SUDO=""
else
    if command -v sudo >/dev/null 2>&1; then
        SUDO="sudo"
    else
        echo "Error: 'sudo' is not installed."
        exit 1
    fi
fi

if [ ! -x "$PYTHON" ]; then
    echo "Error: Python not found: $PYTHON"
    exit 1
fi

echo "Installing dependencies..."

$SUDO "$PACKAGE_MANAGER" $pkgm_command $package

echo "Preparing directories..."

$SUDO mkdir -p "$ZAP_DIR"
$SUDO mkdir -p "$ZAP_TMP"

echo "Downloading ZAP source..."

curl -fL "$URL" -o "$ZIP_OUTPUT"

echo "Extracting source..."

rm -rf "$ZAP_SOURCE"

unzip -q "$ZIP_OUTPUT" -d "$ZAP_TMP"

if [ ! -d "$ZAP_SOURCE" ]; then
    echo "Error: source directory not found: $ZAP_SOURCE"
    echo "Contents of $ZAP_TMP:"
    ls -la "$ZAP_TMP"
    exit 1
fi

cd "$ZAP_SOURCE"

echo "Creating Python virtual environment..."

"$PYTHON" -m venv ".venv"

echo "Installing Python dependencies..."

".venv/bin/python" -m pip install --upgrade pip
".venv/bin/python" -m pip install -r requirements.txt
".venv/bin/python" -m pip install pyinstaller

echo "Compiling ZAP..."

".venv/bin/pyinstaller" \
    --onefile \
    --icon="assets/zap_icon.png" \
    "zap.py"

echo "Installing ZAP..."

$SUDO mkdir -p "$ZAP_DIR"

$SUDO rm -f "$ZAP_DIR/zap"

$SUDO mv "dist/zap" "$ZAP_DIR/zap"

$SUDO chmod +x "$ZAP_DIR/zap"

$SUDO rm -f "$ZAP_BIN"

$SUDO ln -s "$ZAP_DIR/zap" "$ZAP_BIN"

rm -rf "$ZAP_SOURCE"
rm -f "$ZIP_OUTPUT"

echo ""
echo "Thanks for installing ZAP!"
echo "ZAP installed at: $ZAP_DIR/zap"
echo "Command: $ZAP_BIN"
echo ""
echo "Run:"
echo "  zap"
```

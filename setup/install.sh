#!/bin/sh

ZAP_DIR="$HOME/.zap"
ZAP_SL="$ZAP_DIR/sl"
ZAP_TMP="$ZAP_DIR/runtime/tmp"

URL="https://github.com/Bkner3/zap/archive/refs/heads/main.zip"
ZIP_OUTPUT="$ZAP_TMP/zap.zip"
ZAP_SOURCE="$ZAP_TMP/zap"

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
    package="python3 python3-pip python3-venv unzip"
    PYTHON="python3"
    echo "Distro: $PRETTY_NAME"

elif is_family arch; then
    PACKAGE_MANAGER="pacman"
    pkgm_command="-S --noconfirm"
    package="python python-pip unzip"
    PYTHON="python"
    echo "Distro: $PRETTY_NAME"

elif is_family fedora; then
    PACKAGE_MANAGER="dnf"
    pkgm_command="install -y"
    package="python3 python3-pip unzip"
    PYTHON="python3"
    echo "Distro: $PRETTY_NAME"

elif is_family suse; then
    PACKAGE_MANAGER="zypper"
    pkgm_command="install --non-interactive"
    package="python3 python3-pip unzip"
    PYTHON="python3"
    echo "Distro: $PRETTY_NAME"

elif is_family alpine; then
    PACKAGE_MANAGER="apk"
    pkgm_command="add --no-interactive"
    package="python3 py3-pip unzip"
    PYTHON="python3"
    echo "Distro: $PRETTY_NAME"

elif is_family gentoo; then
    PACKAGE_MANAGER="emerge"
    pkgm_command="--ask=n"
    package="dev-lang/python app-arch/unzip"
    PYTHON="python"
    echo "Distro: $PRETTY_NAME"

else
    echo "Distro not supported: $PRETTY_NAME"
    echo "ID: $ID"
    echo "ID_LIKE: ${ID_LIKE:-not defined}"
    exit 1
fi

echo "Downloading zap dependencies (Used in the compilation process!)"

if [ "$(id -u)" -eq 0 ]; then
    sudo=""
else
    if command -v sudo >/dev/null 2>&1; then
        sudo="sudo"
    else
        echo "Error: 'sudo' is not installed."
        exit 1
    fi
fi

$sudo "$PACKAGE_MANAGER" $pkgm_command $package

mkdir -p "$ZAP_SL"
mkdir -p "$ZAP_TMP"

if command -v wget >/dev/null 2>&1; then

    if ! wget "$URL" -O "$ZIP_OUTPUT"; then
        echo "wget failed, trying curl..."

        if command -v curl >/dev/null 2>&1; then
            curl -L "$URL" -o "$ZIP_OUTPUT"
        else
            echo "Error: 'curl' is not installed."
            exit 1
        fi
    fi

elif command -v curl >/dev/null 2>&1; then

    curl -L "$URL" -o "$ZIP_OUTPUT"

else

    echo "Error: 'wget' or 'curl' are not installed."
    exit 1

fi

rm -rf "$ZAP_SOURCE"

unzip -q "$ZIP_OUTPUT" -d "$ZAP_TMP"

if [ ! -d "$ZAP_SOURCE" ]; then
    echo "Error: source directory not found."
    exit 1
fi

cd "$ZAP_SOURCE"

"$PYTHON" -m venv ".venv"

. ".venv/bin/activate"

".venv/bin/pip" install -r requirements.txt
".venv/bin/pip" install pyinstaller

".venv/bin/pyinstaller" \
    --onefile \
    --icon="assets/zap_icon.png" \
    "zap.py"

mv "dist/zap" "$ZAP_DIR/zap"

cat > "$ZAP_SL/zap" <<'EOF'
#!/bin/sh
exec "$HOME/.zap/zap" "$@"
EOF

chmod +x "$ZAP_SL/zap"
chmod +x "$ZAP_DIR/zap"

rm -rf "$ZAP_SOURCE"
rm -f "$ZIP_OUTPUT"

if [ -f "$HOME/.profile" ]; then
    if ! grep -Fq 'export PATH="$HOME/.zap/sl:$PATH"' "$HOME/.profile"; then
        printf '\nexport PATH="$HOME/.zap/sl:$PATH"\n' >> "$HOME/.profile"
    fi
else
    printf 'export PATH="$HOME/.zap/sl:$PATH"\n' > "$HOME/.profile"
fi

export PATH="$ZAP_SL:$PATH"

echo "Thanks for installing ZAP"

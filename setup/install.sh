#!/bin/sh

ZAP_DIR="$HOME/.zap"
ZAP_SL="$ZAP_DIR/sl"
ZAP_TMP="$ZAP_DIR/runtime/tmp/"

URL="https://github.com/Bkner3/zap/archive/refs/heads/main.zip"
ZIP_OUTPUT="$ZAP_TMP/zap.zip"

. /etc/os-release

is_family() {
    family="$1"

    [ "$ID" = "$family" ] && return 0

    for like in $ID_LIKE; do
        [ "$like" = "$family" ] && return 0
    done

    return 1
}

#DETECT THE DISTRO
if is_family debian; then
    PACKAGE_MANAGER="apt"
    pkgm_command="install"
    package="python3 python3-pip python3-venv"
    echo "Distro: $PRETTY_NAME"

elif is_family arch; then
    PACKAGE_MANAGER="pacman"
    pkgm_command=" -S --noconfirm"
    package="python python-pip"
    echo "Distro: $PRETTY_NAME"

elif is_family fedora; then
    PACKAGE_MANAGER="dnf"
    pkgm_command="install"
    package="python3 python3-pip"
    echo "Distro: $PRETTY_NAME"

elif is_family suse; then
    PACKAGE_MANAGER="zypper"
    pkgm_command="install"
    package="python3 python3-pip"
    echo "Distro: $PRETTY_NAME"

elif is_family alpine; then
    PACKAGE_MANAGER="apk"
    pkgm_command="add"
    package="python3 py3-pip"
    echo "Distro: $PRETTY_NAME"

elif is_family gentoo; then
    PACKAGE_MANAGER="emerge"
    pkgm_command="--ask=n"
    echo "Distro: $PRETTY_NAME"

else
    echo "Distro not supported: $PRETTY_NAME"
    echo "ID: $ID"
    echo "ID_LIKE: ${ID_LIKE:- "not defined"}"
    exit 1
fi

echo "Downloading zap dependencies (Used in the compilation process!)"

#DOWNLOAD THE DEPENDENCIES FOR THE COMPILATION
$PACKAGE_MANAGER $pkgm_command $package


#CREATE THE ZAP DIRECTORY IN ~/.zap/
mkdir -p "$ZAP_SL"
mkdir -p "$ZAP_TMP"

#DOWNLOAD THE SOURCE CODE
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

unzip "$ZIP_OUTPUT"
cd "$ZAP_TMP/zap"


export PATH="$ZAP_SL:$PATH"
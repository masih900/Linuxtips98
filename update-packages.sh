#!/bin/bash

if [ -d "/data/data/com.termux" ]; then
    echo "Detected Termux. Updating packages..."
    pkg update -y && pkg upgrade -y
elif [ -f "/etc/os-release" ]; then
    echo "Detected Linux. Updating packages..."
    if command -v apt >/dev/null 2>&1; then
        sudo apt update && sudo apt upgrade -y
    elif command -v dnf >/dev/null 2>&1; then
        sudo dnf update -y
    elif command -v pacman >/dev/null 2>&1; then
        sudo pacman -Syu --noconfirm
    else
        echo "Unsupported package manager. Please update manually."
        exit 1
    fi
else
    echo "Unknown environment. Cannot update packages."
    exit 1
fi

echo "Package update completed!"

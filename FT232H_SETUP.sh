#!/usr/bin/env bash
set -euo pipefail

apt_package_install() {
    if apt list 2>/dev/null | grep -q "^$1/"; then
        sudo apt install -y "$@"
        return 0
    fi
    return 1
}

device_rules_create(){
    local path="$1"
    local subsystem="${2:-usb}"
    local VendorID="$3"
    local pid="$4"
    local group="$5"
    local permission="${6:-0666}"

    local rule="SUBSYSTEM==\"${subsystem}\", ATTR{idVendor}==\"${VendorID}\", ATTR{idProduct}==\"${pid}\", GROUP=\"${group}\", MODE=\"${permission}\""
    if  [ ! -f "${path}" ] || ! grep -qF "${rule}" "${path}"; then
        echo "${rule}" | sudo tee -a "${path}" > /dev/null
    fi
}

sudo apt update

apt_package_install libusb-1.0
apt_package_install libusb-1.0-0 libusb-1.0-0-dev

pids=("6001" "6011" "6010" "6014" "6015")

for pid in "${pids[@]}"; do
    device_rules_create "/etc/udev/rules.d/11-ftdi.rules" "usb" "0403" "${pid}" "plugdev" "0666"
done

sudo apt install -y python3-pip
sudo pip install pyftdi adafruit-blinka --break-system-packages

if ! grep -qF 'BLINKA_FT232H' ~/.bashrc; then
    echo 'export BLINKA_FT232H=1' >> ~/.bashrc
fi
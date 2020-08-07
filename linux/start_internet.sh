#!/bin/bash

sudo ip link set wlp4s0 up
sudo wpa_supplicant -B -i wlp4s0 -c /etc/wpa_supplicant/pal.conf
sudo dhcpcd wlp4s0

#!/usr/bin/bash
# you have to change the file permission to use this
# check the max brightness to be sure

sudo chmod 777 /sys/class/backlight/intel_backlight/brightness
echo $1 > /sys/class/backlight/intel_backlight/brightness

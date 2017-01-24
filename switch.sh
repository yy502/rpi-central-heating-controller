#!/bin/bash

CH="2"
HW="3"

if [ "$1" == "ch" ] || [ "$1" == "hw" ] && [ "$2" == "on" ] || [ "$2" == "off" ]; then
    if [ "$1" == "ch" ]; then
        TYPE="$CH"
    else
        TYPE="$HW"
    fi
    if [ "$2" == "on" ]; then
        MODE="1"
    else
        MODE="0"
    fi
    
    /usr/local/bin/gpio write $TYPE $MODE
    gpio readall | grep "GPIO. $TYPE" | awk '{print $4,$9,$11}'
else
    echo "Usage: switch.sh <ch|hw> <on|off>"
fi


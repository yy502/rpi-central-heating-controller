#!/bin/bash

# a wrapper script to switch the relays on/off via GPIOs
# execute 'switch.sh setup' once at boot to set the GPIOs in output mode

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

elif [ "$1" == "setup" ]; then
    /usr/local/bin/gpio mode $CH output
    /usr/local/bin/gpio mode $HW output
    gpio readall | grep "GPIO. [2,3]" | awk '{print $4,$9,$11}'

else
    echo "Usage: switch.sh [<ch|hw> <on|off>] | [setup]"

fi


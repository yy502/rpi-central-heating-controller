#!/bin/bash

CH="2"
HW="3"

/usr/local/bin/gpio mode $CH output
/usr/local/bin/gpio mode $HW output

gpio readall | grep "GPIO. [2,3]" | awk '{print $4,$9,$11}'

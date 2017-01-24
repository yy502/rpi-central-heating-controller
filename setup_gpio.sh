#!/bin/bash

CH="2"
HW="3"

/usr/local/bin/gpio mode $CH output
/usr/local/bin/gpio mode $HW output

echo "CH and HW pin set to output mode."
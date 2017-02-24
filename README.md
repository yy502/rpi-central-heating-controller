# Raspberry Pi Central Heating & Hot Water Controller #

I aim to use a Raspberry Pi to provide **fine** and **remote** control of my central heating and hot water, in order to improve the user experience as well as reducing energy wastage.

## Hardware ##

### Parts ###

- **Raspberry Pi** x1 -- I used a Zero for its size and price, since it will only serve as the central heating controller. It will be a waste and overkill to use a £30 worth full size RPi 2, for example.
- **USB WiFi Dongle** x1 -- for network connectivity
- **Female USB Socket** x1 -- to connect the USB WiFi dongle.
- **2-Switch Relay Module** x1 -- there are many versions of 5V relays that look very similar. The cheap ones I initially used does not support 3.3V signal. I could make it work with additional transistors and resistors, but that's just too messy. So make sure to pick one that supports 3.3V signal (5V for power is okay) to keep the wiring simple and clean. You can tell by the extra 4-leg chip on the relay.
- **RTC Module** x1 -- it's important to keep track of time in case there no network to sync with an NTP server.
- **DHT22** x1 -- as a backup on-board temperature sensor. It will use a remote temperature sensor over WiFi in normal operation. Should it fail to contact the WiFi sensor for any reason, e.g. sensor failure, router failure, signal interference, it will use its backup on-board sensor.
- **0.96" OLED Display Module** -- to display what's going on rather than needing to open a browser to check its status and settings.
- **Micro USB Cable** x1 and **USB Charger** x1 for power
- some wires
- something **non-conductive** to house the controller


### Wiring ###


### Dependencies ###

#### pigpio ####

(Download and install)[http://abyz.co.uk/rpi/pigpio/download.html]


### Command Line Back-End ###

simple control commands

#### Settings ####

CH and HW pins are using WiringPi index; DHT sensor pin is using BCM index.

#### Cron Jobs ####

timed switches

### OLED Display ###

128x64 display over I2C

### Web UI ###

to view room temperature, timer/temperature settings, overrides, etc.

### Remote Access ###

external access over the Interbet with port forwarding and authentication

### Watchdog ###

In case RPi silently crashes and freezes, watchdog service will auto-reboot it and hopefully things will be back on track.
Here's how to set up watchdog.

    sudo modprobe bcm2708_wdog
    echo "bcm2708_wdog" | sudo tee -a /etc/modules
    sudo apt-get install watchdog chkconfig
    sudo chkconfig --add watchdog

    sudo vim /etc/watchdog.conf
    # uncomment lines below
    watchdog-device = /dev/watchdog
    max-load-1 = 24

    sudo /etc/init.d/watchdog start

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

- CH and HW pins use WiringPi index.
- Local DHT sensor pin uses BCM index.
- Remote sensor is a URL for reading data.

#### Cron Jobs ####

timed switches

### Web UI ###

to view room temperature, timer/temperature settings, overrides, etc.

### Web Server ###

After some research, I chose `nginx` over `Apache` for web server for its
lightweight and performance.

    sudo apt-get install nginx

I normally change the site root to `/home/pi/www`, so I'll use this path through out the documentation.

I'm going to use Python for CGI, so here's how to set up `uwsgi` with `nginx` to handle `.py` scripts.

    sudo apt-get install uwsgi
    sudo uwsgi --version

    sudo vim /etc/uwsgi/apps-available/uwsgi_config.ini

    # make it looks like the block below
    [uwsgi]
    plugins = cgi
    socket = 127.0.0.1:8000
    cgi = /home/pi/www   # this should match your site's root
    chdir = /home/pi/www
    cgi-allowed-ext = .py
    cgi-helper = .py = python
    uid = pi
    gid = pi
    die-on-term = true

    sudo ln -s /etc/uwsgi/apps-available/uwsgi_config.ini /etc/uwsgi/apps-enabled/uwsgi_config.ini
    sudo service uwsgi restart

    # Config nginx to use uWSGI for Python CGI

    # edit nginx site config
    # add a block as below to handle .py files
    location ~ \.py$ {
        uwsgi_pass 127.0.0.1:8000;
        include uwsgi_params;
        uwsgi_modifier1 9;
    }

    sudo service nginx restart

    # Testing: add 4 lines of code below into /home/pi/www/hello.py

    #!/usr/bin/env python
    import cgi
    print "Content-Type: text/html\n"
    print "<h1>Hello World from Python CGI</h1>"

    # make it executable
    chmod +x /home/pi/www/hello.py

Now visit `http://rpi_ip/hello.py` and expect to see some hello world texts.

### Port Forwarding ###

This is done on your router. Basically, map an external port to your RPi's port 80 for external web access; and map an external port to your RPi's port 22 for external SSH access in case some manual work is needed.

*Warning on Security*

- add some password protection to your web app for obvious reasons if you allow external access to your home central heating and hot water controller.
- do not map 80 for 80 and 22 for 22. Choose some other random ports to avoid _some_ attacks.
- install `fail2ban` to block attempts to hack in. I only allow 2 failed attempts before banning an IP for 24 hours or longer. If you do so, make sure you don't lock yourself out. Better to use password-less login on your own computers or mobile phones using rsa key.

### Watchdog ###

In case RPi silently crashes and freezes, watchdog service will auto-reboot it and hopefully things will be back on track.
Here's how to set up watchdog.

    # add this line to /boot/config.txt
    dtparam=watchdog=on

    # reboot; check watchdog device is enabled
    ls /dev/watchdog*

    /dev/watchdog /dev/watchdog0

    # install package
    sudo apt-get install watchdog
    # ignore a few lines of warnings and ignores

    # edit config file: /etc/watchdog.conf
    # uncomment
    watchdog-device = /dev/watchdog
    max-load-1 = 24

    # add below or you get "cannot set timeout 60 (errno = 22 = 'Invalid argument')"
    # because the default 60 seconds is an invalid option!
    watchdog-timeout=15

    # start watchdog service
    sudo /etc/init.d/watchdog start

    # check watchdog status
    sudo systemctl status watchdog

    # now make watchdog service start at boot
    # add below to /lib/systemd/system/watchdog.service
    [Install]
    WantedBy=multi-user.target

    # then run
    sudo systemctl enable watchdog

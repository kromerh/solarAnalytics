# solarAnalytics

1.) Analyse solar panel output distribution on roof

2.) Predict total output based on historical performance of the sysem

## Installation of vzlogger

- Buy smartmeter readout (IR), i.e. this one Weidmann Elektronik Stromzähler, Smart Meter IR (Infrarot) Schreib/Lesekopf USB (Optokopf) https://www.amazon.de/gp/product/B01B8N0ASY/ref=ppx_yo_dt_b_asin_title_o08_s00?ie=UTF8&psc=1
- Install it onto the current reader, connect it to RPi3
- Follow instructions to install vzlogger on volkszaehler.org
	- Check if the readout is found by the RPi ` ls -l /dev/serial/{by-path,by-id}/*`
	- Install vzlogger from https://github.com/volkszaehler/vzlogger
		- To install, follow the detailed installation instructions at http://wiki.volkszaehler.org/software/controller/vzlogger/installation_cpp-version
			If you're impatient you can quickstart using (Debian Wheezy):

			`sudo apt-get install build-essential git-core cmake pkg-config subversion libcurl3-dev libgnutls-dev libsasl2-dev uuid-dev uuid-runtime libtool dh-autoreconf libunistring-dev`

			For Debian Jessie be sure to add:

			`sudo apt-get install libgcrypt20-dev`

	- Create the configuration for vzlogger as in `/readout_scripts/vzlogger/vzlogger.conf`
	- Start vzlogger with  vzlogger -c CONFIGURATIONFILE

## Installation of MongoDB on RPi3 with Python3

- Install the packages with `sudo apt-get install mongodb`
- Create directory `/data/db`, be sure to check permissions correctly with `sudo chrown -R `mongodb` /data/db/`
- Start mongodb service using `sudo systemctl start mongodb.service`
- Check that it is also running with a restart of the system (do the same for the vzlogger!)

- Install python packages `pip3 install pymongo==3.4.0 pandas numpy`

- Put the readout script `read_itron_push_mongoDB.py` into `/home/pi/Documents/myvzlogger/`

- Edit the crontab via `crontab -e` and add the line
	`*/5 * * * * /usr/bin/python3 /home/pi/Documents/myvzlogger/read_itron_push_mongoDB.py`


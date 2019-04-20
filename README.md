# solarAnalytics

1.) Analyse solar panel output distribution on roof

2.) Predict total output based on historical performance of the sysem


## Installation of MongoDB on RPi3 with Python3

- Install the packages with `sudo apt-get install mongodb`
- Create directory `/data/db`, be sure to check permissions correctly with `sudo chrown -R `mongodb` /data/db/`
- Start mongodb service using `sudo systemctl start mongodb.service`
- Check that it is also running with a restart of the system (do the same for the vzlogger!)

- Install python packages `pip3 install pymongo`


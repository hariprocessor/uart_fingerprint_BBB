# UART fingerprint sensor for BBB

## Usage
### Beaglebone black
* Connect fingerprint sensor to beaglebone.
* In beaglebone system, execute index.py.
* Required package before executing is tornado.

### Ubuntu
* Ubuntu server(web server)
* In host system, execute index.py.
* Required package before executing is tornado, torndb, python-mysql.

### index.html
* It is a client file.
* Execute with any browser.

## fingerprint.py
* This file control the fingerprint module.
* It is developed by Adafuit_UART and can conduct basic functions, registering fingerprint, deleting fingerprint and retrieving the number of registered fingerprints.

### Demo
* https://www.youtube.com/watch?v=sQ4XIpN_qYE


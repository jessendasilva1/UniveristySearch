#!/bin/sh
sudo apt-get update # To get the latest package lists
sudo apt-get -y install nginx npm openssl
#etc.



sudo cp -Rf nginx/* /etc/nginx/ #copying config files from etc/nginx folder
cd webserver



npm install



mkdir -p ssl/certs
mkdir -p ssl/private



openssl dhparam -out ssl/certs/dhparam.pem 4096



sudo openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout ssl/private/nginx-selfsigned.key -out ssl/certs/nginx-selfsigned.crt
cd ..

crontab /graphing/scraper/test/cronjobs.txt
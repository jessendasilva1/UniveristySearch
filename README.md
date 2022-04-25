# W22_CIS3760_Team11

Winter 2022 CIS 3760 Sprint 9

#

## Usage
-   Install dependincies required for starting the server by running `./installScript.sh` 
-   start the server by running `systemctl start nginx` 
-   stop the server by running `systemctl stop nginx` 
-   restart the server by running `systemctl restart nginx`
-   start uWSGI by running `uwsgi --ini api/wsgi.ini`
	-    To Daemonize the uwsgi master append `--daemonize /home/sysadmin/api/logs/uwsgi_daemon.log`
-   get uWSGI pid via `cat /tmp/uwsgi.pid` and restart with `kill -HUP [pid]`. 
	-    Kill using `-INT`

## Automated Testing
-   Open cronjobs by running in any directory `crontab -e`
	-  To run error testing email script every hour, paste thes following lines at end of file:
	- `5 * * * * /usr/bin/python3 ~/graphing/scraper/test/courseTest.py`
	- `10 * * * * /usr/bin/python3 ~/graphing/scraper/test/emailTemplate.py`
	- `0 * * * * cd ~/graphing/scraper && npm run testFront >> outputTest.txt`
-	Set Email and Password to be notified of error by opening `graphing/scraper/test/emailTemplate.py`
	-	Change `email = ""` to desired email and `pasword = ""` to desired password
	-	All e-mails sent 10 minutes after the hour are done automatically by crontab, manual testing if any other time

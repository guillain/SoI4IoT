# SoI4IoT
Web integration of Cisco Spark to provide continuous engagement system.

## Why I've done that?
That's the capability for the external people to request (open folder) and exchange with an enterprise via web form and follow its folder.
During that the enterprise continue to work on the folder with Spark and all associated communication features.

## Scenario
The scenario can be describe like that :
* AirLines open a folder via a web form
* Automatically: the Spark room (Space) is created, the AirLine, Field Representative and Expert are associated to this Space. 
* The Expert works on the folder with the Field Representative support and communicate through the file sharing, webex and video conferencing, white board and chat provided by the Space.
* At the end of the folder process, only the admin can close the folder and the dump of the Space stay available via the Web form.

## Requirements
Account
* Cisco Spark (for free)

Servers
* Python 2.7
* * flask
* * werkzeug
* * MySQLdb
* MySQL

Two web server configurations available
* Apache and WSGI
* python CLI (should be considered as dev pf even if tips for exposure is provided)

### Local database
* Manage user independantly of Spark Cloud user registration system. This is to solve an access issue for external people who doesn't use Spak.
* Manage users, groups and admin rights (via web forms)
* Log each events and Spark messages and provide permnanent access to the dump and real time replication features (useful for third party integration)
* Also useful if we consider that the log function can be adapted for noSQL and data analytics systems

## Features
* [doc/features.md](doc/features.md)

## HowTo
* [Install](doc/install.md)
* [Configuration](doc/configuration.md)

## ToDo list
* [ToDo](doc/todo.md)

## Report bug
* [issues](issues)


Have fun ;)

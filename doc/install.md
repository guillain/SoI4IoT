# PreRequisites
* MySQL
* python (2.7)
* * Flask
* * MySQLdb

Configurations is provided for:
* Apache and WSGI server
* python/flask CLI (cf. run file)
But you can also get only the python with another web server, container...
So according to your choice thanks to install the necessary package

# Install

## Clone localy
```bash
git clone https://github.com/guillain/SoI4IoT.git
cd SoI4IoT
```
### Install the Python requirements
```bash
pip install -r requirements.txt
```
### Create additionnal folders
```bash
mkdir log downloads uploads
```
### Configure and set apache configuration
If you use one dedicated alias on your web server for this specific web app, follow the explanation below (virtual host creation with default config file).
Else put the WSGI content of the default file in your virtual host definiton
* For unsecure http (80)
```bash
cp conf/apache.conf.default conf/apache.conf
vi conf/apache.conf
ln -s /var/www/SoI4IoT/conf/apache.conf /etc/apache2/conf-enabled/SoI4IoT_apache.conf
```
* For secure http (443)
```bash
cp conf/apache-secure.conf.default conf/SoI4IoT_apache_secure.conf
vi conf/apache-secure.conf
ln -s /var/www/SoI4IoT/conf/apache-secure.conf /etc/apache2/conf-enabled/SoI4IoT_apache-secure.conf
```
### Configure the database
```bash
mysqladmin create SoI4IoT -utoto -p
mysql SoI4IoT -utoto -p < conf/mysql.sql
mysql SoI4IoT -utoto -p < conf/mysql_data.sql (add users can be useful...)
```
### Complete setting file
```bash
cp conf/settings.cfg.default conf/settings.cfg
vi conf/settings.cfg
```


## Fast & Furious method
```bash
yum install httpd
yum mysql-server mysql-client
yum install MySQL-python.x_
yum install mysql-server
yum install python-pip
pip install flask
pip install express
pip install config
```


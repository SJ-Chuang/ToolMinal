# ToolMinal

ToolMinal is a tool project developed based on Flask, and it will continue to be updated and deployed to [here](http://64.110.111.37) for demonstration.

## Installation

Run the following code for installing required packages
```python
pip install -r requiremnets.txt
```

The installation and testing of this project were conducted using [Python 3.8.10](https://www.python.org/downloads/release/python-3810/).

## Get started
```shell
python src/main.py
```

## Deploy via the Apache Server
1. Open the configuration file (```/etc/apache2/sites-available/000-default.conf```) after installing the Apache server

ServerName 64.110.111.37
ServerAdmin ubuntu@localhost

2. Modify the config file with the following script
* Change the ServerName to your local IP
* Change the ServerAdmin to a sudo user
```apacheconf
<VirtualHost *:80>
    ServerName 127.0.0.1
    ServerAdmin user@localhost
    DocumentRoot /var/www/ToolMinal/src
    Alias /static /var/www/ToolMinal/static

    WSGIDaemonProcess main user=www-data group=www-data threads=5 python-home=/var/www/venv
    WSGIScriptAlias / /var/www/ToolMinal/src/main.wsgi
    WSGIApplicationGroup %{GLOBAL}

    <Directory /var/www/ToolMinal/src>
        WSGIProcessGroup main
        WSGIApplicationGroup %{GLOBAL}
        Order deny,allow
        Allow from all
    </Directory>
    <Directory /var/www/ToolMinal/static>
        Order allow,deny
        Allow from all
    </Directory>

    ErrorLog ${APACHE_LOG_DIR}/error.log
    CustomLog ${APACHE_LOG_DIR}/access.log combined
</VirtualHost>
```
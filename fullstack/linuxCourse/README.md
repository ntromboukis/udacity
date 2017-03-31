# Linux Configuration Course

public ip address   : 35.165.209.51

ssh port            : 2200

hosted URL          : http://ec2-35-165-209-51.us-west-2.compute.amazonaws.com/


## Software installed and Configuration Changes

#### Created New User and granted sudo

## 1. Created new user grader

```bash
sudo adduser grader
```


## 2. Granted sudo privileges
Reference: [Udacity](https://classroom.udacity.com/nanodegrees/nd004/parts/00413454014/modules/357367901175461/lessons/4331066009/concepts/48010894710923#)

Created
```bash
sudo nano /etc/sudoers.d/grader
```

Pasted into grader
```bash
grader ALL=(ALL) NOPASSWD:ALL
```


## 3. Updated installed packages

```bash
sudo apt-get update
```


## 4. Upgraded install packages

```bash
sudo apt-get upgrade
```


## 5. Changed SSH port and Configured SSH access

#### Opened config file
```bash
sudo nano /etc/ssh/sshd_config
```

#### Edited file
Changed
```Port``` to 2200
```PermitRootLogin``` to ```no```

Appended
```AllowedUsers grader```

Write out file

Restarted SSH
```bash
sudo service sshd restart
```


## 6. Created SSH keys
References: [Udacity](https://classroom.udacity.com/nanodegrees/nd004/parts/00413454014/modules/357367901175461/lessons/4331066009/concepts/48010894770923#), [Digital Ocean](https://www.digitalocean.com/community/tutorials/how-to-configure-ssh-key-based-authentication-on-a-linux-server)

On local machine
```bash
ssh-keygen
```

Set keys
```bash
ssh-copy-id grader@35.165.209.51 -p 2200
```

Logged in with new user
```bash
ssh grader@35.165.209.51 -p 2200
```


## 7. Configured UFW
Reference: [Udacity](https://classroom.udacity.com/nanodegrees/nd004/parts/00413454014/modules/357367901175461/lessons/4331066009/concepts/48010894990923#)

Denied all incoming traffic
```bash
sudo ufw default deny incoming
```

Allowed all outgoing traffic
```bash
sudo ufw default allow outgoing
```

Allowed incoming traffic
```bash
sudo ufw allow 2200/tcp
```

```bash
sudo ufw allow 80/tcp
```

```bash
sudo ufw allow 123/tcp
```

Enabled UFW
```bash
sudo ufw enable
```


## 8. Installed Fail2ban
Reference: [Digital Ocean](https://www.digitalocean.com/community/tutorials/how-to-protect-ssh-with-fail2ban-on-ubuntu-14-04)

```bash
sudo apt-get install fail2ban
```

Copied config file
```bash
sudo cp /etc/fail2ban/jail.conf /etc/fail2banjail.local
```

Opened local cofig file
```bash
sudo nano /etc/fail2banjail.local
```

Updated preferences
```bash
bantime = 1800
```

```bash
ssh port = 2200
```


## 9. Installed and configured dev stack
Reference: [Udacity](http://blog.udacity.com/2015/03/step-by-step-guide-install-lamp-linux-apache-mysql-python-ubuntu.html)

#### Installed Apache
```bash
sudo apt-get install apache2
```
Opened browser and navigated to public ip address

#### Installed mod_wsgi for serving Python apps from Apache and helper package python-setuptools
```bash
sudo apt-get install python-setuptools libapache2-mod-wsgi
```

Restarted Apache server
```bash
sudo service apache2 restart
```

#### Installed PostgreSQL
```bash
sudo apt-get install postgresql
```


## 10. Installed and configured git

Installed git
```bash
sudo apt-get install git
```

Setup name and email for commits
```bash
git config --global user.name "YOUR NAME"
```

```bash
git config --global user.email "YOUR EMAIL ADDRESS"
```


## 11. Setup for delpoying app
Reference: [Digital Ocean](https://www.digitalocean.com/community/tutorials/how-to-deploy-a-flask-application-on-an-ubuntu-vps)

Changed to www directory
```bash
cd /var/www
```

Setup app directory
```bash
sudo mkdir catalog
```

```bash
cd catalog
```

Installed Pip
```bash
sudo apt-get install python-pip
```

Installed virtualenv
```bash
sudo pip install virtualenv
```

Set virtual environment to name 'venv'
```bash
sudo virtualenv venv
```

Enabled permissions for venv
```bash
sudo chmod -R 777 venv
```

Activated virtual environment
```bash
source venv/bin/activate
```

Installed Flask inside venv
```bash
pip install Flask
```

Deactivated venv
```bash
deactivate
```

Created new virtual host
```bash
sudo nano /etc/apache2/sites-available/catalog.conf
```

Pasted the following lines (used names and addresses for my app)

```apache
   <VirtualHost *:80>
      ServerName 35.165.209.51
      ServerAdmin admin@35.165.209.51
      WSGIScriptAlias / /var/www/catalog/catalog.wsgi
      <Directory /var/www/catalog/catalog/>
          Order allow,deny
          Allow from all
      </Directory>
      Alias /static /var/www/catalog/catalog/static
      <Directory /var/www/catalog/catalog/static/>
          Order allow,deny
          Allow from all
      </Directory>
      ErrorLog ${APACHE_LOG_DIR}/error.log
      LogLevel warn
      CustomLog ${APACHE_LOG_DIR}/access.log combined
   </VirtualHost>
```

Enabled virtual host
```bash
sudo a2ensite catalog
```

Created wsgi file
```bash
sudo nano /var/www/catalog/catalog.wsgi
```

Pasted the following lines

```bash
import sys
import logging
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0,"/var/www/catalog/")

from catalog import app as application
application.secret_key = 'Add your secret key'
```

Restarted Apache

```bash
sudo service apache2 restart
```

## Setup Application

Changed dir to catalog
```bash
cd /var/www/catalog
```

Cloned git repository
```bash
git clone https://github.com/ntromboukis/item-catalog.git
```

Moved contents to catalog dir
```bash
mkdir catalog
```

```bash
mv item-catalog catalog
```

#### Installed modules and packages

Activate venv
```bash
source venv/bin/activate
```

Installed httplib2
```bash
pip install httplib2
```

Installed requests
```bash
pip install requests
```

Installed oauth2client
```bash
sudo pip install --upgrade oauth2client
```

Installed SQLAlchemy
```bash
sudo pip install sqlalchemy
```

Install the Python PostgreSQL adapter psycopg
```bash
sudo apt-get install python-psycopg2
```

## Configure PostgreSQL
Reference: [Digital Ocean](https://www.digitalocean.com/community/tutorials/how-to-secure-postgresql-on-an-ubuntu-vps)

Opened the database setup file
```bash
sudo nano database_setup.py
```

Changed the line starting with "engine" to (fill in a password):
```engine = create_engine('postgresql://catalog:PW-FOR-DB@localhost/catalog')```
Changed the same line in project.py

Renamed project.py:
```bash
mv project.py __init__.py
```

Created user for psql
```bash
sudo adduser catalog
```

Changed to default user postgres
```bash
sudo su - postgres
```

Connected to the system
```bash
psql
```

Created User
```bash
CREATE USER catalog WITH PASSWORD 'PW-FOR-DB';
```

Allowed user to create database tables
```bash
ALTER USER catalog CREATEDB;
```

Created database
```bash
CREATE DATABASE catalog WITH OWNER catalog;
```

Connected to database
```bash
\c catalog
```

Revoked all rights
```bash
REVOKE ALL ON SCHEMA public FROM public;
```

Granted only access to the catalog role
```bash
GRANT ALL ON SCHEMA public TO catalog;
```

## Done
Restarted Apache and opened page in browser
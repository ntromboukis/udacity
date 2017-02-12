#Linux Configuration Course

public ip address   : 35.165.209.51
ssh port            : 2200
hosted URL          : http://ec2-35-165-209-51.us-west-2.compute.amazonaws.com/


##Software installed and Configuration Changes

####Created New User and granted sudo

##1. Created new user grader

```sudo adduser grader```


##2. Granted sudo privileges
Reference: [Udacity](https://classroom.udacity.com/nanodegrees/nd004/parts/00413454014/modules/357367901175461/lessons/4331066009/concepts/48010894710923#)

Created
```sudo nano /etc/sudoers.d/grader```

Pasted into grader
```grader ALL=(ALL) NOPASSWD:ALL```


##3. Updated installed packages

```sudo apt-get update```


##4. Upgraded install packages

```sudo apt-get upgrade```


##5. Changed SSH port and Configured SSH access

####Opened config file
```sudo nano /etc/ssh/sshd_config```

####Edited file
Changed
```Port``` to 2200
```PermitRootLogin``` to ```no```

Appended ```AllowedUsers grader```

Write out file

Restarted SSH
```sudo service sshd restart```


##6. Created SSH keys
References: [Udacity](https://classroom.udacity.com/nanodegrees/nd004/parts/00413454014/modules/357367901175461/lessons/4331066009/concepts/48010894770923#), [Digital Ocean](https://www.digitalocean.com/community/tutorials/how-to-configure-ssh-key-based-authentication-on-a-linux-server)

On local machine

```ssh-keygen```

Set keys
```ssh-copy-id grader@35.165.209.51 -p 2200```

Logged in with new user
```ssh grader@35.165.209.51 -p 2200```


##7. Configured UFW
Reference: [Udacity](https://classroom.udacity.com/nanodegrees/nd004/parts/00413454014/modules/357367901175461/lessons/4331066009/concepts/48010894990923#)

Denied all incoming traffic
```sudo ufw default deny incoming```

Allowed all outgoing traffic
```sudo ufw default allow outgoing```

Allowed incoming traffic
```sudo ufw allow 2200/tcp```
```sudo ufw allow 80/tcp```
```sudo ufw allow 123/tcp```

Enabled UFW
```sudo ufw enable```


##8. Installed Fail2ban
Reference: [Digital Ocean](https://www.digitalocean.com/community/tutorials/how-to-protect-ssh-with-fail2ban-on-ubuntu-14-04)

```sudo apt-get install fail2ban```

Copied config file
```sudo cp /etc/fail2ban/jail.conf /etc/fail2banjail.local```

Opened local cofig file
```sudo nano /etc/fail2banjail.local```

Updated preferences
```bantime = 1800```
```ssh port = 2200```


##9. Installed and configured dev stack
Reference: [Udacity](http://blog.udacity.com/2015/03/step-by-step-guide-install-lamp-linux-apache-mysql-python-ubuntu.html)

####Installed Apache
```sudo apt-get install apache2```
Opened browser and navigated to public ip address

####Installed mod_wsgi for serving Python apps from Apache and helper package python-setuptools
```sudo apt-get install python-setuptools libapache2-mod-wsgi```

Restarted Apache server
```sudo service apache2 restart```

####Installed PostgreSQL
```sudo apt-get install postgresql```


##10. Installed and configured git

Installed git
```sudo apt-get install git```

Setup name and email for commits
```git config --global user.name "YOUR NAME"```
```git config --global user.email "YOUR EMAIL ADDRESS"```


##11. Setup for delpoying app
Reference: [Digital Ocean](https://www.digitalocean.com/community/tutorials/how-to-deploy-a-flask-application-on-an-ubuntu-vps)

Changed to www directory
```cd /var/www```

Setup app directory
```sudo mkdir catalog```
```cd catalog```

Installed Pip
```sudo apt-get install python-pip```

Installed virtualenv
```sudo pip install virtualenv```

Set virtual environment to name 'venv'
```sudo virtualenv venv```

Enabled permissions for venv
```sudo chmod -R 777 venv```

Activated virtual environment
```source venv/bin/activate```

Installed Flask inside venv
```pip install Flask```

Deactivated venv
```deactivate```

Created new virtual host
```sudo nano /etc/apache2/sites-available/catalog.conf```

Pasted the following lines (used names and addresses for my app)
```
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
```sudo a2ensite catalog```

Created wsgi file
```sudo nano /var/www/catalog/catalog.wsgi```

Pasted the following lines
```
import sys
import logging
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0,"/var/www/catalog/")

from catalog import app as application
application.secret_key = 'Add your secret key'
```

Restarted Apache
```sudo service apache2 restart```

##Setup Application

Changed dir to catalog
```cd /var/www/catalog```

Cloned git repository
```git clone https://github.com/ntromboukis/item-catalog.git```

Moved contents to catalog dir
```mkdir catalog```
```mv item-catalog catalog```

####Installed modules and packages

Activate venv
```source venv/bin/activate```

Installed httplib2
```pip install httplib2```

Installed requests
```pip install requests```

Installed oauth2client
sudo pip install --upgrade oauth2client

Installed SQLAlchemy
```sudo pip install sqlalchemy```

Install the Python PostgreSQL adapter psycopg
```sudo apt-get install python-psycopg2```

##Configure PostgreSQL
Reference: [Digital Ocean](https://www.digitalocean.com/community/tutorials/how-to-secure-postgresql-on-an-ubuntu-vps)

Opened the database setup file
```sudo nano database_setup.py```

Changed the line starting with "engine" to (fill in a password):
```engine = create_engine('postgresql://catalog:PW-FOR-DB@localhost/catalog')```
Changed the same line in project.py

Renamed project.py:
```mv project.py __init__.py```

Created user for psql
```sudo adduser catalog```

Changed to default user postgres
```sudo su - postgres```

Connected to the system
```psql```

Created User
```CREATE USER catalog WITH PASSWORD 'PW-FOR-DB';```

Allowed user to create database tables
```ALTER USER catalog CREATEDB;```

Created databas
```CREATE DATABASE catalog WITH OWNER catalog;```

Connected to database
``` \c catalog```

Revoked all rights
```REVOKE ALL ON SCHEMA public FROM public;```

Granted only access to the catalog role
```GRANT ALL ON SCHEMA public TO catalog;```

##Done
Restarted Apache and opened page in browser
Create a new GitHub repository and add a file named README.md.
Your README.md file should include all of the following:

i. The IP address and SSH port so your server can be accessed by the reviewer.

ii. The complete URL to your hosted web application.

iii. A summary of software you installed and configuration changes made.

iv. A list of any third-party resources you made use of to complete this project.
Open your ~/.ssh/udacity_key.rsa file in a text editor and copy the contents of that file.
During the submission process, paste the contents of the udacity_key.rsa file into the "Notes to Reviewer" field.

#Linux Configuration Course#

ip Address   : 35.165.209.51
ssh port     : 2200
hosted URL   : http://ec2-35-165-209-51.us-west-2.compute.amazonaws.com/

##Software installed and Configuration Changes##

####Created New User and granted sudo####

##1. Created new user grader##
Reference: [Digital Ocean](https://www.digitalocean.com/community/tutorials/how-to-add-and-delete-users-on-an-ubuntu-14-04-vps)

```sudo newuser grader```


##2. Grant sudo privileges##
Reference: [Udacity](https://classroom.udacity.com/nanodegrees/nd004/parts/00413454014/modules/357367901175461/lessons/4331066009/concepts/48010894710923#)

Create
```sudo nano /etc/sudoers.d/grader```

Paste into grader
```grader ALL=(ALL) NOPASSWD:ALL```


##3. Update installed packages##

```sudo apt-get install update```


##4. Upgrade install packages##

```sudo apt-get install upgrade```


##5. Change SSH port and Configure SSH access##

####Open config file####
```sudo nano /etc/ssh/sshd_config```

####Edit file####
Change
```Port``` to 2200
```PermitRootLogin``` to ```no```

Append ```AllowedUsers grader```

Write out file

Restart SSH
```sudo service sshd restart```


##6. Create SSH keys##
References: [Udacity](https://classroom.udacity.com/nanodegrees/nd004/parts/00413454014/modules/357367901175461/lessons/4331066009/concepts/48010894770923#), [Digital Ocean](https://www.digitalocean.com/community/tutorials/how-to-configure-ssh-key-based-authentication-on-a-linux-server)

On local machine
```ssh-keygen```

Set keys
```ssh-copy-id grader@remote_host -p**_PORTNUMBER_**```

Login with new user
```ssh grader@public_ip_address -p 2200```


##7. Configure UFW##
Reference: [Udacity](https://classroom.udacity.com/nanodegrees/nd004/parts/00413454014/modules/357367901175461/lessons/4331066009/concepts/48010894990923#)

Deny all incoming traffic
```sudo ufw default deny incoming```

Allow all outgoing traffic
```sudo ufw default allow outgoing```

Allow incoming traffic
```sudo ufw allow 2200/tcp```
```sudo ufw allow 80/tcp```
```sudo ufw allow 123/tcp```

Enable UFW
```sudo ufw enable```


##8. Install Fail2ban##
Reference: [Digital Ocean](https://www.digitalocean.com/community/tutorials/how-to-protect-ssh-with-fail2ban-on-ubuntu-14-04)

```sudo apt-get install fail2ban```

Copy config file
```sudo cp /etc/fail2ban/jail.conf /etc/fail2banjail.local```

Open local cofig file
```sudo nano /etc/fail2banjail.local```

Update preferences
```bantime = 1800```
```ssh port = 2200```


##9. Install and configure dev stack##
Reference: [Udacity](http://blog.udacity.com/2015/03/step-by-step-guide-install-lamp-linux-apache-mysql-python-ubuntu.html)

####Install Apache####
```sudo apt-get install apache2```
Open browser and navigate to public ip address

####Install mod_wsgi for serving Python apps from Apache and helper package python-setuptools####
```sudo apt-get install python-setuptools libapache2-mod-wsgi```

Restart Apache server
```sudo service apache2 restart```

####Install PostgreSQL####
```sudo apt-get install postgresql```


##10. Install and configure git##

Install git
```sudo apt-get install git```

Setup name and email for commits
```git config --global user.name "YOUR NAME"```
```git config --global user.email "YOUR EMAIL ADDRESS"```


##11. Setup for delpoying app##
Reference: [Digital Ocean](https://www.digitalocean.com/community/tutorials/how-to-deploy-a-flask-application-on-an-ubuntu-vps)

Move to www directory
```cd /var/www```

Setup app directory
```sudo mkdir catalog```
```cd catalog```

Install Pip
```sudo apt-get install python-pip```

Install virtualenv
```sudo pip install virtualenv```

Set virtual environment to name 'venv'
```sudo virtualenv venv```

Enable permissions for venv
```sudo chmod -R 777 venv```

Activate virtual environment
```source venv/bin/activate```

Install Flask inside venv
```pip install Flask```

Deactivate venv
```deactivate```

Create new virtual host
```sudo nano /etc/apache2/sites-available/catalog.conf```

Pasted the following lines (used names and addresses for my app)
```
   <VirtualHost *:80>
      ServerName PUBLIC-IP-ADDRESS
      ServerAdmin admin@PUBLIC-IP-ADDRESS
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

Enable virtual host
```sudo a2ensite catalog```

Create wsgi file
```sudo nano /var/www/catalog/catalog.wsgi```

Paste the following lines
```
import sys
import logging
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0,"/var/www/catalog/")

from catalog import app as application
application.secret_key = 'Add your secret key'
```

Restart Apache
```sudo service apache2 restart```

##Setup Application##

Change dir to catalog
```cd /var/www/catalog```

Clone git repository
```git clone https://github.com/ntromboukis/item-catalog.git```

Move contents to catalog dir
```mkdir catalog```
```mv item-catalog catalog```




##3rd Party resources##
[Fail2Ban](https://www.digitalocean.com/community/tutorials/how-to-protect-ssh-with-fail2ban-on-ubuntu-14-04)
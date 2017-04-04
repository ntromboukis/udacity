# Description
This is the second project in Udacity's Full Stack Nanodegree program

# Steps to Run program
The way you run this program (on OSX)

1. Make sure you have VirtualBox and Vagrant installed if not install it from [here](https://www.udacity.com/wiki/ud197/install-vagrant). Udacity has a great starting page to get your machine up and running!

2. Now navigate (in terminal) to the tournament folder you just downloaded and type ```vagrant up```. This will set up a vagrant file in that folder.

3. After Vagrant has created the file, run the command ```vagrant ssh```.

4. Now you are in the VM. Navigate run ```cd /vagrant/tournament``` to be put in the tournament directory.

5. Run ```ls``` to make sure tournament.py, tournament.sql, and tournament_test.py are in the directory

6. Now run ```psql``` to be put in the postgresql database

7. Run the command ```CREATE DATABASE tournament;``` then ```\i tournament.sql```

8. Now hit ```control + D``` to exit from psql

9. Now run ```python tournament_test.py``` to test the schema of the database
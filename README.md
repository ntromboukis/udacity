###Instructions to run this application on OSX

If you do not have Virtual Box or Vagrant already installed, refer to this [tutorial](https://www.udacity.com/wiki/ud197/install-vagrant).

###In Terminal
- Clone this repository and navigate to it.
- Run ```vagrant up```
- Run ```vagrant ssh``` (This will put you in the virtual machine)
- Once in the virtual machine navigate to ```cd /vagrant/```
- Run ```python database-setup.py```
- To populate the database you can run ```python storepopulator.py```
- Run ```python project.py```

After getting the confirmation open up your favorite browser and go to ```http://localhost:5000/```

You can login using a Google account, open a store, populate it with your favorite things, or just browse around!
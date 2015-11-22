
sqlPyPlus
=========

A generic database browser based on Flask, using SQLAlchemy's reflection/inspector mechanism.

How to start
============

After unpacking, set up your virtualenv and install the needed packages:

      virtualenv venv
      source ./venv/bin/activate
      pip install -r requirements.txt

Edit the config file and set 

     SQLALCHEMY_DATABASE_URI = 'sqlite:////Users/ap/PycharmProjects/data-test.sqlite'

to point to your DB.

Start the server via:

      python run.py

and point your browser to http://localhost:5000 - you should see a list of all tables in your DB.

Click on one to see the corresponding table ... ;)


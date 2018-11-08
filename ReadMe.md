
DbExplorer
==========

A generic database browsing service based on Flask, using SQLAlchemy's reflection/inspector mechanism.

You provide a URI to your database and the service will discover all available information in there and present it in your web browser.


How to start
============

After unpacking, set up your virtualenv and install the needed packages:

      virtualenv venv
      source ./venv/bin/activate
      pip install -r requirements.txt

Create an `instance` directory, and a `config.py` in there. Edit that config file and set 

     SQLALCHEMY_DATABASE_URI = 'sqlite:////Users/ap/PycharmProjects/data-test.sqlite'

to point to your DB, and update the `SECRET_KEY` variable with something secure.

Then start the server via:

      python run.py

and point your browser to http://localhost:5000 and start exploring your DB.


# CellCounter

[![Build Status](https://secure.travis-ci.org/cellcounter/cellcounter.png)](http://travis-ci.org/cellcounter/cellcounter)

Code developed at NHSHackDay2 to count cells for haematological blood film analysis.


## Running Locally

Clone the repository:

    git clone ...

Create a virtual environment:

    virtualenv .env
    source .env/bin/activate
    pip install -r requirements.txt

(if you don't have `virtualenv`, then `sudo pip install virtualenv`)
(if you don't have `pip`, then `sudo easy_install pip`)

Build the database:

    python manage.py syncdb

Run the Django webserver:

    python manage.py runserver

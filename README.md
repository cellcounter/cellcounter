# CellCounter

[![Build Status](https://secure.travis-ci.org/cellcounter/cellcounter.png)](http://travis-ci.org/cellcounter/cellcounter) [![Coverage Status](https://coveralls.io/repos/cellcounter/cellcounter/badge.svg?branch=master&service=github)](https://coveralls.io/github/cellcounter/cellcounter?branch=master)

Code developed at NHSHackDay2 to count cells for haematological blood film analysis. Cellcounter is deployed at [cellcountr.com](http://www.cellcountr.com).


## Running Locally

Clone the repository:

    git clone ...

Create a virtual environment:

    virtualenv -p python3 .env
    source .env/bin/activate
    pip install -r requirements.txt

(if you don't have `virtualenv`, then `sudo pip install virtualenv`)
(if you don't have `pip`, then `sudo easy_install pip`)

Update your database:

    python manage.py migrate

Run the Django webserver locally, setting the DEBUG environment variable:

    export DEBUG=True
    export ALLOWED_HOSTS="127.0.0.1"
    python manage.py runserver

To run the test suite locally, you also need the test requirements in your virtualenv:

    pip install -r test-requirements.txt

    export TEST=True
    python manage.py test

To install npm from source for JavaScript testing:

    curl http://nodejs.org/dist/node-latest.tar.gz | tar xvz
    cd node-v*
    ./configure --prefix=$VIRTUAL_ENV
    make install

    npm ci
    
    export DEBUG=True; export ALLOWED_HOSTS="127.0.0.1"
    ./test_integration


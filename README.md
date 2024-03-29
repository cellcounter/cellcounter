# CellCounter

[![CircleCI](https://circleci.com/gh/cellcounter/cellcounter/tree/master.svg?style=shield)](https://circleci.com/gh/cellcounter/cellcounter/tree/master) [![Coverage Status](https://coveralls.io/repos/cellcounter/cellcounter/badge.svg?branch=master&service=github)](https://coveralls.io/github/cellcounter/cellcounter?branch=master)

Cellcounter Django app to count cells for haematological blood film analysis. Cellcounter is deployed at [cellcountr.com](http://www.cellcountr.com).


## Running Locally

Clone the repository:

    git clone ...

Create a virtual environment:

    virtualenv -p python3 .env
    source .env/bin/activate
    pip install --upgrade pip
    pip install -r requirements.txt

(if you don't have `virtualenv`, then `sudo pip install virtualenv`)
(if you don't have `pip`, then `sudo easy_install pip`)

Update your database:

    python manage.py migrate

Run the Django webserver locally, setting the DEBUG environment variable:

    export DEBUG=True
    export ALLOWED_HOSTS="127.0.0.1"
    python manage.py runserver


## Testing

To run the test suite locally, you also need the test requirements in your virtualenv:

    pip install -r test-requirements.txt

    export TEST=True
    python manage.py test

To install npm from source for JavaScript testing:

    curl https://nodejs.org/dist/node-latest.tar.gz | tar xvz
    cd node-v*
    ./configure --prefix=$VIRTUAL_ENV
    make install

    npm ci
    
    export DEBUG=True; export ALLOWED_HOSTS="127.0.0.1"
    ./test_integration

To run the test suite via docker:

    docker build --target test -t cellcountr/cellcountr_test:latest .

    docker run cellcountr/cellcountr_test:latest python manage.py test


## Deployment

To create the docker volume to store the media files:

    sudo mkdir -p /var/www/mediafiles
    docker volume create --driver local --opt type=none --opt device=/var/www/mediafiles --opt o=bind media_volume

To build and run the docker image:

    cp env.dev.example env.dev
    edit env.dev
    docker compose build

    docker compose up -d

    docker compose exec web python manage.py migrate --no-input

To stop the docker image:

    docker compose down -v


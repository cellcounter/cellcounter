#!/bin/bash

export NODE_PATH=$VIRTUAL_ENV/lib/node_modules


TMP_SERVER_LOG_FILE=$(tempfile)

export DEBUG=True
# disable autoreload or Django unhelpfully changes PID
python -u manage.py runserver --noreload &>$TMP_SERVER_LOG_FILE &

DEBUG_SERVER_PID=$!

sleep 1

while ! grep -m1 'Quit the server with CONTROL-C.' < $TMP_SERVER_LOG_FILE; do
    sleep 1
done

cat $TMP_SERVER_LOG_FILE

mocha js_test/integration.js

# kill the server process
kill $DEBUG_SERVER_PID

# delete the temporary log file
rm $TMP_SERVER_LOG_FILE


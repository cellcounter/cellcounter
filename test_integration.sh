#!/bin/bash

export NODE_PATH=node_modules/.bin


TMP_SERVER_LOG_FILE=$(mktemp)

export DEBUG=True

# disable autoreload or Django unhelpfully changes PID
(python3 -u manage.py runserver --noreload | tee $TMP_SERVER_LOG_FILE) &

DEBUG_SERVER_PID=$!

sleep 1

[ -d "/proc/${DEBUG_SERVER_PID}" ] || (echo "Server not running"; exit 1)

while ! grep -m1 'Quit the server with CONTROL-C.' < $TMP_SERVER_LOG_FILE; do
    sleep 1
done

TESTS="js_test/test_counting.js"
TESTS="$TESTS js_test/test_display.js"
TESTS="$TESTS js_test/test_abnormal.js"
TESTS="$TESTS js_test/test_keyboard_editing.js"

mocha $TESTS

retval=$?

# kill the server process
kill $DEBUG_SERVER_PID

# delete the temporary log file
rm $TMP_SERVER_LOG_FILE

exit $retval


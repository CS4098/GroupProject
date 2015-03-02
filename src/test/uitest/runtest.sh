#!/bin/sh
count_failed=0

java -jar ./src/test/uitest/selenium-server-standalone-2.43.1.jar &
sleep 5
fails=$(python ./src/test/uitest/uitest.py)
kill $!
sleep 1
count_failed=$((count_failed+fails))
exit $count_failed

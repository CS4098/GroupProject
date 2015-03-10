#!/bin/sh
echo ""
echo "-------------------------------------------------------"
echo " SELENIUM WEBDRIVER TESTS"
echo "-------------------------------------------------------"
count_failed=0

echo "Starting up Selenium server..."
java -jar ./src/test/uitest/selenium-server-standalone-2.43.1.jar &
sleep 5
echo "Running Selenium tests..."
fails=$(python ./src/test/uitest/uitest.py)
echo "Stopping Selenium server..."
kill $!
sleep 1
count_failed=$((count_failed+fails))
exit $count_failed

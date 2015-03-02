#pip install selenium
java -jar ./src/test/uitest/selenium-server-standalone-2.43.1.jar &
sleep 5
python ./src/test/uitest/uitest.py
kill $!
sleep 1
echo

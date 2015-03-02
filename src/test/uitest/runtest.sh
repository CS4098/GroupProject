#pip install selenium
#java -jar selenium-server-standalone-2.43.1.jar &
java -jar src/test/UITest/selenium-server-standalone-2.43.1.jar &
sleep 5
#python uitest.py
python src/test/UITest/uitest.py
kill $!
sleep 1
echo

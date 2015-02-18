#pip install selenium
java -jar selenium-server-standalone-2.43.1.jar &
sleep 5
python uitest.py
kill $!
echo
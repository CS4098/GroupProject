import unittest
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

class uiTest(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Remote("http://localhost:4444/wd/hub", webdriver.DesiredCapabilities.HTMLUNIT.copy())

    def test_ui(self):
        driver = self.driver
        driver.get("http://bhegarty.com/cgi-bin/")
        #driver.get("http://127.0.0.1/GroupProject/src/main/webapp/index.html")

        inputForm = driver.find_element_by_name("pmlfile")
        #inputForm.send_keys("test.pml")
        inputForm.send_keys("src/test/UITest/test.pml")
        inputForm.submit()

        test = driver.find_element_by_id('output')
        assert test.text != ""


    def tearDown(self):
       self.driver.quit()

if __name__ == "__main__":
    unittest.main()

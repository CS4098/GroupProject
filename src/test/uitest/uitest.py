import unittest
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException 
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

class pmlFile(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Remote("http://localhost:4444/wd/hub", webdriver.DesiredCapabilities.HTMLUNIT.copy())

    def testUI(self):
        driver = self.driver
        driver.get("http://vps138348.ovh.net/GroupProject/")

        fileUpload = driver.find_element_by_name("pmlfile")
        fileUpload.send_keys("src/test/uitest/test.pml")
        fileUpload.submit()

        pmlFile = driver.find_element_by_id("pml")
        assert pmlFile.text != ""


    def tearDown(self):
       self.driver.quit()

class promelaGenerator(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Remote("http://localhost:4444/wd/hub", webdriver.DesiredCapabilities.HTMLUNIT.copy())

    def testUI(self):
        driver = self.driver
        driver.get("http://vps138348.ovh.net/GroupProject/")

        fileUpload = driver.find_element_by_name("pmlfile")
        fileUpload.send_keys("src/test/uitest/test.pml")
        fileUpload.submit()

        promela = driver.find_element_by_id("promela")
        assert promela.text != ""

    def tearDown(self):
       self.driver.quit()

class spinOutput(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Remote("http://localhost:4444/wd/hub", webdriver.DesiredCapabilities.HTMLUNIT.copy())

    def testUI(self):
        driver = self.driver
        driver.get("http://vps138348.ovh.net/GroupProject/")

        fileUpload = driver.find_element_by_name("pmlfile")
        fileUpload.send_keys("src/test/uitest/test.pml")
        fileUpload.submit()

        resourceValue = driver.find_element_by_name("resourcefile")
        resourceValue.submit()

        spin = driver.find_element_by_id("spin")
        assert spin.text != ""

    def tearDown(self):
        self.driver.quit()

class spinTrailOutput(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Remote("http://localhost:4444/wd/hub", webdriver.DesiredCapabilities.HTMLUNIT.copy())

    def testUI(self):
        driver = self.driver
        driver.get("http://vps138348.ovh.net/GroupProject/")

        fileUpload = driver.find_element_by_name("pmlfile")
        fileUpload.send_keys("src/test/uitest/test.pml")
        fileUpload.submit()

        resourceValue = driver.find_element_by_name("resourcefile")
        resourceValue.submit()

        spin = driver.find_element_by_id("spintrail")
        assert spin.text != ""

    def tearDown(self):
        self.driver.quit()

if __name__ == "__main__":
    unittest.main()

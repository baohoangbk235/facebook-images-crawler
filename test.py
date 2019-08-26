import time
from selenium import webdriver 
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

options = Options()
options.set_preference("dom.webnotifications.enabled", False)
driver = webdriver.Firefox(firefox_options=options)
driver.get("https://www.facebook.com/")
element = driver.find_element_by_name("email")
element.clear()
element.send_keys("0354505705")
element = driver.find_element_by_name("pass")
element.clear()
element.send_keys("facebook")
time.sleep(1)
element.send_keys(Keys.ENTER)
time.sleep(5)

element = driver.find_element_by_id("email")
if element is not None:
    print("Failed!")
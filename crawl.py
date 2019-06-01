from selenium import webdriver 
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import shutil
from tqdm import tqdm
from selenium.webdriver.support import expected_conditions as EC
import requests
# from bs4 import BeautifulSoup
import time
import re

def downloadImage(url, img_name):
    response = requests.get(url)
    if response.status_code == 200:
        with open(img_name + ".jpg", 'wb') as f:
            f.write(response.content)

SCROLL_PAUSE_TIME = 1

def scrollToEnd(driver):
        # Get scroll height
        last_height = driver.execute_script("return document.body.scrollHeight")

        while True:
                # Scroll down to bottom
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                # Wait to load page
                time.sleep(SCROLL_PAUSE_TIME)

                # Calculate new scroll height and compare with last scroll height
                new_height = driver.execute_script("return document.body.scrollHeight")
                if new_height == last_height:
                        break
                last_height = new_height

def getImages(driver, homepage):
        driver.get(homepage + "&sk=photos")
        time.sleep(2)
        # scrollToEnd(driver)
        time.sleep(2)
        imageElements = driver.find_elements_by_css_selector('a._6i9')
        # images = [imageElement.get_attribute("href") for imageElement in imageElements]
        full_hd_images = []
        count = 0
        for imageElement in imageElements:
            imageElement.click()
            time.sleep(2)
            driver.implicitly_wait(20)  
            elm_img = driver.find_element_by_css_selector('img.spotlight')
            driver.implicitly_wait(20)
            image_src = elm_img.get_attribute("src")
            p = re.compile('([0-9]+[_0-9a-zA-Z]+\.(png|jpg|gif))')
            m = p.findall(image_src)
            driver.find_element_by_css_selector('a._418x').click()
            time.sleep(2)
            driver.implicitly_wait(20)
            full_hd_images.append(m[0][0])
        return full_hd_images

def getFriendList(driver, homepage):
        driver.get(homepage + "&sk=friends")
        time.sleep(2)
        scrollToEnd(driver)
        time.sleep(2)
        friendElements = driver.find_elements_by_class_name("_6i9")
        friends = [friendElement.get_attribute("href") for friendElement in friendElements]
        return friends

def logInAccount(driver):
    email = input("Enter email: ")
    password = input("Enter password: ")
    driver.get("https://www.facebook.com/")

    element = driver.find_element_by_name("email")
    element.send_keys(email)
    element = driver.find_element_by_name("pass")
    element.send_keys(password)
    time.sleep(1)
    element.send_keys(Keys.ENTER)
    time.sleep(5)

options = Options()
options.set_headless()
options.set_preference("dom.webnotifications.enabled", False)
driver = webdriver.Firefox(firefox_options=options)
logInAccount(driver)
element = driver.find_element_by_class_name("_2s25")
homepage = element.get_attribute("href")

# images = driver.find_elements_by_class_name("fbPhotoStarGridElement")
# friends = getFriendList(driver, homepage)
# for friend in friends:
#         print(friend)
#download image

images = getImages(driver, homepage)
count = 0
for img in images:
    # downloadImage(img, str(count))
    print(img)
    count += 1
driver.close()

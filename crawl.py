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
import dlib
import cv2
from PIL import Image
from io import BytesIO
import numpy as np

def read_image_from_url(url, name):
	response = requests.get(url)
	image = Image.open(BytesIO(response.content))
	image = np.asarray(image)[:, :, ::-1].copy() 

	# Khai báo việc sử dụng các hàm của dlib
	hog_face_detector = dlib.get_frontal_face_detector()

	# Thực hiện xác định bằng HOG và SVM
	start = time.time()
	faces_hog = hog_face_detector(image, 1)
	end = time.time()
	print("Hog + SVM Execution time: " + str(end-start))
	count = 0
	# Vẽ một đường bao màu xanh lá xung quanh các khuôn mặt được xác định ra bởi HOG + SVM
	if len(faces_hog) > 0:
	  cv2.imwrite(name, image)

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
        # driver.get(homepage + "&sk=photos")
        driver.get(homepage)
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
            print(image_src)
            p = re.compile('([0-9]+[_0-9a-zA-Z]+\.(png|jpg|gif))')
            m = p.findall(image_src)
            driver.find_element_by_css_selector('a._418x').click()
            time.sleep(2)
            driver.implicitly_wait(20)
            read_image_from_url(image_src, m[0][0])
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
# options.set_headless()
options.set_preference("dom.webnotifications.enabled", False)
driver = webdriver.Firefox(firefox_options=options)
logInAccount(driver)
# element = driver.find_element_by_class_name("_2s25")
# homepage = element.get_attribute("href")
homepage = "https://www.facebook.com/luong.duong.1276/photos?lst=100010797130122%3A100002977864766%3A1559406306"

# images = driver.find_elements_by_class_name("fbPhotoStarGridElement")
# friends = getFriendList(driver, homepage)
# for friend in friends:
#         print(friend)
#download image

images = getImages(driver, homepage)
count = 0
# for img in images:
    # downloadImage(img, str(count))
    # count += 1
driver.close()

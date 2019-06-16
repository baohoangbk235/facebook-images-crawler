from multiprocessing import Pool
import time
import getpass
import cv2
from selenium import webdriver 
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import requests
import os
import re
from PIL import Image
from io import BytesIO
import numpy as np

class CrawlerBrowser:
	def __init__(self, timeout=5, display_browser=True, max_images_per_facebook=30):
		options = Options()
		if display_browser == False:
			options.set_headless()
		options.set_preference("dom.webnotifications.enabled", False)
		self.driver = webdriver.Firefox(firefox_options=options)
		# self.driver.set_page_load_timeout(timeout)
		self.driver_status = True
		self.homepage = None
		self.SCROLL_PAUSE_TIME = 2
		self.max_images_per_facebook = max_images_per_facebook
		self.end_of_page = False

		# email = input("Email or phonenumber: ")
		# password = getpass.getpass("Password: ")
		email = "your email or phonenumber here"
		password = ""

		try:
			self.driver.get("https://www.facebook.com/")
			element = self.driver.find_element_by_name("email")
			element.clear()
			element.send_keys(email)
			element = self.driver.find_element_by_name("pass")
			element.clear()
			element.send_keys(password)
			time.sleep(1)
			element.send_keys(Keys.ENTER)
			time.sleep(5)
			print("[INFO] Log in successfully!")

			element = self.driver.find_element_by_class_name("_2s25")
			self.homepage = element.get_attribute("href")

			self.driver.get(self.homepage + "&sk=friends")
			time.sleep(2)
			self.scrollToEnd()
			time.sleep(2)
			friendElements = self.driver.find_elements_by_class_name("_5q6s")
			self.friends = [friendElement.get_attribute("href") for friendElement in friendElements]
			print("[INFO] Get friendlist successfully!")

		except TimeoutException as ex:
			print("Exception has been thrown. " + str(ex))

	def scrollToEnd(self):
	        # Get scroll height
	        last_height = self.driver.execute_script("return document.body.scrollHeight")

	        while True:
	                # Scroll down to bottom
	                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
	                # Wait to load page
	                time.sleep(self.SCROLL_PAUSE_TIME)

	                # Calculate new scroll height and compare with last scroll height
	                new_height = self.driver.execute_script("return document.body.scrollHeight")
	                if new_height == last_height:
	                        break
	                last_height = new_height

	def scrollToBottom(self):
		last_height = self.driver.execute_script("return document.body.scrollHeight")
		if not self.end_of_page:
			self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
			time.sleep(self.SCROLL_PAUSE_TIME)
		new_height = self.driver.execute_script("return document.body.scrollHeight")
		if new_height == last_height:
			self.end_of_page = True

	def read_image_from_url(self, url, name):
		try:
			response = requests.get(url)
			image = Image.open(BytesIO(response.content))
			image = np.asarray(image)[:, :, ::-1].copy() 

		# Khai báo việc sử dụng các hàm của dlib
		# hog_face_detector = dlib.get_frontal_face_detector()

		# # Thực hiện xác định bằng HOG và SVM
		# start = time.time()
		# faces_hog = hog_face_detector(image, 1)
		# end = time.time()
		# print("Hog + SVM Execution time: " + str(end-start))
		# if len(faces_hog) > 0:
		#   cv2.imwrite(name, image)
			cv2.imwrite(name,image)
			return image
		except requests.ConnectionError:
			return None

	def get_homepage(self):
		return self.homepage

	def get_friendlist(self):
		return self.friends

	def quit_browser(self):
		self.driver.close()
		self.driver_status = False

	def get_images(self, homepage):
		self.driver.get(homepage + "&sk=photos")
		# self.scrollToEnd()
		time.sleep(2)
		imageElements = self.driver.find_elements_by_css_selector('a._6i9')

		full_hd_images = []
		wait = WebDriverWait(self.driver, 20)
		# self.scrollToBottom()


		for imageElement in imageElements:
			self.scrollToBottom()
			self.driver.execute_script("arguments[0].click();", imageElement)
			time.sleep(2)
			try:
				elm_img = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'img.spotlight')))
				image_src = elm_img.get_attribute("src")
			except Exception as e:
				print(str(e))
				continue
			print(image_src)
			p = re.compile('([0-9]+[_0-9a-zA-Z]+\.(png|jpg|gif))')
			m = p.findall(image_src)
			tmp = lambda:self.driver.find_element_by_css_selector('a._418x')
			time.sleep(2)
			tmp().click()
			time.sleep(2)
			match = re.search(r'https://www.facebook.com/profile.php?(.*)', homepage)
			if match is None:
				match = re.search(r'https://www.facebook.com/(.*)', homepage)
			path = os.path.join(os.getcwd(),'images/{}'.format(match.groups()[0].replace('?','')))   
			if not os.path.exists(path):
				os.mkdir(path)
			imageName = os.path.join(path, m[0][0])
			if self.read_image_from_url(image_src, imageName) is not None:
				full_hd_images.append(m[0][0])

			if len(full_hd_images) == self.max_images_per_facebook:
				break

		print("\n[DONE] Facebook {} has finished crawling images!\n".format(homepage))
		return full_hd_images

	def get_friendlist_images(self):
		for friend in self.friends[16:]:
			self.get_images(friend)


if __name__ == '__main__':
	crawler = CrawlerBrowser()
	crawler.get_friendlist_images()
	crawler.quit_browser()

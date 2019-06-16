import time
import dlib
import cv2
from PIL import Image
import requests
from io import BytesIO
import numpy as np
import os
import glob
from tqdm import tqdm

extracted_faces_dir = "/home/baohoang235/Downloads/extraced"

def extract_faces(img_path, root, count):
	image = cv2.imread(img_path)
	if image is None:
		return None
	height, width = image.shape[:2]
	if (not height > 0) or (not width > 0):
		return None  
	hog_face_detector = dlib.get_frontal_face_detector()
	# Thực hiện xác định bằng HOG và SVM
	faces_hog = hog_face_detector(image, 1)
	# Vẽ một đường bao màu xanh lá xung quanh các khuôn mặt được xác định ra bởi HOG + SVM
	num = 0
	for face in faces_hog:
		x = face.left()
		y = face.top()
		w = face.right() - x
		h = face.bottom() - y
		num += 1
		try:
			face_img = image[y:y+h, x:x+w]
			face_img = cv2.resize(face_img, (128, 128))
			cv2.imwrite(os.path.join(root,'{}_{}.jpg'.format(count, num)), face_img)
		except Exception as e:
			print(str(e))
			print("[INFO] Error at {}".format(img_path))
			continue
	return image

def parse_dir(img_dir):
	count = 0
	if not os.path.exists(extracted_faces_dir):
		os.mkdir(extracted_faces_dir)

	for root, dirs, files in os.walk(img_dir):
		for d in dirs:
			for ext in ('jpg', 'jpeg', 'png'):
				for f in tqdm(glob.glob(os.path.join(root, d, '*.' + ext))):
					count += 1
					saved_dir = os.path.join(extracted_faces_dir,d)
					if not os.path.exists(saved_dir):
						os.mkdir(saved_dir)
					extract_faces(f, saved_dir, count)
			print("[INFO] Faces of {} has been extracted successfully!".format(d))

if __name__ == '__main__':
	parse_dir("/home/baohoang235/Downloads/images")

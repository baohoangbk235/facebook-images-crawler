import time
import dlib
import cv2
from PIL import Image
import requests
from io import BytesIO
import numpy as np

img_path = '/home/baohoang235/Downloads/images/35.jpg'
# Đọc ảnh đầu vào
# image = cv2.imread(img_path)
url = "https://scontent.fhan5-3.fna.fbcdn.net/v/t1.0-9/46435022_1621506184618208_5865803665561878528_n.jpg?_nc_cat=106&_nc_oc=AQmKc_p0cfYUWq917Qt7D9BWJ5orFpUXz19jbXW6JPeKz0HE5PZqpSBATs-x4ntUmF0&_nc_ht=scontent.fhan5-3.fna&oh=f041db821cfc39a6e00f432f83827f0c&oe=5D99B8DD"
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
for face in faces_hog:
  x = face.left()
  y = face.top()
  w = face.right() - x
  h = face.bottom() - y

  cv2.rectangle(image, (x,y), (x+w,y+h), (0,255,0), 2)

  cv2.imwrite('test.jpg', image)

print(len(faces_hog))
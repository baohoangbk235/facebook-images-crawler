import time
import dlib
import cv2

img_path = '/home/baohoang235/Downloads/images/35.jpg'
# Đọc ảnh đầu vào
image = cv2.imread(img_path)

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

  cv2.imwrite(img_path[0:35] + 'detected_' + img_path[35:], image)

print(len(faces_hog))
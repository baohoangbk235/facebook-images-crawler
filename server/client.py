import requests
import numpy as np 
import os 

def upload(class_dir_name, img_file):
    image = open(img_file,'rb')

    files = {'file': (os.path.basename(img_file), image, 'image/jpg')}

    metadata = {'class': class_dir_name}

    re = requests.post('http://e5ffa4cd.ngrok.io',files=files, data=metadata)

if __name__ == "__main__":
    upload("Big0c3an","/home/baohoang235/Downloads/facebook-images-crawler/server/test3.jpg")
    
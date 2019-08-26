import cv2
import face_recognition
from sklearn.cluster import DBSCAN
from imutils import build_montages
import numpy as np
import argparse
import pickle
import cv2
import matplotlib.pyplot as plt
import os
import shutil

encoding_file = "encodings.pkl"
current_dir = os.getcwd()
images_folder = os.path.join(current_dir, "images")
filtered_folder = os.path.join(current_dir, "filtered_images")

class Clustering():
    def __init__(self):
        self.clt = DBSCAN(eps=0.375,min_samples=10,metric="euclidean", n_jobs=-1)

    def get_encodings(self, facebook_dir):
        data = []
        print("Processing {}...".format(facebook_dir))
        folder = os.path.join(images_folder, facebook_dir)
        images_files = os.listdir(folder)
        imagePaths = [os.path.join(folder, images_file) for images_file in images_files]
        for (i, imagePath) in enumerate(imagePaths):
        # load the input image and convert it from RGB (OpenCV ordering)
        # to dlib ordering (RGB)
            print("[INFO] processing image {}/{}".format(i + 1,
                len(imagePaths)))
            print(imagePath)
            image = cv2.imread(imagePath)
            rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

            # detect the (x, y)-coordinates of the bounding boxes
            # corresponding to each face in the input image
            boxes = face_recognition.face_locations(rgb,
                model="cnn")

            # compute the facial embedding for the face
            encodings = face_recognition.face_encodings(rgb, boxes)

            # build a dictionary of the image path, bounding box location,
            # and facial encodings for the current image
            d = [{"imagePath": imagePath, "loc": box, "encoding": enc}
                for (box, enc) in zip(boxes, encodings)]
            data.extend(d)

        class_filtered_folder = os.path.join(filtered_folder,facebook_dir)

        if not os.path.exists(class_filtered_folder):
            os.mkdir(class_filtered_folder)

        self.clustering(data, class_filtered_folder)

        print("[INFO] serializing encodings...")
        f = open(encoding_file, "wb")
        f.write(pickle.dumps(data))
        f.close()

        return encodings
    
    def clustering(self, data, class_filtered_folder):
        data = np.array(data)
        encodings = [d["encoding"] for d in data]
        encodings = np.asarray(encodings)
        self.clt.fit(encodings)
        labelIDs, count = np.unique(self.clt.labels_, return_counts=True)
        maxLabelID = labelIDs[count.argsort()[-2]]
        print("MaxLabelID : {}".format(maxLabelID))
        numUniqueFaces = len(np.where(labelIDs > -2)[0])
        print("[INFO] # unique faces: {}".format(numUniqueFaces))

        for labelID in labelIDs:
            # find all indexes into the `data` array that belong to the
            # current label ID, then randomly sample a maximum of 25 indexes
            # from the set
            print("[INFO] faces for face ID: {}".format(labelID))
            idxs = np.where(self.clt.labels_ == labelID)[0]
            print(len(idxs))
            idxs = np.random.choice(idxs, size=min(49, len(idxs)),
                replace=False)

            # initialize the list of faces to include in the montage
            faces = []
            # loop over the sampled indexes
            for i in idxs:
                # load the input image and extract the face ROI
                image = cv2.imread(data[i]["imagePath"])
                (top, right, bottom, left) = data[i]["loc"]
                face = image[top:bottom, left:right]

                # force resize the face ROI to 96x96 and then add it to the
                # faces montage list
                face = cv2.resize(face, (96, 96))
                faces.append(face)
                if labelID == maxLabelID:
                    cv2.imwrite(os.path.join(class_filtered_folder,'{}.png'.format(i)), face)

            # create a montage using 96x96 "tiles" with 5 rows and 5 columns
            montage = build_montages(faces, (96, 96), (7, 7))[0]
            
            # show the output montage
            title = "Face ID #{}".format(labelID)
            title = "Unknown Faces" if labelID == -1 else title
            cv2.imshow(title, montage)
            if labelID == maxLabelID:
                cv2.imwrite('test.jpg', montage)
            if cv2.waitKey(0) & 0xFF == ord('q'):
                cv2.destroyAllWindows()

    def filter(self):
        user_list = os.listdir(images_folder)
        for user in user_list:
            self.get_encodings(user)

if __name__ == "__main__":
    cluster = Clustering()
    cluster.get_encodings('congtunamlc.12')


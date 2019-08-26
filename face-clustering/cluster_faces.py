# USAGE
# python cluster_faces.py --encodings encodings.pickle

# import the necessary packages
from sklearn.cluster import DBSCAN
from imutils import build_montages
import numpy as np
import argparse
import pickle
import cv2
import matplotlib.pyplot as plt

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-e", "--encodings", required=True,
	help="path to serialized db of facial encodings")
ap.add_argument("-j", "--jobs", type=int, default=-1,
	help="# of parallel jobs to run (-1 will use all CPUs)")
args = vars(ap.parse_args())

# load the serialized face encodings + bounding box locations from
# disk, then extract the set of encodings to so we can cluster on
# them
print("[INFO] loading encodings...")
data = pickle.loads(open(args["encodings"], "rb").read())
data = np.array(data)
encodings = [d["encoding"] for d in data]
encodings = np.asarray(encodings)

# def k_distances2(x, k):
#     dim0 = x.shape[0]
#     dim1 = x.shape[1]
#     p=-2*x.dot(x.T)+np.sum(x**2, axis=1).T+ np.repeat(np.sum(x**2, axis=1),dim0,axis=0).reshape(dim0,dim0)
#     p = np.sqrt(p)
#     p.sort(axis=1)
#     p=p[:,:k]
#     pm= p.flatten()
#     pm= np.sort(pm)
#     return p, pm
# m, m2= k_distances2(encodings, 128)
# plt.plot(m2)
# plt.ylabel("k-distances")
# plt.grid(True)
# plt.show()

# cluster the embeddings
print("[INFO] clustering...")
clt = DBSCAN(eps=0.375,min_samples=10,metric="euclidean", n_jobs=args["jobs"])
clt.fit(encodings)

# determine the total number of unique faces found in the dataset
labelIDs, count = np.unique(clt.labels_, return_counts=True)
maxLabelID = labelIDs[count.argsort()[-2]]
numUniqueFaces = len(np.where(labelIDs > -1)[0])
print("[INFO] # unique faces: {}".format(numUniqueFaces))

# loop over the unique face integers
for labelID in labelIDs:
	# find all indexes into the `data` array that belong to the
	# current label ID, then randomly sample a maximum of 25 indexes
	# from the set
	print("[INFO] faces for face ID: {}".format(labelID))
	idxs = np.where(clt.labels_ == labelID)[0]
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

	# create a montage using 96x96 "tiles" with 5 rows and 5 columns
	montage = build_montages(faces, (96, 96), (7, 7))[0]
	
	# show the output montage
	title = "Face ID #{}".format(labelID)
	title = "Unknown Faces" if labelID == -1 else title
	cv2.imshow(title, montage)
	if labelID == maxLabelID:
		cv2.imwrite('test3.jpg', montage)
	cv2.waitKey(0)
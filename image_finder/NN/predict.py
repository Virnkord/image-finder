# USAGE
# python predict.py --input output/test_paths.txt

# import the necessary packages
from pyimagesearch import config
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.preprocessing.image import load_img
from tensorflow.keras.models import load_model
import numpy as np
import mimetypes
import argparse
import imutils
import pickle
import cv2
import os


# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--input", required=True,
	help="path to input image/text file of image paths")
ap.add_argument("-t", "--type", required=True,
	help="path to input image/text file of image paths")
args = vars(ap.parse_args())

# determine the input file type, but assume that we're working with
# single input image
filetype = mimetypes.guess_type(args["input"])[0]
imagePaths = [args["input"]]
keyword = args["type"]
keyword = str(keyword)
print(keyword)
# if the file type is a text file, then we need to process *multiple*
# images
if "text/plain" == filetype:
	# load the image paths in our testing file
	imagePaths = open(args["input"]).read().strip().split("\n")

# load our object detector and label binarizer from disk
print("[INFO] loading object detector...")
model = load_model(config.MODEL_PATH)
lb = pickle.loads(open(config.LB_PATH, "rb").read())

# loop over the images that we'll be testing using our bounding box
# regression model
for imagePath in imagePaths:
	# load the input image (in Keras format) from disk and preprocess
	# it, scaling the pixel intensities to the range [0, 1]
	image = load_img(imagePath, target_size=(224, 224))
	image = img_to_array(image) / 255.0
	image = np.expand_dims(image, axis=0)

	# predict the bounding box of the object along with the class
	# label
	(boxPreds, labelPreds) = model.predict(image)
	(startX, startY, endX, endY) = boxPreds[0]

	# determine the class label with the largest predicted
	# probability
	i = np.argmax(labelPreds, axis=1)
	label = lb.classes_[i][0]

	if label == keyword:
		# load the input image (in OpenCV format), resize it such that it
		# fits on our screen, and grab its dimensions
		image = cv2.imread(imagePath)
		image = imutils.resize(image, width=600)
		(h, w) = image.shape[:2]

		# scale the predicted bounding box coordinates based on the image
		# dimensions
		startX = int(startX * w)
		startY = int(startY * h)
		endX = int(endX * w)
		endY = int(endY * h)

		# draw the predicted bounding box and class label on the image
		cropped_image = np.copy(image[startY:endY, startX:endX])
		cv2.imwrite(os.path.join(config.IMAGES_PATH, imagePath[15:]), cropped_image)
	else:
		# print(imagePath[15:], "No")
		os.remove(imagePath)
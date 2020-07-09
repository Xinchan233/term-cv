import argparse

import cv2
from oldcare.facial import FaceUtil
from keras.models import load_model
from keras.preprocessing.image import img_to_array
import numpy as np
from imutils import paths

facial_recognition_model_path = 'models/face_recognition_hog.pickle'
facial_expression_model_path = 'models/face_expression.hdf5'
facial_expression_model = load_model(facial_expression_model_path)
dataset_path = 'images'

image_list = list(paths.list_images(dataset_path))

for image_path in image_list:
    img = cv2.imread(image_path)
    img = cv2.resize(img, (640, 480))
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    faceutil = FaceUtil(facial_recognition_model_path)
    face_location_list, names = faceutil.get_face_location_and_name(img)

    for ((left, top, right, bottom), name) in zip(face_location_list, names):
        roi = gray[top:bottom, left:right]
        roi = cv2.resize(roi, (28, 28))
        roi = roi.astype("float") / 255.0
        roi = img_to_array(roi)
        roi = np.expand_dims(roi, axis=0)

        (disgust, neural, smile) = facial_expression_model.predict(roi)[0]
        if max(disgust, neural, smile) == disgust:
            facial_expression_label = "Disgust"
        elif max(disgust, neural, smile) == neural:
            facial_expression_label = "Neural"
        elif max(disgust, neural, smile) == smile:
            facial_expression_label = "Smile"

        print(facial_expression_label);

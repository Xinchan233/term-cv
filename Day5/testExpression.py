import argparse
from oldcare.facial import FaceUtil
from PIL import Image, ImageDraw, ImageFont
from oldcare.utils import fileassistant
from keras.models import load_model
from keras.preprocessing.image import img_to_array
import cv2
import time
import numpy as np
import os
import imutils
import subprocess

# 全局变量
facial_expression_info_path = 'info/facial_expression_info.csv'
facial_recognition_model_path = 'models/face_recognition_hog.pickle'
facial_expression_model_path = 'models/face_expression.hdf5'
FACIAL_EXPRESSION_TARGET_WIDTH = 28
FACIAL_EXPRESSION_TARGET_HEIGHT = 28

VIDEO_WIDTH = 640
VIDEO_HEIGHT = 480

# 得到 ID->姓名的map 、 ID->职位类型的map、
# 摄像头ID->摄像头名字的map、表情ID->表情名字的map
facial_expression_id_to_name = fileassistant.get_facial_expression_info(
    facial_expression_info_path)

vs = cv2.VideoCapture(0)

# 初始化人脸识别模型
faceutil = FaceUtil(facial_recognition_model_path)
facial_expression_model = load_model(facial_expression_model_path)

while True:
    (grabbed, frame) = vs.read()
    frame = imutils.resize(frame, width=VIDEO_WIDTH,
                           height=VIDEO_HEIGHT)  # 压缩，加快识别速度
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # grayscale，情感分析

    face_location_list, names = faceutil.get_face_location_and_name(frame)

    for ((left, top, right, bottom), name) in zip(face_location_list, names):
        roi = gray[top:bottom, left:right]
        roi = cv2.resize(roi, (FACIAL_EXPRESSION_TARGET_WIDTH,
                               FACIAL_EXPRESSION_TARGET_HEIGHT))
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

        img_PIL = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        draw = ImageDraw.Draw(img_PIL)
        final_label = facial_expression_id_to_name[facial_expression_label]

        draw.text((left, top - 30), final_label,
                  font=ImageFont.truetype('NotoSansCJK-Black.ttc', 40),
                  fill=(255, 0, 0))  # linux

        # 转换回OpenCV格式
        frame = cv2.cvtColor(np.asarray(img_PIL), cv2.COLOR_RGB2BGR)
        # show our detected faces along with smiling/not smiling labels
        cv2.imshow("Checking Strangers and Ole People's Face Expression", frame)
        # Press 'ESC' for exiting video
        k = cv2.waitKey(1) & 0xff
        if k == 27:
            break

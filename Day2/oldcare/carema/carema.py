from time import sleep

import cv2

class Camera:
    cam = cv2.VideoCapture(0)

    def __init__(self):
        self.cam.set(cv2.CAP_PROP_FPS, 5)

    def read(self):
        self.cam.open(0)
        _,img = self.cam.read()
        self.cam.release();
        return _,img

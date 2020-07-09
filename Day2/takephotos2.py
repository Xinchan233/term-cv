# -*- coding: utf-8 -*-
'''
使用Web摄像头 (USB摄像头)捕捉图像并保存
'''

import cv2
import time
from oldcare.carema.carema import Camera
#from oldcare.facial.faceutildlib import FaceUtil
cam = Camera()
while(True):  # 拍100张图片就结束
#    print(2)
    ret, img = cam.read()
    cv2.imshow('img2', img)
    #cv2.imwrite('images/%d.jpg' % (i), img)

    #Press 'ESC' for exiting video
    k = cv2.waitKey(100) & 0xff
    if k == 27:
        break

cv2.destroyAllWindows()
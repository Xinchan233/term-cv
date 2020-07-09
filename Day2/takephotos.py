# -*- coding: utf-8 -*-
'''
使用Web摄像头 (USB摄像头)捕捉图像并保存
'''

import cv2
from oldcare.carema.carema import Camera
import threading

cam = Camera()
while (True):
    ret,img = cam.read()
    if(ret):
        cv2.imshow('img1', img)
    # cv2.imwrite('images/%d.jpg' % (i), img)

    # Press 'ESC' for exiting video
    k = cv2.waitKey(100) & 0xff
    if k == 27:
        break
cv2.destroyAllWindows()

# def fc1():
#     while (True):  # 拍100张图片就结束
#         ret, img = cam.read()
#         cv2.imshow('img1', img)
#         # cv2.imwrite('images/%d.jpg' % (i), img)
#
#         # Press 'ESC' for exiting video
#         k = cv2.waitKey(100) & 0xff
#         if k == 27:
#             break
#     cv2.destroyAllWindows()
#
# def fc2():
#     while (True):  # 拍100张图片就结束
#         ret, img = cam.read()
#         cv2.imshow('img', img)
#         # cv2.imwrite('images/%d.jpg' % (i), img)
#
#         # Press 'ESC' for exiting video
#         k = cv2.waitKey(100) & 0xff
#         if k == 27:
#             break
#     cv2.destroyAllWindows()
#
# if __name__ == '__main__':
#     t1 = threading.Thread(target=fc2)
#     t2 = threading.Thread(target=fc1)
#
#     t1.start()
#     t2.start()
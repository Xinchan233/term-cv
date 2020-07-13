import cv2
import time
import subprocess as sp
import multiprocessing
import psutil
from pusher.streamPusher import stream_pusher

if __name__ == '__main__':
    cap = cv2.VideoCapture(0)
    cap.set(3, 320)
    cap.set(4, 240)
    rtmpUrl = "rtmp://39.100.106.24:1935/stream/camera"
    raw_q = multiprocessing.Queue()
    my_pusher = stream_pusher(rtmp_url=rtmpUrl, raw_frame_q=raw_q,w=320,h=240)
    my_pusher.run()
    while True:
        _, raw_frame = cap.read()
        #cv2.imshow('img',raw_frame)
        info = (raw_frame, '2', '3', '4')
        if not raw_q.full():
            raw_q.put(info)
        cv2.waitKey(100)
    cap.release()
    print('finish')
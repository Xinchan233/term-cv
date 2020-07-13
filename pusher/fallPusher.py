import cv2
import time
import subprocess as sp
import multiprocessing
import psutil
from pusher.streamPusher import stream_pusher

if __name__ == '__main__':
    cap = cv2.VideoCapture('../videos/fall.mp4')
    # while True:
    #     ret, img = cap.read()
    #     cv2.imshow('img',img);
    #     cv2.waitKey(50)
    rtmpUrl = "rtmp://39.100.106.24:1935/stream/fall"
    raw_q = multiprocessing.Queue()
    my_pusher = stream_pusher(rtmp_url=rtmpUrl, raw_frame_q=raw_q, w=640, h=240)
    my_pusher.run()
    while True:
        ret, raw_frame = cap.read()
        if ret:
            cv2.imshow('img',raw_frame)
            raw_frame = cv2.flip(raw_frame, 1)
            info = (raw_frame, '2', '3', '4')
            raw_q.put(info)
        else:
            raw_q.put(None)
            break
        cv2.waitKey(50)

    cap.release()
    print('finish')
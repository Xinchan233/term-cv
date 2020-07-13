import cv2
import time
import subprocess as sp
import multiprocessing
import psutil

class stream_pusher(object):
    def __init__(self, rtmp_url=None, raw_frame_q=None, w=320, h=240):
        self.rtmp_url = rtmp_url
        self.raw_frame_q = raw_frame_q

        fps = 10
        width = w
        height = h

        self.command = ['ffmpeg',
                        '-y',
                        '-f', 'rawvideo',
                        '-vcodec', 'rawvideo',
                        '-pix_fmt', 'bgr24',
                        '-s', "{}x{}".format(width, height),
                        '-r', str(fps),
                        '-i', '-',
                        '-c:v', 'libx264',
                        '-pix_fmt', 'yuv420p',
                        '-preset', 'ultrafast',
                        '-f', 'flv',
                        self.rtmp_url]

    def __frame_handle__(self, raw_frame, text, shape1, shape2):
        return (raw_frame)

    def push_frame(self):
        p = psutil.Process()
        p.cpu_affinity([0, 1, 2, 3])
        p = sp.Popen(self.command, stdin=sp.PIPE)

        while True:
            if not self.raw_frame_q.empty():
                raw_frame, text, shape1, shape2 = self.raw_frame_q.get()
                frame = self.__frame_handle__(raw_frame, text, shape1, shape2)
                p.stdin.write(frame.tostring())
            else:
                time.sleep(0.01)

    def run(self):
        push_frame_p = multiprocessing.Process(target=self.push_frame, args=())
        push_frame_p.daemon = True
        push_frame_p.start()


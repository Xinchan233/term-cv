import cv2

vs = cv2.VideoCapture('rtmp://39.100.106.24:1935/stream/pupils_trace')

while True:
    ret,img = vs.read()
    if ret:
        cv2.imshow('img',img)

    k = cv2.waitKey(100) & 0xff
    if k == 27:
        break
cv2.destroyAllWindows()
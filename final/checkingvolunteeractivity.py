# -*- coding: utf-8 -*-
'''
义工是否和老人有互动主程序

用法：
python checkingvolunteeractivity.py
python testingvolunteeractivity.py --filename tests/desk_01.mp4
1.当义工不存在时候，重置互动插入
2.当义工和老人距离超过规定距离，重置互动插入
'''
import pymysql

from oldcare.facial import FaceUtil
from scipy.spatial import distance as dist
from oldcare.utils import fileassistant
from PIL import Image, ImageDraw, ImageFont
import cv2
import time
import imutils
import numpy as np
import argparse

# 传入参数
ap = argparse.ArgumentParser()
ap.add_argument("-f", "--filename", required=False, default='',
                help="")
args = vars(ap.parse_args())
db = pymysql.connect(host='123.57.246.9', user='root', password='199918', port=3306,
                     db='oldcare', charset='utf8')
cursor = db.cursor()
# 全局变量
output_interact_path = 'supervision/interact'
interact_timing = 0  # 计时开始
interact_start_time = 0  # 开始时间
interact_limit_time = 4  # if >= 2 seconds, he/she is smiling
pixel_per_metric = None
input_video = args['filename']
model_path = 'models/face_recognition_hog.pickle'
people_info_path = 'info/people_info.csv'

# 全局常量
FACE_ACTUAL_WIDTH = 20  # 单位厘米   姑且认为所有人的脸都是相同大小
VIDEO_WIDTH = 640
VIDEO_HEIGHT = 480
ACTUAL_DISTANCE_LIMIT = 100  # cm
flag = 1

# 得到 ID->姓名的map 、 ID->职位类型的map
id_card_to_name, id_card_to_type = fileassistant.get_people_info(
    people_info_path)

# 初始化摄像头
if not input_video:
    vs = cv2.VideoCapture('rtmp://39.100.106.24:1935/stream/pupils_trace')
    time.sleep(2)
else:
    vs = cv2.VideoCapture(input_video)

# 加载模型
faceutil = FaceUtil(model_path)

print('[INFO] 开始检测义工和老人是否有互动...')
# 不断循环
counter = 0
while True:
    counter += 1
    # grab the current frame
    (grabbed, frame) = vs.read()
    vs.grab()
    vs.grab()
    vs.grab()
    vs.grab()
    vs.grab()

    # if we are viewing a video and we did not grab a frame, then we
    # have reached the end of the video
    if input_video and not grabbed:
        break

    if not input_video:
        frame = cv2.flip(frame, 1)

    frame = imutils.resize(frame,
                           width=VIDEO_WIDTH,
                           height=VIDEO_HEIGHT)  # 压缩，加快识别速度

    face_location_list, names = faceutil.get_face_location_and_name(
        frame)

    people_type_list = list(set([id_card_to_type[i] for i in names]))

    volunteer_centroids = []
    old_people_centroids = []
    old_people_name = []

    # loop over the face bounding boxes
    for ((left, top, right, bottom), name) in zip(face_location_list,
                                                  names):  # 处理单个人

        person_type = id_card_to_type[name]
        # 将人脸框出来
        rectangle_color = (0, 0, 255)
        if person_type == 'old_people':
            rectangle_color = (0, 0, 128)
        elif person_type == 'employee':
            rectangle_color = (255, 0, 0)
        elif person_type == 'volunteer':
            rectangle_color = (0, 255, 0)
        else:
            pass

        cv2.rectangle(frame, (left, top), (right, bottom),
                      rectangle_color, 2)

        if 'volunteer' not in people_type_list:  # 如果无义工则跳出循环
            flag = 1
            interact_timing = 0
            continue

        if person_type == 'volunteer':  # 如果检测到有义工存在
            # 获得义工位置
            volunteer_face_center = (int((right + left) / 2),
                                     int((top + bottom) / 2))
            volunteer_centroids.append(volunteer_face_center)

            cv2.circle(frame,
                       (volunteer_face_center[0],
                        volunteer_face_center[1]),
                       8, (255, 0, 0), -1)
        elif person_type == 'old_people':  # 如果没有发现义工
            old_people_face_center = (int((right + left) / 2),
                                      int((top + bottom) / 2))
            old_people_centroids.append(old_people_face_center)
            old_people_name.append(name)

            cv2.circle(frame,
                       (old_people_face_center[0],
                        old_people_face_center[1]),
                       4, (0, 255, 0), -1)
        else:
            pass

        # 把人名写上(同时处理中文显示问题)
        img_PIL = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        draw = ImageDraw.Draw(img_PIL)
        final_label = id_card_to_name[name]
        draw.text((left, top - 30), final_label,
                  font=ImageFont.truetype('NotoSansCJK-Black.ttc',
                                          40), fill=(255, 0, 0))  # linux
        # 转换回OpenCV格式
        frame = cv2.cvtColor(np.asarray(img_PIL), cv2.COLOR_RGB2BGR)

    # 在义工和老人之间划线
    for i in volunteer_centroids:
        for j_index, j in enumerate(old_people_centroids):
            pixel_distance = dist.euclidean(i, j)
            face_pixel_width = sum([i[2] - i[0] for i in face_location_list]) / len(face_location_list)  # avg
            pixel_per_metric = face_pixel_width / FACE_ACTUAL_WIDTH
            actual_distance = pixel_distance / pixel_per_metric

            if actual_distance < ACTUAL_DISTANCE_LIMIT:
                cv2.line(frame, (int(i[0]), int(i[1])),
                         (int(j[0]), int(j[1])), (255, 0, 255), 2)
                label = 'distance: %dcm' % (actual_distance)
                cv2.putText(frame, label, (frame.shape[1] - 150, 30),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                            (0, 0, 255), 2)

                if interact_timing == 0:  # just start timing
                    print("1")
                    interact_timing = 1
                    interact_start_time = time.time()
                else:  # already started timing
                    print("2")
                    interact_end_time = time.time()
                    difference = interact_end_time - interact_start_time

                    current_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
                    if difference < interact_limit_time:
                        print('[INFO] %s, 房间桌子, %s仅交互了 %.1f 秒. 忽略' % (
                            current_time, id_card_to_name[old_people_name[j_index]], difference))
                    else:  # he/she is really smiling

                        current_time = time.strftime('%Y-%m-%d %H:%M:%S',
                                                     time.localtime(time.time()))
                        img_name = 'snapshot_%s.jpg' % (time.strftime('%Y%m%d_%H%M%S'))
                        cv2.imwrite(cv2.os.path.join(output_interact_path,
                                                     img_name), frame)
                        path = output_interact_path + "/" + img_name
                        myimg = open(path, 'rb')
                        img_data = myimg.read()
                        if (flag == 1):
                            event_desc = '%s正在与义工交互' % (id_card_to_name[old_people_name[j_index]])
                            event_location = '房间桌子'
                            print('[EVENT] %s, 房间桌子, %s正在与义工交互.' % (
                                current_time, id_card_to_name[old_people_name[j_index]]))
                            print(id_card_to_name[old_people_name[j_index]])
                            name= id_card_to_name[old_people_name[j_index]]
                            try:
                                cursor.execute(
                                    "insert into event_info(event_date,event_type,event_desc,event_location,oldperson_name,image) value(now(),0,'老人正在与义工交互','房间桌子',%s,%s)" , (
                                        name, img_data))
                                print('Successful')
                                db.commit()
                            except:
                                print('Failed')
                                db.rollback()
                            flag = 0

                        print('[EVENT] %s, 房间桌子, %s 正在与义工交互.'
                              % (current_time,
                                 id_card_to_name[old_people_name[j_index]]))


            else:
                flag = 1
                interact_timing = 0

    # show our detected faces along with smiling/not smiling labels
    cv2.imshow("Checking Volunteer's Activities", frame)

    # Press 'ESC' for exiting video
    k = cv2.waitKey(1) & 0xff
    if k == 27:
        break

# cleanup the camera and close any open windows
vs.release()
cv2.destroyAllWindows()

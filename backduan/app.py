import pymysql
import smtplib
from email.mime.text import MIMEText
import numpy as np
import os
import operator
import glob
from flask import Flask, render_template, Response, request, jsonify, Blueprint, make_response
import cv2
from flask_cors import CORS
import config
from exts import db
from model import test_user, test_warning_info
import _json
import json
import time
import logging
from flask_sqlalchemy import SQLAlchemy
import random
import multiprocessing as mp
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

app = Flask(__name__)
CORS(app, supports_credentials=True)  # 跨域
app.config.from_object(config)  # 加载数据库配置文件

db.init_app(app)  # 绑定到我们到应用程序
# db = SQLAlchemy(app)
staff = Blueprint('staff', __name__)
record = Blueprint('record', __name__)



# VideoCapture可以读取从url、本地视频文件以及本地摄像头的数据
# camera = cv2.VideoCapture('rtsp://admin:admin@172.21.182.12:554/cam/realmonitor?channel=1&subtype=1')
# camera = cv2.VideoCapture('test.mp4')
# camera = cv2.VideoCapture(0)

# 全局警告信息
# warninginfo = [[] * 4] * 500
# count = 0
CorrectVerificationCode = 0
alert_info = False
nums = 1
num1 = 0
num2 = 0
qq = 0
qp = 0
names = 'unKnown'
op = 'unKnown'
images = []
classNames = []
path = r'E:\Python\xiaoxueqi\xiaoxueqi\data1'
myList = os.listdir(path)
print(myList)
tx = 1
tp = 0
tr = ''
n = [[1, 2], [100, 120], [150, 130], [300, 200], [400, 50]]
q = [[1, 2], [100, 120], [150, 130], [300, 200], [400, 50]]


def getVideo():
    img_root = 'E:/Python/xiaoxueqi/xiaoxueqi/'  # 是图片序列的位置
    fps = 10  # 可以随意调整视频的帧速率

    # 可以用(*'DVIX')或(*'X264'),如果都不行先装ffmepg
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    videoWriter = cv2.VideoWriter('TestVideo.avi', fourcc, fps, (352, 288), True)  # 最后一个是保存图片的尺寸
    path_file_number = glob.glob('E:/Python/xiaoxueqi/xiaoxueqi/*.jpg')  # 或者指定文件下个数
    print(path_file_number)
    for i in range(len(path_file_number) + 1):
        frame = cv2.imread(img_root + str(i + 1) + '.jpg')
        # print(frame.shape)

        videoWriter.write(frame)


def getVideo2():
    img_root = 'C:/Users/akc/PycharmProjects/pythonProject2/opencv/data1'  # 是图片序列的位置
    fps = 10  # 可以随意调整视频的帧速率

    # 可以用(*'DVIX')或(*'X264'),如果都不行先装ffmepg
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    videoWriter = cv2.VideoWriter('C:/Users/akc/PycharmProjects/pythonProject2/opencv/data1/TestVideo2.avi', fourcc,
                                  fps, (352, 288), True)  # 最后一个是保存图片的尺寸
    path_file_number = glob.glob('C:/Users/akc/PycharmProjects/pythonProject2/opencv/data1/*.jpg')  # 或者指定文件下个数
    for i in range(len(path_file_number) + 1):
        frame = cv2.imread(img_root + str(i + 1) + '.jpg')
        # print(frame.shape)

        videoWriter.write(frame)


# 报警发送邮件
def send_email():
    mail_host = 'smtp.163.com'
    # 163用户名
    mail_user = 'tjsghj'
    # 密码(部分邮箱为授权码)
    mail_pass = 'UEYTOKGEXOZLFYSS'
    # 邮件发送方邮箱地址
    sender = 'tjsghj@163.com'

    # type:str
    # emailaddr = request.POST.get('emailAddress')
    # 邮件接受方邮箱地址，注意需要[]包裹，这意味着你可以写多个邮件地址群发
    receivers = ['19301100@bjtu.edu.cn']

    content = '【鹰眼入侵检测系统】有入侵！请及时查看！'

    # 设置email信息
    # 邮件内容设置
    message = MIMEText(content, 'plain', 'utf-8')
    # 邮件主题
    message['Subject'] = '鹰眼入侵检测系统入侵检测'
    # 发送方信息
    message['From'] = sender
    # 接受方信息
    message['To'] = receivers[0]

    # 登录并发送邮件
    try:
        smtpObj = smtplib.SMTP()
        # 连接到服务器
        smtpObj.connect(mail_host, 25)
        # 登录到服务器
        smtpObj.login(mail_user, mail_pass)
        # 发送
        smtpObj.sendmail(
            sender, receivers, message.as_string())
        # 退出
        smtpObj.quit()

    except smtplib.SMTPException as e:
        print('error', e)  # 打印错误


def gen_frames():
    camera = cv2.VideoCapture('rtsp://192.168.28.104:8554/live')
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read('trainer/trainer.yml')
    cascadePath = r"E:\Python\Lib\site-packages\cv2\data\haarcascade_frontalface_alt.xml"
    faceCascade = cv2.CascadeClassifier(cascadePath);

    font = cv2.FONT_HERSHEY_SIMPLEX

    # iniciate id counter
    id = 0

    # names related to ids: example ==> Marcelo: id=1,  etc
    names = ['None', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj',
             'cwj', 'cwj', 'cwj'
        , 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj',
             'cwj', 'cwj', 'cwj'
        , 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj',
             'cwj', 'cwj', 'cwj'
        , 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj',
             'cwj', 'cwj', 'cwj'
        , 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj',
             'cwj', 'cwj', 'cwj'
        , 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj',
             'cwj', 'cwj', 'cwj'
        , 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj',
             'cwj', 'cwj', 'cwj'
        , 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj',
             'cwj', 'cwj', 'cwj'
        , 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj',
             'cwj', 'cwj', 'cwj'
        , 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj',
             'cwj', 'cwj', 'cwj'
        , 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj',
             'cwj', 'cwj', 'cwj'
        , 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj',
             'cwj', 'cwj', 'cwj'
        , 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj',
             'cwj', 'cwj', 'cwj'
        , 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj',
             'cwj', 'cwj', 'cwj'
        , 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj',
             'cwj', 'cwj', 'cwj'
        , 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj',
             'cwj', 'cwj', 'cwj'
        , 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj',
             'cwj', 'cwj', 'cwj'
        , 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj',
             'cwj', 'cwj', 'cwj'
        , 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj',
             'cwj', 'cwj', 'cwj'
        , 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj',
             'cwj', 'cwj', 'cwj'
        , 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj']
    minW = 0.1 * camera.get(3)
    minH = 0.1 * camera.get(4)
    width = (int(camera.get(cv2.CAP_PROP_FRAME_WIDTH)))
    height = (int(camera.get(cv2.CAP_PROP_FRAME_HEIGHT)))
    # 测试用,查看视频size
    size = (int(camera.get(cv2.CAP_PROP_FRAME_WIDTH)),
            int(camera.get(cv2.CAP_PROP_FRAME_HEIGHT)))
    print('size:' + repr(size))

    fgbg = cv2.createBackgroundSubtractorMOG2()
    num = 0

    time1 = time3 = time.time()
    while True:
        global nums, op, num1, q, qq
        nums = nums + 1
        m1 = []
        c1 = []
        m = []
        c = []
        for a in n:
            m.append(a[0])
        max_index, max_number = max(enumerate(m), key=operator.itemgetter(1))
        min_index, min_number = min(enumerate(m), key=operator.itemgetter(1))
        for b in n:
            c.append(b[1])
        max_1, max_2 = max(enumerate(c), key=operator.itemgetter(1))
        min_1, min_2 = min(enumerate(c), key=operator.itemgetter(1))
        for e in q:
            m1.append(e[0])
        maxindex, maxnumber = max(enumerate(m1), key=operator.itemgetter(1))
        minindex, minnumber = min(enumerate(m1), key=operator.itemgetter(1))
        for d in q:
            c1.append(d[1])
        max1, max2 = max(enumerate(c1), key=operator.itemgetter(1))
        min1, min2 = min(enumerate(c1), key=operator.itemgetter(1))
        # 读取视频流

        try:
            grabbed, frame_lwpCV = camera.read()
            global alert_info
            alert_info = False
            gray = cv2.cvtColor(frame_lwpCV, cv2.COLOR_BGR2GRAY)
        except Exception:
            pass

        faces = faceCascade.detectMultiScale(
            gray,
            scaleFactor=1.2,
            minNeighbors=5,
            minSize=(int(minW), int(minH)),
        )

        for (x, y, w, h) in faces:

            id, confidence = recognizer.predict(gray[y:y + h, x:x + w])

            # Check if confidence is less them 100 ==> "0" is perfect match
            if (confidence < 100):
                id = names[id]
                print(str(id))
                confidence = "  {0}%".format(round(100 - confidence))
            else:
                id = "unknown"
                print(str(id))
                confidence = "  {0}%".format(round(100 - confidence))

        background = None

        if frame_lwpCV is None:
            break

        # (success, boxes) = trackers.update(frame_lwpCV)

        # 对帧进行预处理，先转灰度图，再进行高斯滤波。
        # 用高斯滤波进行模糊处理，进行处理的原因：每个输入的视频都会因自然震动、光照变化或者摄像头本身等原因而产生噪声。对噪声进行平滑是为了避免在运动和跟踪时将其检测出来。
        # gray_lwpCV = cv2.cvtColor(frame_lwpCV, cv2.COLOR_BGR2GRAY)
        # gray_lwpCV = cv2.GaussianBlur(gray_lwpCV, (11, 11), 0)
        #
        # # 将第一帧设置为整个输入的背景
        # if background is None:
        #     background = gray_lwpCV
        #     continue
        # diff = cv2.absdiff(background, gray_lwpCV)
        fgamsk = fgbg.apply(frame_lwpCV)

        # 显示矩形框
        contours, hierarchy = cv2.findContours(fgamsk, cv2.RETR_EXTERNAL,
                                               cv2.CHAIN_APPROX_SIMPLE)  # 该函数计算一幅图像中目标的轮廓

        mark = 0

        for c in contours:
            if cv2.contourArea(c) < 3200:  # 对于矩形区域，只显示大于给定阈值的轮廓，所以一些微小的变化不会显示。对于光照不变和噪声低的摄像头可不设定轮廓最小尺寸的阈值
                continue
            (x, y, w, h) = cv2.boundingRect(c)  # 该函数计算矩形的边界框
            count = 0

            # objects = ct.update(cv2.boundingRect(c))
            # # 循环跟踪对象
            # for (objectID, centroid) in objects.items():
            #     # 在输出帧上绘制对象的ID和对象的质心
            #     text = "ID {}".format(objectID)
            #     cv2.putText(frame_lwpCV, text, (centroid[0] - 10, centroid[1] - 10),
            #                 cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
            #     cv2.circle(frame_lwpCV, (centroid[0], centroid[1]), 4, (0, 255, 0), -1)
            if (y > max_2) or (x > max_number) or (y + h < min_2) or (x + w < min_number) or id != "unknown":
                cv2.rectangle(frame_lwpCV, (x, y), (x + w, y + h), (0, 255, 0), 2)

                alert_info = False

            else:
                time2 = time.time()
                alert_info = True
                qq += 1
                filename = "%s.jpg" % qq
                cv2.imwrite(filename, frame_lwpCV)
                warning = test_warning_info(date=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
                                            start_time=time.strftime("%H:%M:%S", time.localtime()),
                                            camera=1,
                                            imgurl="/image/1/" + "%s" % qq
                                            )
                db.session.add(warning)
                db.session.commit()
                if time2 - time1 > 5:
                    time1 = time2

                    cv2.rectangle(frame_lwpCV, (x, y), (x + w, y + h), (0, 0, 255), 2)
                    # # 获取截图路径并在下面数据库中保存路径
                    # num = num + 1
                    # filename = "\camera1" + "%s.jpg" % num
                    # cv2.imwrite(r"E:\Python\xiaoxueqi\xiaoxueqi\img" + filename, frame_lwpCV)
                    # #
                    # date = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
                    # start_time = time.strftime("%H:%M:%S", time.localtime()),
                    # camera = 1,
                    # imgurl = "/image/1/" + "%s" % num
                    # date = str(date)
                    # start_time = str(start_time)
                    # camera = str(camera)
                    # imgurl = str(imgurl)
                    # 存入数据库


                    # warninginfo[count].append(date)
                    # warninginfo[count].append(start_time)
                    # warninginfo[count].append(camera)
                    # # warninginfo[count].append(imgurl)
                    # count = count + 1

                    # db1 = pymysql.connect(host="localhost", user="root", password="tyl20001206llh",
                    #                       db="systemdata")
                    # cursor = db1.cursor()
                    # # sql = "INSERT INTO test_warning_info \ VALUES (%s, %s, %s, %s)" % (pymysql.escape_string(date),
                    # # pymysql.escape_string(start_time), pymysql.escape_string(camera), pymysql.escape_string(imgurl))
                    # sql = """INSERT INTO test_warning_info (
                    #     date, start_time, camera, imgurl) values('123','liu','1234','123')"""
                    # cursor.execute(sql)
                    # db1.commit()
                    # db1.close()

                else:
                    cv2.rectangle(frame_lwpCV, (x, y), (x + w, y + h), (0, 0, 255), 2)

                if time2 - time3 > 30:
                    time3 = time2
                    send_email()

        print("n:", n)
        pts = np.array(n, np.int32)
        cv2.polylines(frame_lwpCV, [pts], True, (255, 0, 0), 3)

        if nums % 20 == 0:
            id = 'unknown'
        ret, jpeg = cv2.imencode('.jpg', frame_lwpCV)
        frame = jpeg.tobytes()
        key1 = cv2.waitKey(100) & 0xFF

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

        if nums % 50 != 0:
            continue
        getVideo()


def gen_frames2():
    camera = cv2.VideoCapture('rtsp://192.168.43.217:8554/live')
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read('trainer/trainer.yml')
    cascadePath = r"E:\Python\Lib\site-packages\cv2\data\haarcascade_frontalface_alt.xml"
    faceCascade = cv2.CascadeClassifier(cascadePath);

    font = cv2.FONT_HERSHEY_SIMPLEX

    # iniciate id counter
    id = 0

    # names related to ids: example ==> Marcelo: id=1,  etc
    names = ['None', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj',
             'cwj', 'cwj', 'cwj'
        , 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj',
             'cwj', 'cwj', 'cwj'
        , 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj',
             'cwj', 'cwj', 'cwj'
        , 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj',
             'cwj', 'cwj', 'cwj'
        , 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj',
             'cwj', 'cwj', 'cwj'
        , 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj',
             'cwj', 'cwj', 'cwj'
        , 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj',
             'cwj', 'cwj', 'cwj'
        , 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj',
             'cwj', 'cwj', 'cwj'
        , 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj',
             'cwj', 'cwj', 'cwj'
        , 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj',
             'cwj', 'cwj', 'cwj'
        , 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj',
             'cwj', 'cwj', 'cwj'
        , 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj',
             'cwj', 'cwj', 'cwj'
        , 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj',
             'cwj', 'cwj', 'cwj'
        , 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj',
             'cwj', 'cwj', 'cwj'
        , 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj',
             'cwj', 'cwj', 'cwj'
        , 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj',
             'cwj', 'cwj', 'cwj'
        , 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj',
             'cwj', 'cwj', 'cwj'
        , 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj',
             'cwj', 'cwj', 'cwj'
        , 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj',
             'cwj', 'cwj', 'cwj'
        , 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj',
             'cwj', 'cwj', 'cwj'
        , 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj', 'cwj']
    minW = 0.1 * camera.get(3)
    minH = 0.1 * camera.get(4)
    width = (int(camera.get(cv2.CAP_PROP_FRAME_WIDTH)))
    height = (int(camera.get(cv2.CAP_PROP_FRAME_HEIGHT)))
    # 测试用,查看视频size
    size = (int(camera.get(cv2.CAP_PROP_FRAME_WIDTH)),
            int(camera.get(cv2.CAP_PROP_FRAME_HEIGHT)))
    print('size:' + repr(size))

    fgbg = cv2.createBackgroundSubtractorMOG2()

    while True:
        global nums, op, num1, q, qp
        nums = nums + 1
        m1 = []
        c1 = []

        for e in q:
            m1.append(e[0])
        maxindex, maxnumber = max(enumerate(m1), key=operator.itemgetter(1))
        minindex, minnumber = min(enumerate(m1), key=operator.itemgetter(1))
        for d in q:
            c1.append(d[1])
        max1, max2 = max(enumerate(c1), key=operator.itemgetter(1))
        min1, min2 = min(enumerate(c1), key=operator.itemgetter(1))
        # 读取视频流

        try:
            grabbed, frame_lwpCV = camera.read()

            gray = cv2.cvtColor(frame_lwpCV, cv2.COLOR_BGR2GRAY)
        except Exception:
            pass

        faces = faceCascade.detectMultiScale(
            gray,
            scaleFactor=1.2,
            minNeighbors=5,
            minSize=(int(minW), int(minH)),
        )

        for (x, y, w, h) in faces:

            id, confidence = recognizer.predict(gray[y:y + h, x:x + w])

            # Check if confidence is less them 100 ==> "0" is perfect match
            if (confidence < 70):
                id = names[id]
                print(str(id))
                confidence = "  {0}%".format(round(100 - confidence))
            else:
                id = "unknown"
                print(str(id))
                confidence = "  {0}%".format(round(100 - confidence))

        background = None

        if frame_lwpCV is None:
            break

        # (success, boxes) = trackers.update(frame_lwpCV)

        # 对帧进行预处理，先转灰度图，再进行高斯滤波。
        # 用高斯滤波进行模糊处理，进行处理的原因：每个输入的视频都会因自然震动、光照变化或者摄像头本身等原因而产生噪声。对噪声进行平滑是为了避免在运动和跟踪时将其检测出来。
        # gray_lwpCV = cv2.cvtColor(frame_lwpCV, cv2.COLOR_BGR2GRAY)
        # gray_lwpCV = cv2.GaussianBlur(gray_lwpCV, (11, 11), 0)
        #
        # # 将第一帧设置为整个输入的背景
        # if background is None:
        #     background = gray_lwpCV
        #     continue
        # diff = cv2.absdiff(background, gray_lwpCV)
        fgamsk = fgbg.apply(frame_lwpCV)

        # 显示矩形框
        contours, hierarchy = cv2.findContours(fgamsk, cv2.RETR_EXTERNAL,
                                               cv2.CHAIN_APPROX_SIMPLE)  # 该函数计算一幅图像中目标的轮廓

        mark = 0
        global alert_info
        for c in contours:
            if cv2.contourArea(c) < 3200:  # 对于矩形区域，只显示大于给定阈值的轮廓，所以一些微小的变化不会显示。对于光照不变和噪声低的摄像头可不设定轮廓最小尺寸的阈值
                continue
            (x, y, w, h) = cv2.boundingRect(c)  # 该函数计算矩形的边界框
            count = 0

            # objects = ct.update(cv2.boundingRect(c))
            # # 循环跟踪对象
            # for (objectID, centroid) in objects.items():
            #     # 在输出帧上绘制对象的ID和对象的质心
            #     text = "ID {}".format(objectID)
            #     cv2.putText(frame_lwpCV, text, (centroid[0] - 10, centroid[1] - 10),
            #                 cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
            #     cv2.circle(frame_lwpCV, (centroid[0], centroid[1]), 4, (0, 255, 0), -1)

            if (y > max2) or (x > maxnumber) or (y + h < min2) or (x + w < minnumber) or id != "unknown":
                cv2.rectangle(frame_lwpCV, (x, y), (x + w, y + h), (0, 255, 0), 2)

                alert_info = False

            else:

                alert_info = True
                cv2.rectangle(frame_lwpCV, (x, y), (x + w, y + h), (0, 0, 255), 2)
                qp += 1
                filename = r"E:\Python\xiaoxueqi\xiaoxueqi\data1\%s.jpg" % qp
                cv2.imwrite(filename, frame_lwpCV)

        print("q:", q)
        pts = np.array(q, np.int32)
        cv2.polylines(frame_lwpCV, [pts], True, (255, 0, 0), 3)

        if nums % 50 == 0:
            id = 'unknown'
        ret, jpeg = cv2.imencode('.jpg', frame_lwpCV)
        frame = jpeg.tobytes()
        key1 = cv2.waitKey(100) & 0xFF

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
        if nums % 50 != 0:
            continue
        getVideo2()


def run_multi_camera():
    # user_name, user_pwd = "admin", "password"
    user_name, user_pwd = "", ""
    camera_ip_l = [
        "192.168.43.1:8554",  # ipv4（改成自己的）
        "192.168.43.26:8554",  # ipv4（改成自己的）
        # 把你的摄像头的地址放到这里，如果是ipv6，那么需要加一个中括号。
    ]

    mp.set_start_method(method='spawn')  # init
    queues = [mp.Queue(maxsize=2) for _ in camera_ip_l]
    i = 0
    processes = []
    for queue, camera_ip in zip(queues, camera_ip_l):
        if i == 1:
            processes.append(mp.Process(target=gen_frames(), args=()))
        if i == 0:
            processes.append(mp.Process(target=gen_frames2(), args=()))

            i = 1
    for process in processes:
        process.daemon = True
        process.start()
    for process in processes:
        process.join()


# 摄像头1
@app.route('/video_start1', methods=['GET', 'POST'])
def video_start():
    # 通过将一帧帧的图像返回，就达到了看视频的目的。multipart/x-mixed-replace是单次的http请求-响应模式，如果网络中断，会导致视频流异常终止，必须重新连接才能恢复

    if request.method == "GET":
        return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


# 摄像头2
@app.route('/video_start2', methods=['GET', 'POST'])
def video_start2():
    # 通过将一帧帧的图像返回，就达到了看视频的目的。multipart/x-mixed-replace是单次的http请求-响应模式，如果网络中断，会导致视频流异常终止，必须重新连接才能恢复

    if request.method == "GET":
        return Response(gen_frames2(), mimetype='multipart/x-mixed-replace; boundary=frame')


# 发送警告信息
@app.route('/alert', methods=['GET', 'POST'])
def send_alert():
    # 返回全局变量，实现发送报警信息
    global alert_info
    if request.method == "GET":
        if alert_info == True:
            return jsonify({"code": 20000, "value": 20000, "data": "warning"})
        else:
            return jsonify({"code": 20000, "value": 10000, "data": "safe"})

def gen():
    camera = cv2.VideoCapture('TestVideo.avi')
    while True:
        grab, frame_lwpCV = camera.read()
        ret, jpeg = cv2.imencode('.jpg', frame_lwpCV)
        frame = jpeg.tobytes()
        key1 = cv2.waitKey(100) & 0xFF

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

# 获取视频回放
@app.route('/video', methods=['GET', 'POST'])
def getVideo123():
    if request.method == "GET":
        return Response(gen(), mimetype='multipart/x-mixed-replace; boundary=frame')


# 获取任意警报区域
@app.route('/drawarea', methods=['GET', 'POST'])
def drawarea():
    if request.method == "POST":
        data = request.get_json()
        # data_ = request.form.get('data')
        # data = json.loads(data_)
        camera = data['camera']
        point = data['point']

        # 添加到改变区域的全局变量
        if camera == 1:
            global n
            print(point)  # 修改1号摄像头的全局变量
            n = point
        else:
            global q
            print(point)  # 修改2号摄像头的全局变量
            q = point

        return jsonify({"code": 20000, "data": "success"})


@app.route('/')
def index():
    return render_template('index.html')


# 注销
@app.route('/logout', methods=['GET', 'POST'])
def logout():
    return jsonify({"code": 20000, "data": "success"})


# 登录
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.get_json()
        # data_ = request.form.get('data')
        # data = json.loads(data_)
        username = data['username']
        password = data['password']
        # print(request.form)
        # username = request.form.get('username')
        # password = request.form.get('password')
        print(username)
        print(password)
        users = test_user.query.all()
        print(users)
        for user in users:
            if user.username == username and user.password == password:
                return jsonify({"code": 20000, "data": user.permissions})
            else:
                continue
        return jsonify({"code": 60204, "message": 'Account and password are incorrect.'})

    else:
        token = request.args.get('token')
        if token == 'admin-token':
            return jsonify({"code": 20000, "data": {"roles": ['admin'], "introduction": 'I am a super administrator',
                                                    "avatar": 'https://wpimg.wallstcn.com/f778738c-e4f8-4870-b634'
                                                              '-56703b4acafe.gif',
                                                    "name": 'Super Admin'}})
        else:
            return jsonify({"code": 20000, "data": {'roles': ['editor'],
                                                    'introduction': 'I am an editor',
                                                    'avatar': 'https://wpimg.wallstcn.com/f778738c-e4f8-4870-b634-56703b4acafe.gif',
                                                    'name': 'Normal Editor'}})


# 注册
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        data = request.get_json()
        print(data)
        username = data['username']
        password = data['password']
        id = data['id']
        id = int(id)
        print(id)
        email = data['email']
        ver = data['verification']
        ver = int(ver)
        print(ver)
        # username = request.form.get('username')
        # password = request.form.get('password')
        # realname = request.form.get('realname')
        # email = request.form.get('email')

        global CorrectVerificationCode
        users = test_user.query.all()
        for user in users:
            print(user.id)
            print(user.username)
            print(id)
            if user.id == id and CorrectVerificationCode == ver:
                if user.username != username:
                    db = pymysql.connect(host="localhost", user="root", password="tyl20001206llh", db="systemdata")
                    cursor = db.cursor()
                    sql = "UPDATE test_user SET username = '%s', password = '%s', email = '%s' WHERE id = '%s'" % (
                        username, password, email, id)
                    cursor.execute(sql)
                    db.commit()
                    return jsonify({"code": 20000, "data": "success"})
                else:
                    return jsonify({"code": 10000, "data": "username is exist"})
            else:
                continue
        return jsonify({"code": 10000, "data": "id is not the same"})


# 获取图片
@app.route('/image/<cameraid>/<string:filename>', methods=['GET'])
def display_img(cameraid, filename):
    if request.method == 'GET':
        if filename is None:
            pass
        else:
            image = open(r"E:\Python\xiaoxueqi\xiaoxueqi" + r"\{}.jpg".format(filename), 'rb')
            resp = Response(image, mimetype="image/jpeg")
            return resp


# 发送验证码
@app.route('/sendemail', methods=['GET', 'POST'])
def send_emailMessage():
    if request.method == 'POST':
        data = request.get_json()
        email = data['email']
        print(email)
        mail_host = 'smtp.163.com'
        # 163用户名
        mail_user = 'tjsghj'
        # 密码(部分邮箱为授权码)
        mail_pass = 'UEYTOKGEXOZLFYSS'
        # 邮件发送方邮箱地址
        sender = 'tjsghj@163.com'

        # 邮件接受方邮箱地址，注意需要[]包裹，这意味着你可以写多个邮件地址群发
        receivers = [email]

        randomNumber = random.randint(1000, 9999)
        global CorrectVerificationCode
        CorrectVerificationCode = randomNumber
        randomNumberStr = str(randomNumber)
        content = '【鹰眼入侵检测系统】您的验证码是' + randomNumberStr + '。如非本人操作，请忽略本邮件'
        print(randomNumber)
        print(CorrectVerificationCode)

        # 设置email信息
        # 邮件内容设置
        message = MIMEText(content, 'plain', 'utf-8')
        # 邮件主题
        message['Subject'] = '鹰眼入侵检测系统验证码'
        # 发送方信息
        message['From'] = sender
        # 接受方信息
        message['To'] = receivers[0]

        # 登录并发送邮件
        try:
            smtpObj = smtplib.SMTP()
            # 连接到服务器
            print(2)
            smtpObj.connect(mail_host, 25)
            # 登录到服务器
            print(3)
            smtpObj.login(mail_user, mail_pass)
            # 发送
            print(4)
            smtpObj.sendmail(
                sender, receivers, message.as_string())
            # 退出
            smtpObj.quit()
            print(1)
        except smtplib.SMTPException as e:
            print('error', e)  # 打印错误
        return jsonify({"code": 20000, "data": {"verification": randomNumber}})


# 增加员工信息
@staff.route('/add', methods=['GET', 'POST'])
def add_info():
    if request.method == 'POST':
        data = request.get_json()

        id = data['id']
        realname = data['realname']
        sex = data['sex']
        age = data['age']
        department = data['department']
        permissions = data['permissions']
        remark = data['remark']
        # id = request.form.get('id')
        # realname = request.form.get('realname')
        # sex = request.form.get('sex')
        # age = request.form.get('age')
        # department = request.form.get('department')
        # permissions = request.form.get('permissions')
        user = test_user(id=id, username='', password='', sex=sex, age=age, department=department,
                         permissions=permissions, email='', remark=remark, realname=realname)
        db.session.add(user)
        db.session.commit()
        return jsonify({"code": 20000, "data": "success"})
    else:
        return jsonify({"code": 10000, "data": "get_succeed"})


# 修改员工信息
@staff.route('/edit', methods=['GET', 'POST'])
def edit_info():
    if request.method == 'POST':
        data = request.get_json()
        print(data)
        id = data['id']
        realname = data['realname']
        sex = data['sex']
        age = data['age']
        department = data['department']
        permissions = data['permissions']
        email = data['email']
        remark = data['remark']
        dbUser = test_user.query.filter(test_user.id == id).first()  # 先根据 id 查出数据库的一条数据
        dbUser.realname = realname  # 修改用户名admin  为 study2100
        dbUser.sex = sex
        dbUser.age = age
        dbUser.department = department
        dbUser.permissions = permissions
        db.session.commit()  # 提交数据库
        return jsonify({"code": 20000, "data": "success"})
    else:
        return jsonify({"code": 10000, "data": "get_succeed"})


# 删除员工信息
@staff.route('/delete', methods=['GET', 'POST'])
def delete_info():
    if request.method == 'POST':
        data = request.get_json()
        id = data['id']
        dbUser = test_user.query.filter(test_user.id == id).first()  # 先根据 id 查出数据库的一条数据
        db.session.delete(dbUser)
        db.session.commit()  # 提交数据库
        return jsonify({"code": 20000, "data": "success"})
    else:
        return jsonify({"code": 10000, "data": "get_succeed"})


# 查找员工信息
@staff.route('/search', methods=['GET', 'POST'])
def search_info():
    if request.method == 'GET':
        id = request.args.get('id')
        id = int(id)
        item = []
        dbUser = test_user.query.filter(test_user.id == id).first()  # 先根据 id 查出数据库的一条数据
        print(dbUser)
        item.append(dbUser.to_json())
        return jsonify({"code": 20000, "data": {"total": 1, "items": item}})
    else:
        return jsonify({"code": 10000, "data": "get_succeed"})


# 查找入侵信息
@record.route('/search', methods=['GET', 'POST'])
def search_invasion_info():
    if request.method == 'GET':
        id = request.args.get('id')
        id = int(id)
        item = []
        dbUser = test_warning_info.query.filter(test_warning_info.id == id).first()  # 先根据 id 查出数据库的一条数据
        print(dbUser)
        item.append(dbUser.to_json())
        return jsonify({"code": 20000, "data": {"total": 1, "items": item}})
    else:
        return jsonify({"code": 10000, "data": "get_succeed"})


# 获取员工列表
@staff.route('/list', methods=['GET', 'POST'])
def get_list():
    if request.method == 'GET':

        users = test_user.query.all()
        items = []
        for user in users:
            items.append(user.to_json())
        user_list = {"code": 20000, "data": {"total": 1, "items": items}}
        return jsonify(user_list)
    else:
        return jsonify({"code": 10000, "data": "get_succeed"})


# 获取入侵记录
@record.route('/list', methods=['GET', 'POST'])
def get_invasion_list():
    if request.method == 'GET':

        warnings = test_warning_info.query.all()
        items = []
        for warning in warnings:
            items.append(warning.to_json())
        warning_list = {"code": 20000, "data": {"total": 1, "items": items}}
        return jsonify(warning_list)
    else:
        return jsonify({"code": 10000, "data": "get_succeed"})


# 删除入侵记录
@record.route('/delete', methods=['GET', 'POST'])
def delete_invasion_info():
    if request.method == 'POST':
        data = request.get_json()
        id = data['id']
        dbUser = test_warning_info.query.filter(test_warning_info.id == id).first()  # 先根据 id 查出数据库的一条数据
        db.session.delete(dbUser)
        db.session.commit()  # 提交数据库
        return jsonify({"code": 20000, "data": "success"})
    else:
        return jsonify({"code": 10000, "data": "get_succeed"})


if __name__ == '__main__':
    app.register_blueprint(staff, url_prefix='/staff')  # 注册staff，使用前缀 user 作为前缀访问
    app.register_blueprint(record, url_prefix='/record')  # 注册staff，使用前缀 user 作为前缀访问
    app.run(host='192.168.28.179', debug=True)
    # app.run(host='127.0.0.1', debug=True)
    run_multi_camera()

# 增
# user = User(userName='admin', userPassword='123456')
#     db.session.add(user)
#     db.session.commit()

# resultUser = User.query.filter(User.id == 1).first()
#     db.session.delete(resultUser)
#     db.session.commit()

# dbUser = User.query.filter(User.id == 1).first() # 先根据 id 查出数据库的一条数据
#     dbUser.userName='study2100' # 修改用户名admin  为 study2100
#     db.session.commit()  # 提交数据库
#
# users = User.query.paginate(1, per_page=10) # 分页查询第一页数据，本页查询10条
#     users = User.query.order_by(User.id.desc()).paginate(page, per_page=10) # order_by 是排序，按照 id 倒叙排列查询

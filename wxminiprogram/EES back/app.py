import random
import smtplib
from email.mime.text import MIMEText

from flask import Flask, render_template, Response, request, jsonify, Blueprint
import cv2
from flask_cors import CORS
import config
from exts import db
from model import test_user, test_warning_info
import _json
import json
import time
import argparse
from flask_sqlalchemy import SQLAlchemy
import base64
import pymysql
from pymysql.converters import escape_string
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

app = Flask(__name__)
CORS(app, supports_credentials=True)  # 跨域
app.config.from_object(config)  # 加载数据库配置文件
# db.init_app(app) # 绑定到我们到应用程序
db = SQLAlchemy(app)
staff = Blueprint('staff', __name__)

# ap = argparse.ArgumentParser()
# ap.add_argument("-v", "--video", type=str,
# 	help="path to input video file")
# ap.add_argument("-t", "--tracker", type=str, default="kcf",
# 	help="OpenCV object tracker type")
# args = vars(ap.parse_args())

# OPENCV_OBJECT_TRACKERS = {
# 	# "csrt": cv2.TrackerCSRT_create,
# 	"kcf": cv2.TrackerKCF_create,
# 	# "boosting": cv2.TrackerBoosting_create,
# 	"mil": cv2.TrackerMIL_create,
# 	# "tld": cv2.TrackerTLD_create,
# 	# "medianflow": cv2.TrackerMedianFlow_create,
# 	# "mosse": cv2.TrackerMOSSE_create
# }
# trackers = cv2.MultiTracker_create()

# VideoCapture可以读取从url、本地视频文件以及本地摄像头的数据
# camera = cv2.VideoCapture('rtsp://admin:admin@172.21.182.12:554/cam/realmonitor?channel=1&subtype=1')
# camera = cv2.VideoCapture('rtsp://192.168.43.1:8554/live')
# camera = cv2.VideoCapture('rtsp://172.30.78.44:8554/live')

#camera = cv2.VideoCapture('test.mp4')
# 0代表的是第一个本地摄像头，如果有多个的话，依次类推

camera1 = cv2.VideoCapture('examplevideo.avi')
#camera1 = cv2.VideoCapture('gbtc.mp4')


camera = cv2.VideoCapture(0)

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
    receivers = ['19301088@bjtu.edu.cn']

    content = '【鹰眼入侵检测系统】有入侵！请及时查看！'

    # 设置email信息
    # 邮件内容设置
    message = MIMEText(content, 'plain', 'utf-8')
    # 邮件主题
    message['Subject'] = '鹰眼入侵检测系统入侵信息'
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

CorrectVerificationCode = 0
#发送验证码
def send_vericode_email(emailaddr):

    # 设置服务器所需信息
    # 163邮箱服务器地址
    mail_host = 'smtp.163.com'
    # 163用户名
    mail_user = 'tjsghj'
    # 密码(部分邮箱为授权码)
    mail_pass = 'UEYTOKGEXOZLFYSS'
    # 邮件发送方邮箱地址
    sender = 'tjsghj@163.com'


    # 邮件接受方邮箱地址，注意需要[]包裹，这意味着你可以写多个邮件地址群发
    receivers = [emailaddr]

    randomNumber = random.randint(1000, 9999)
    global CorrectVerificationCode
    CorrectVerificationCode = randomNumber
    randomNumberStr = str(randomNumber)
    content = '【鹰眼入侵检测系统】您的验证码是' + randomNumberStr + '。如非本人操作，请忽略本邮件'

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
        smtpObj.connect(mail_host, 25)
        # 登录到服务器
        smtpObj.login(mail_user, mail_pass)
        # 发送
        smtpObj.sendmail(
            sender, receivers, message.as_string())
        # 退出
        smtpObj.quit()
        # print('success')

    except smtplib.SMTPException as e:
        print('error', e)  # 打印错误

def send_intrusion_email():

    # 设置服务器所需信息
    # 163邮箱服务器地址
    mail_host = 'smtp.163.com'
    # 163用户名
    mail_user = 'tjsghj'
    # 密码(部分邮箱为授权码)
    mail_pass = 'UEYTOKGEXOZLFYSS'
    # 邮件发送方邮箱地址
    sender = 'tjsghj@163.com'


    # 邮件接受方邮箱地址，注意需要[]包裹，这意味着你可以写多个邮件地址群发
    receivers = ['19301088@bjtu.edu.cn']

    content = '【鹰眼入侵检测系统】您好！检测到入侵！'

    # 设置email信息
    # 邮件内容设置
    message = MIMEText(content, 'plain', 'utf-8')
    # 邮件主题
    message['Subject'] = '鹰眼入侵检测系统'
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
        # print('success')

    except smtplib.SMTPException as e:
        print('error', e)  # 打印错误

def gen_frames():
    # 测试用,查看视频size
    # camera = cv2.VideoCapture('rtsp://172.30.78.44:8554/live')
    size = (int(camera.get(cv2.CAP_PROP_FRAME_WIDTH)),
            int(camera.get(cv2.CAP_PROP_FRAME_HEIGHT)))
    print('size:' + repr(size))

    fgbg = cv2.createBackgroundSubtractorKNN()

    background = None
    # warning = test_warning_info(id='', date=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
    #                             start_time=time.strftime("%H:%M:%S", time.localtime()),
    #                             camera='', invasion='')
    # db.session.add(warning)
    # db.session.commit()

    time1 = time3 = time.time()
    print(time1)
    while True:
        # 读取视频流
        grabbed, frame_lwpCV = camera.read()

        if frame_lwpCV is None:
            break

        # (success, boxes) = trackers.update(frame_lwpCV)

        # 对帧进行预处理，先转灰度图，再进行高斯滤波。
        # 用高斯滤波进行模糊处理，进行处理的原因：每个输入的视频都会因自然震动、光照变化或者摄像头本身等原因而产生噪声。对噪声进行平滑是为了避免在运动和跟踪时将其检测出来。
        gray_lwpCV = cv2.cvtColor(frame_lwpCV, cv2.COLOR_BGR2GRAY)
        gray_lwpCV = cv2.GaussianBlur(gray_lwpCV, (11, 11), 0)

        # 将第一帧设置为整个输入的背景
        if background is None:
            background = gray_lwpCV
            continue
        diff = cv2.absdiff(background, gray_lwpCV)
        fgamsk = fgbg.apply(diff)

        # 显示矩形框
        contours, hierarchy = cv2.findContours(fgamsk, cv2.RETR_EXTERNAL,
                                               cv2.CHAIN_APPROX_SIMPLE)  # 该函数计算一幅图像中目标的轮廓

        mark = 0

        rightBorder = int(camera.get(cv2.CAP_PROP_FRAME_WIDTH)-400)
        lowBorder = int(camera.get(cv2.CAP_PROP_FRAME_HEIGHT))
        for c in contours:
            if cv2.contourArea(c) < 6000:  # 对于矩形区域，只显示大于给定阈值的轮廓，所以一些微小的变化不会显示。对于光照不变和噪声低的摄像头可不设定轮廓最小尺寸的阈值
                continue
            (x, y, w, h) = cv2.boundingRect(c)  # 该函数计算矩形的边界框
            count = 0

            if (x + w > 220 and x < 400):
                time2 = time.time()
                print(time2)
                if time2 - time1 > 200:
                    time1 = time2
                    cv2.rectangle(frame_lwpCV, (x, y), (x + w, y + h), (0, 0, 255), 2)
                    # cv2.rectangle(frame_lwpCV, (rightBorder, 0), (rightBorder + 400, lowBorder), (0, 0, 255), 2)

                    # 获取截图路径并在下面数据库中保存路径
                    image_path1 = '1.jpg'

                    # 存入数据库
                    # warning = test_warning_info(date=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
                    #                             start_time=time.strftime("%H:%M:%S", time.localtime()),
                    #                             image=image_path1
                    #                             )
                    # db.session.add(warning)
                    # db.session.commit()
                else:
                    cv2.rectangle(frame_lwpCV, (x, y), (x + w, y + h), (0, 0, 255), 2)
                    if time2 - time3 > 10:
                        time3 = time2
                        send_intrusion_email()
                    # cv2.rectangle(frame_lwpCV, (rightBorder, 0), (rightBorder + 400, lowBorder), (0, 0, 255), 2)
                # 隔三十秒检测到入侵就发邮件
                # if time2 - time3 > 30:
                #     time3 = time2
                #     send_intrusion_email()

            else:
                cv2.rectangle(frame_lwpCV, (x, y), (x + w, y + h), (0, 255, 0), 2)

            print(x, y, w, h)
        cv2.rectangle(frame_lwpCV, (220, 0), (400, lowBorder), (255, 0, 0), 2)
        ret, jpeg = cv2.imencode('.jpg', frame_lwpCV)
        frame = jpeg.tobytes()
        key1 = cv2.waitKey(100) & 0xFF
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


def gen_frames_second():
    # 测试用,查看视频size
    # camera = cv2.VideoCapture('rtsp://172.30.78.44:8554/live')
    # camera1 = cv2.VideoCapture('rtsp://172.30.78.44:8554/live')
    size = (int(camera1.get(cv2.CAP_PROP_FRAME_WIDTH)),
            int(camera1.get(cv2.CAP_PROP_FRAME_HEIGHT)))
    print('size:' + repr(size))

    fgbg = cv2.createBackgroundSubtractorKNN()

    background = None
    # warning = test_warning_info(id='', date=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
    #                             start_time=time.strftime("%H:%M:%S", time.localtime()),
    #                             camera='', invasion='')
    # db.session.add(warning)
    # db.session.commit()

    # time1 = time3 = time.time()
    # print(time1)
    while True:
        # 读取视频流
        grabbed, frame_lwpCV = camera1.read()

        if frame_lwpCV is None:
            break

        # (success, boxes) = trackers.update(frame_lwpCV)

        # 对帧进行预处理，先转灰度图，再进行高斯滤波。
        # 用高斯滤波进行模糊处理，进行处理的原因：每个输入的视频都会因自然震动、光照变化或者摄像头本身等原因而产生噪声。对噪声进行平滑是为了避免在运动和跟踪时将其检测出来。
        gray_lwpCV = cv2.cvtColor(frame_lwpCV, cv2.COLOR_BGR2GRAY)
        gray_lwpCV = cv2.GaussianBlur(gray_lwpCV, (11, 11), 0)

        # 将第一帧设置为整个输入的背景
        if background is None:
            background = gray_lwpCV
            continue
        diff = cv2.absdiff(background, gray_lwpCV)
        fgamsk = fgbg.apply(diff)

        # 显示矩形框
        contours, hierarchy = cv2.findContours(fgamsk, cv2.RETR_EXTERNAL,
                                               cv2.CHAIN_APPROX_SIMPLE)  # 该函数计算一幅图像中目标的轮廓

        mark = 0

        for c in contours:
            if cv2.contourArea(c) < 3200:  # 对于矩形区域，只显示大于给定阈值的轮廓，所以一些微小的变化不会显示。对于光照不变和噪声低的摄像头可不设定轮廓最小尺寸的阈值
                continue
            (x, y, w, h) = cv2.boundingRect(c)  # 该函数计算矩形的边界框
            count = 0

            if (x + w > 200):
                time2 = time.time()
                print(time2)
                if time2 - time1 > 5:
                    time1 = time2
                    cv2.rectangle(frame_lwpCV, (x, y), (x + w, y + h), (0, 0, 255), 2)

                    # 获取截图路径并在下面数据库中保存路径
                    # image_path1 = '1.jpg'

                    # 存入数据库
                    # warning = test_warning_info(date=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
                    #                             start_time=time.strftime("%H:%M:%S", time.localtime()),
                    #                             image=image_path1
                    #                             )
                    # db.session.add(warning)
                    # db.session.commit()
                else:
                    cv2.rectangle(frame_lwpCV, (x, y), (x + w, y + h), (0, 0, 255), 2)

                # 隔三十秒检测到入侵就发邮件
                # if time2 - time3 > 30:
                #     time3 = time2
                #     send_email()

            else:
                cv2.rectangle(frame_lwpCV, (x, y), (x + w, y + h), (0, 255, 0), 2)

            print(x, y, w, h)
        cv2.rectangle(frame_lwpCV, (200, 0), (320, 240), (255, 0, 0), 2)
        ret, jpeg = cv2.imencode('.jpg', frame_lwpCV)
        frame = jpeg.tobytes()
        key1 = cv2.waitKey(100) & 0xFF
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')





#test连接用 无实际用途
########################################################
@app.route('/testsend', methods=['POST'])
def testsend():
    if request.method == 'POST':
        send_email()
    return jsonify({"code": 20000, "data": "success"})


########################################################

@app.route('/sendVericode', methods=['POST'])
def send_vericode():

    username = request.values.get("username")
    password = request.values.get("password")
    id = request.values.get("id")
    intid = int(request.values.get("id"))
    email = request.values.get("email")

    if request.method == 'POST':
        if (len(username) == 0):
            return jsonify({"code": 10000, "msg": "用户名不能为空"})
        if (len(password) == 0):
            return jsonify({"code": 10000, "msg": "密码不能为空"})
        if (len(id) == 0):
            return jsonify({"code": 10000, "msg": "id不能为空"})
        if (len(email) == 0):
            return jsonify({"code": 10000, "msg": "邮箱不能为空"})

        users = test_user.query.all()
        # print(users)
        for user in users:
            # if user.username == username and user.password == password:
            if user.id == intid:
                if(user.username != None):
                    return jsonify({"code": 10000, "msg": "账号已存在"})
                else:
                    send_vericode_email(email)
                    return jsonify({"code": 20000,"revericode": str(CorrectVerificationCode), "msg": "success"})
            else:
                continue
        # 19301088@bjtu.edu.cn
        return jsonify({"code": 10000, "msg": "id不存在"})


@app.route('/video_start', methods=['GET', 'POST'])
def video_start():
    # 通过将一帧帧的图像返回，就达到了看视频的目的。multipart/x-mixed-replace是单次的http请求-响应模式，如果网络中断，会导致视频流异常终止，必须重新连接才能恢复

    if request.method == "GET":
        return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/video_start_second', methods=['GET', 'POST'])
def video_start_second():
    # 通过将一帧帧的图像返回，就达到了看视频的目的。multipart/x-mixed-replace是单次的http请求-响应模式，如果网络中断，会导致视频流异常终止，必须重新连接才能恢复

    if request.method == "GET":
        return Response(gen_frames_second(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/')
def index():
    return render_template('index.html')


# 注销
@app.route('/logout')
def logout():
    return jsonify({"code": 20000, "data": "success"})


# 登录
@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':
        username = request.values.get("username")
        password = request.values.get("password")
        print(username)
        print(password)

        if(len(username)==0):
            return jsonify({"code": 10000, "msg": "用户名不能为空"})
        if (len(password) == 0):
            return jsonify({"code": 10000, "msg": "密码不能为空"})


        users = test_user.query.all()
        print(users)
        for user in users:
            if user.username == username and user.password == password:
                return jsonify({"code": 20000, "data": user.permissions})
            else:
                continue

        return jsonify({"code": 10000, "data": "login_fail"})

    else:
        return jsonify({"code": 20000, "data": {"roles": ['admin'], "introduction": 'I am a super administrator',
                                                "avatar": 'https://wpimg.wallstcn.com/f778738c-e4f8-4870-b634'
                                                          '-56703b4acafe.gif',
                                                "name": 'Super Admin'}})


# 注册
@app.route('/register', methods=['GET', 'POST'])
def register():
    username = request.values.get("username")
    password = request.values.get("password")
    id = request.values.get("id")
    email = request.values.get("email")
    print(username)
    print(password)
    print(email)
    if request.method == 'POST':
        if (len(username) == 0):
            return jsonify({"code": 10000, "msg": "用户名不能为空"})
        if (len(password) == 0):
            return jsonify({"code": 10000, "msg": "密码不能为空"})
        if (len(id) == 0):
            return jsonify({"code": 10000, "msg": "id不能为空"})
        if (len(email) == 0):
            return jsonify({"code": 10000, "msg": "邮箱不能为空"})

        intid = int(request.values.get("id"))

        users = test_user.query.all()
        for user in users:
            if user.id == intid:
                if (user.username != None):
                    return jsonify({"code": 10000, "msg": "账号已存在"})

                else:
                    # 19301088@bjtu.edu.cn
                    db = pymysql.connect(host="localhost", user="root", password="mysql1125", db="testdbdj")
                    cursor = db.cursor()
                    sql = "UPDATE test_user SET username = '%s', password = '%s', email = '%s' WHERE id = '%s'" % (username, password, email, intid)
                    cursor.execute(sql)
                    db.commit()

                    return jsonify({"code": 20000, "msg": "注册成功"})
            else:
                continue
        # 19301088@bjtu.edu.cn
        return jsonify({"code": 10000, "msg": "id不存在"})


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


# 获取员工列表
@staff.route('/list', methods=['GET', 'POST'])
def get_list():
    if request.method == 'GET':
        users = test_user.query.all()
        items = []
        for user in users:
            items.append(user.to_json())
        # user_list = {"code": 20000, "data": {"total": 1, "items": items}}
        user_list = {"code": 20000, "items": items}
        # print(items)
        return jsonify(user_list)
    else:
        return jsonify({"code": 10000, "data": "get_succeed"})

@staff.route('/intrusion_records', methods=['GET', 'POST'])
def get_intrusion_records():
    if request.method == 'GET':
        records = test_warning_info.query.all()

        items = []
        for record in records:
            items.append(record.to_json())

        info_list = {"code": 20000, "items": items}
        return jsonify(info_list)
    else:
        return jsonify({"code": 10000, "data": "get_succeed"})

@staff.route('/intrusion_picture', methods=['GET', 'POST'])
def get_intrusion_picture():
    if request.method == 'GET':
        image = open(r"C:\Users\Tony Guo\Desktop\xiaoxueqi\ruqin.png", 'rb')
        resp = Response(image, mimetype="image/png")
        return resp

# 传输入侵图片
# @app.route('/invasion_graph', methods=['GET', 'POST'])
# def get_warning_graph():
#     if request.method == 'GET':
#         data = request.get_json()
#         date = data['date']
#         warnings = test_warning_info.query.filter(test_warning_info.date == date).all()
#
#         for warning in warnings:
#             warning_graph =
#         user_list = {"code": 20000, "data": {"total": 1, "items": items}}
#         return jsonify(user_list)
#     else:
#         return jsonify({"code": 10000, "data": "get_succeed"})

@app.route('/cameraindex_image', methods=['GET'])
def display_cameraindex_image():
    if request.method == 'GET':
        saveFigure()
        image = open(r"C:\Users\Tony Guo\Desktop\xiaoxueqi\cameraindex_times.jpg", 'rb')
        resp = Response(image, mimetype="image/jpeg")
        return resp


@app.route('/time_image', methods=['GET'])
def display_time_image():
    if request.method == 'GET':
        image = open(r"C:\Users\Tony Guo\Desktop\xiaoxueqi\time_times.jpg", 'rb')
        resp = Response(image, mimetype="image/jpeg")
        return resp

#时间段-检测入侵次数
def drawTimeTimesBarChart():

    plt.rcParams['font.sans-serif']=['SimHei'] #显示中文标签
    plt.rcParams['axes.unicode_minus']=False   #这两行需要手动设置

    # 添加图形属性
    plt.xlabel('时间段')
    plt.ylabel('次数')
    plt.title('数据统计')

    #读取数据库
    #tp~time period
    #统计 tp1 tp2 tp3 tp4 次数

    tp1 = tp2 = tp3 = tp4 = 0

    db = pymysql.connect(host="localhost",
                     user="root",
                     password="mysql1125",
                     db="testdbdj")  ##########
    cursor = db.cursor()
    ########数据表信息 读取用户信息
    sql = """SELECT * FROM test_warning_info"""  ##########

    cursor.execute(sql)
    results = cursor.fetchall()
    """
    #         0       1          2         3        4         5
    #        id      date    start_time  camera   invasion  image
    # type   int     char       char      char     char      char
    """

    for row in results:
        sqlBeginTime = row[2]
        timenums = sqlBeginTime.split(':')
        hournum = int(timenums[0])

        if hournum >= 6 and hournum <= 11:
            tp1 += 1
        if hournum >= 12 and hournum <= 17:
            tp2 += 1
        if hournum >= 18 and hournum <= 23:
            tp3 += 1
        if hournum >= 0 and hournum <= 5:
            tp4 += 1

    cursor.execute(sql)
    db.commit()
    # 关闭数据库连接
    db.close()

    y = [tp1, tp2, tp3, tp4]  # 这个是y轴的数据
    first_bar = plt.bar(range(len(y)), y, color='blue')  # 初版柱形图，x轴0-9，y轴是列表y的数据，颜色是蓝色

    index = [0, 1, 2, 3]
    name_list = ['6:00-12:00', '12:00-18:00', '18:00-24:00', '0:00-6:00']  # x轴标签
    plt.xticks(index, name_list)  # 绘制x轴的标签

    # 柱形图顶端数值显示
    for data in first_bar:
        y = data.get_height()
        x = data.get_x()
        plt.text(x + 0.35, y, str(y), va='bottom')  # 0.15为偏移值，可以自己调整，正好在柱形图顶部正中

    # 图片的显示及存储
    plt.savefig("time_times.jpg")
#    plt.show()

#监控编号（位置）-检测入侵次数
def drawCameraIndexTimesBarChart():

    plt.rcParams['font.sans-serif']=['SimHei'] #显示中文标签
    plt.rcParams['axes.unicode_minus']=False   #这两行需要手动设置

    # 添加图形属性
    plt.xlabel('监控编号')
    plt.ylabel('次数')
    plt.title('数据统计')

    #读取数据库
    #tp~time period
    #统计 cnt1 cnt2 cnt3 cnt4 次数

    cnt1 = cnt2 = cnt3 = cnt4 = 0

    db = pymysql.connect(host="localhost",
                     user="root",
                     password="mysql1125",
                     db="testdbdj")  ##########
    cursor = db.cursor()
    ########数据表信息 读取用户信息
    sql = """SELECT * FROM test_warning_info"""  ##########

    cursor.execute(sql)
    results = cursor.fetchall()

    """
        #         0       1          2         3        4         5
        #        id      date    start_time  camera   invasion  image
        # type   int     char       char      char     char      char
    """

    for row in results:
        sqlcharIndex = row[3]
        sqlIndex = int(sqlcharIndex)

        if sqlIndex == 1:
            cnt1 += 1
        if sqlIndex == 2:
            cnt2 += 1
        if sqlIndex == 3:
            cnt3 += 1
        if sqlIndex == 4:
            cnt4 += 1

    cursor.execute(sql)
    db.commit()
    # 关闭数据库连接
    db.close()

    y = [cnt1, cnt2, cnt3, cnt4]  # 这个是y轴的数据
    first_bar = plt.bar(range(len(y)), y, color='blue')  # 初版柱形图，x轴0-9，y轴是列表y的数据，颜色是蓝色

    index = [0, 1, 2, 3]
    name_list = ['Camera 1', 'Camera 2', 'Camera 3', 'Camera 4']  # x轴标签
    plt.xticks(index, name_list)  # 绘制x轴的标签

    # 柱形图顶端数值显示
    for data in first_bar:
        y = data.get_height()
        x = data.get_x()
        plt.text(x + 0.35, y, str(y), va='bottom')  # 0.15为偏移值，可以自己调整，正好在柱形图顶部正中

    # 图片的显示及存储
    plt.savefig("cameraindex_times.jpg")
    # plt.show()

    #图片转成流
    #return jsonResponse


def saveFigure():
    drawCameraIndexTimesBarChart()
    drawTimeTimesBarChart()
















if __name__ == '__main__':
    app.register_blueprint(staff, url_prefix='/staff')  # 注册staff，使用前缀 staff 作为前缀访问
    app.run(host='127.0.0.1', debug=True)

# def get_month_records():
#     month_choose_str = request.POST.get('month')
#     month_choose = datetime.datetime.strptime(month_choose_str,'%Y-%m')
#     invation_m_list1 = invationRecord.objects.filter(date__year=month_choose.year)
#     invation_m_list =invation_m_list1.filter(date__month=month_choose.month)
#     invation_list=[]
#     dict = {}
#     for i in range(1,31):
#         invation_d_list =invation_m_list.filter(date__day=i)
#         if invation_d_list.count() !=0:
#             # dict={i:invation_d_list.count()}
#             dict[i] = invation_d_list.count()
#             invation_list.append(dict)
#
#     response_data =json.dumps(list(invation_list),cls=DateEncoder,indent= 4)
#     return Response(dict)

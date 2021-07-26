from flask import Flask, render_template, Response,request,jsonify,Blueprint
import cv2
from flask_cors import CORS
import config
from exts import db
from model import test_user
import _json
import json

app = Flask(__name__)
CORS(app, supports_credentials=True)# 跨域
app.config.from_object(config) # 加载数据库配置文件
db.init_app(app) # 绑定到我们到应用程序
staff = Blueprint('staff', __name__)


# VideoCapture可以读取从url、本地视频文件以及本地摄像头的数据
# camera = cv2.VideoCapture('rtsp://admin:admin@172.21.182.12:554/cam/realmonitor?channel=1&subtype=1')
# camera = cv2.VideoCapture('test.mp4')
# 0代表的是第一个本地摄像头，如果有多个的话，依次类推
camera = cv2.VideoCapture('examplevideo.avi')
#camera = cv2.VideoCapture(0)

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
def gen_frames():

    # 测试用,查看视频size
    size = (int(camera.get(cv2.CAP_PROP_FRAME_WIDTH)),
            int(camera.get(cv2.CAP_PROP_FRAME_HEIGHT)))
    print('size:' + repr(size))

    fgbg = cv2.createBackgroundSubtractorKNN()

    background = None
    while True:
        # 读取视频流
        grabbed, frame_lwpCV = camera.read()

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
        for c in contours:
            if cv2.contourArea(c) < 3200:  # 对于矩形区域，只显示大于给定阈值的轮廓，所以一些微小的变化不会显示。对于光照不变和噪声低的摄像头可不设定轮廓最小尺寸的阈值
                continue
            (x, y, w, h) = cv2.boundingRect(c)  # 该函数计算矩形的边界框

            if (x + w > 200):
                cv2.rectangle(frame_lwpCV, (x, y), (x + w, y + h), (0, 0, 255), 2)
            else:
                cv2.rectangle(frame_lwpCV, (x, y), (x + w, y + h), (0, 255, 0), 2)

            print(x, y, w, h)
        cv2.rectangle(frame_lwpCV, (200, 0), (320, 240), (255, 0, 0), 2)
        ret, jpeg = cv2.imencode('.jpg', frame_lwpCV)
        frame = jpeg.tobytes()
        key1 = cv2.waitKey(100) & 0xFF
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


@app.route('/video_start',methods=['GET', 'POST'])
def video_start():
    # 通过将一帧帧的图像返回，就达到了看视频的目的。multipart/x-mixed-replace是单次的http请求-响应模式，如果网络中断，会导致视频流异常终止，必须重新连接才能恢复

    if request.method == "GET":
        return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')



@app.route('/')
def index():
    return render_template('index.html')


# 注销
@app.route('/logout')
def logout():
    return jsonify({"code": 20000, "data": "success"})


# 登录
@app.route('/login',methods=['GET', 'POST'])
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
        return jsonify({"code": 10000, "data": "login_fail"})

    else:
        return jsonify({"code": 20000,"data": {"roles": ['admin'],"introduction": 'I am a super administrator',
                            "avatar": 'https://wpimg.wallstcn.com/f778738c-e4f8-4870-b634-56703b4acafe.gif',
                            "name": 'Super Admin'}})


# 注册
@app.route('/register',methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        realname = request.form.get('realname')
        email = request.form.get('email')

        user = test_user(realname,username,password,email)
        db.session.add(user)
        db.session.commit()
        return jsonify({"code": 20000, "data": "success"})
    else:
        return jsonify({"code": 10000, "data": "login_fail"})


# 增加员工信息
@staff.route('/add',methods=['GET', 'POST'])
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
        user = test_user(id = id,username = '',password = '',sex = sex,age = age,department = department,permissions = permissions,email = '',remark = remark,realname = realname)
        db.session.add(user)
        db.session.commit()
        return jsonify({"code": 20000, "data": "success"})
    else:
        return jsonify({"code": 10000, "data": "get_succeed"})

@staff.route('/edit',methods=['GET', 'POST'])
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
        dbUser = test_user.query.filter(test_user.id == id).first() # 先根据 id 查出数据库的一条数据
        dbUser.realname = realname # 修改用户名admin  为 study2100
        dbUser.sex = sex
        dbUser.age = age
        dbUser.department = department
        dbUser.permissions = permissions
        db.session.commit()  # 提交数据库
        return jsonify({"code": 20000, "data": "success"})
    else:
        return jsonify({"code": 10000, "data": "get_succeed"})

@staff.route('/delete',methods=['GET', 'POST'])
def delete_info():
    if request.method == 'POST':
        data = request.get_json()
        id = data['id']
        dbUser = test_user.query.filter(test_user.id == id).first() # 先根据 id 查出数据库的一条数据
        db.session.delete(dbUser)
        db.session.commit()  # 提交数据库
        return jsonify({"code": 20000, "data": "success"})
    else:
        return jsonify({"code": 10000, "data": "get_succeed"})

# 获取员工列表
@staff.route('/list',methods=['GET', 'POST'])
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

if __name__ == '__main__':
    app.register_blueprint(staff, url_prefix='/staff')  # 注册staff，使用前缀 user 作为前缀访问
    app.run(host='172.20.10.5', debug=True)
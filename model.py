from exts import db
from datetime import datetime

# 用户模型
class test_user(db.Model):
    tableName = 'test_user'
    id = db.Column(db.INTEGER, primary_key=True, autoincrement=True,nullable=True)
    username = db.Column(db.String(30), nullable=True)
    password = db.Column(db.String(30), nullable=True)
    realname = db.Column(db.String(30), nullable=True)
    sex = db.Column(db.String(30), nullable=True)
    age = db.Column(db.String(30), nullable=True)
    department = db.Column(db.String(30), nullable=True)
    permissions = db.Column(db.String(30), nullable=True)
    email = db.Column(db.String(30), nullable=True)
    remark = db.Column(db.String(30), nullable=True)

    def to_json(self):
        """将实例对象转化为json"""
        item = self.__dict__
        if "_sa_instance_state" in item:
            del item["_sa_instance_state"]
        return item

class test_warning_info(db.Model):
    tableName = 'test_warning_info'
    id = db.Column(db.INTEGER, primary_key=True, autoincrement=True)
    date = db.Column(db.Date)
    start_time = db.Column(db.Time)
    end_time = db.Column(db.Time)
    camera = db.Column(db.String(30), nullable=True)
    invasion = db.Column(db.String(30), nullable=True)

    def to_json(self):
        """将实例对象转化为json"""
        item = self.__dict__
        if "_sa_instance_state" in item:
            del item["_sa_instance_state"]
        return item

    # class User(db.Model):
    #     __tablename__ = 'users'
    #     id = db.Column(db.Integer, primary_key=True)
    #     username = db.Column(db.String(80), unique=True)
    #     email = db.Column(db.String(320), unique=True)
    #     password = db.Column(db.String(32), nullable=False)
    #
    #     def __repr__(self):
    #         return '<User %r>' % self.username
    #
    # class Admin(db.Model):
    #     __tablename__ = 'admins'
    #     id = db.Column(db.Integer, primary_key=True)
    #     username = db.Column(db.String(80), unique=True)
    #     email = db.Column(db.String(320), unique=True)
    #     password = db.Column(db.String(32), nullable=False)
    #
    #     def __repr__(self):
    #         return '<User %r>' % self.username
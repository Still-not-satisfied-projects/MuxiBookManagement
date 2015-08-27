# coding: utf-8
"""
    models.py
    ~~~~~~~~~

        数据库文件

            木犀图书是一个图书借阅管理网站，所以数据库主要提供图书、用户信息以及图书借阅状态与信息的存储

            数据库tables:
                                                        books

                 id                         Integer, primary_key                          主键
                 url                        String url                                    对应豆瓣API的get url
                 name                       String                                        书名
                 summary                    String(编码) resp['summary']返回值             概要，豆瓣API获取
                 image                      String(编码) resp['image']返回值 url           封面图，API获取
                 user_id                    Integer，ForeignKey 外键 与users表的id相关联    与借阅者关联
                 end                        String, 书籍到期时间
                 status                     Boolean, 书籍的借阅状态，如果为True则被借阅
                ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                                                        users

                 id                         Integer, primary_key                          主键
                 username                   String                                        用户名
                 password                   password_hash                                 密码散列值
                 book                       relationship                                  借阅书籍的属性
"""
from . import db, login_manager, app
from flask.ext.login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import sys


# python 3搜索的不兼容
if sys.version_info[0] == 3:
    enable_search = False
else:
    enable_search = True
    import flask.ext.whooshalchemy as whooshalchemy




class Book(db.Model):
    """图书类"""
    __searchable__ = ['name', 'tag', 'summary']
    __tablename__ = "books"
    id = db.Column(db.Integer, primary_key = True)
    url = db.Column(db.String(164))
    name = db.Column(db.Text)
    author = db.Column(db.Text)
    tag = db.Column(db.String(164))
    summary = db.Column(db.Text)
    image = db.Column(db.String(164))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    status = db.Column(db.Boolean)
    start = db.Column(db.String(164))
    end = db.Column(db.String(164))

    def __repr__(self):
        return "%r :The instance of class Book" % self.name


class User(db.Model, UserMixin):
    """用户类"""
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(164))
    password_hash = db.Column(db.String(164))
    book = db.relationship('Book', backref="user", lazy="dynamic")

    @login_manager.user_loader
    def load_user(user_id):
        """flask-login要求实现的用户加载回调函数
           依据用户的unicode字符串的id加载用户"""
        return User.query.get(int(user_id))

    @property
    def password(self):
        """将密码方法设为User类的属性"""
        raise AttributeError('无法读取密码原始值!')

    @password.setter
    def password(self, password):
        """设置密码散列值"""
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        """验证密码散列值"""
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return "%r :The instance of class User" % self.username


if enable_search:
    whooshalchemy.whoosh_index(app, Book)

# coding: utf-8
"""
    muxibook 木犀图书管理系统
    ~~~~~~~~~~~~~~~~~~~~~~~~~

        实现图书借阅管理功能
"""
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager


app = Flask(__name__)
app.config['SECRET_KEY'] = "I hate flask!"
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///path/to/data.sqlite"  # 系统相应替换
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['WHOOSH_BASE'] = "search.db"
app.config['MAX_SEARCH_RESULTS'] = 5  # 最大加载5个搜索结果


db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.session_protection = 'strong'
login_manager.login_view = 'login'


from . import models, views, forms

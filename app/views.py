# coding: utf-8

"""
    views.py
    ~~~~~~~~

        木犀图书视图函数
        url                                        func
        /;/home                           1.最近录入(6条)， 2.最近借阅
        /login                            登录
        /logout                           登出
        /bookin                           录入新书
        /search                           站内搜索（支持两种模式）
        /search_results                   搜索结果页(提供借阅表单) 关于借阅状态
        /admin                            后台管理（只对管理员开放)
        /<current_user>                   个人信息页(最近借阅)(快要到期 3天)
                      已过期的图书会flash消息提示
"""

from . import app, db
from app.models import User, Book
from app.forms import SearchForm, BookForm, LoginForm, GetForm, BackForm
from flask import render_template, redirect, url_for, session, flash
from flask.ext.login import login_user, logout_user, login_required, \
    current_user
from urllib2 import urlopen
import json
import datetime


@app.route('/')
@app.route('/home')
def home():
    """
    首页视图函数

        1. 最近录入
        2. 最近借阅

        new_book_list: 最近录入新书列表(默认为6本, 依据时间[id]排序)
    """
    new_book_list = Book.query.order_by('-id').all()[:6]
    get_book_list = Book.query.filter_by(status=True).order_by('-id').all()[:2]

    return render_template('zhuye.html', new_book_list=new_book_list,
                           get_book_list=get_book_list)


@app.route('/search', methods=["POST", "GET"])
def search():
    """
    搜索视图函数

        1. 搜索表单
        2. 显示搜索结果列表(最多加载5条搜索结果)

        搜索模式：
            1. 书名搜索（书名必须正确）
            2. 类别搜索（返回类别的图书：后台、前端、设计、互联网、其他）
    """
    form = SearchForm()
    if form.validate_on_submit():
        query = form.search.data
        return redirect(url_for('search_results', query=query))
    return render_template('search.html', form=form)


@app.route('/search_results/<query>', methods=["POST", "GET"])
def search_results(query):
    """
    搜索结果页

        提供书籍借阅表单
    """
    form = GetForm()
    get_book_list = []
    form_list = []
    results = Book.query.whoosh_search(query, app.config['MAX_SEARCH_RESULTS'])

    for book in results[:]:
        if book.status != True:
        # 跳过不可借阅图书
            get_book_list.append(book)
            form_list.append(form)

    form_and_book_list = zip(form_list, get_book_list)

    for n in range(len(form_list)):
        """
        这是发现的第一个重大的bug！，也就是说，for循环在python中是顺序遍历，
        这也意味着用户也要顺序点击才能将书籍与表单对应，显然，这是不可能的
        用户需要选择！

        现在必须找到一种方法将用户书籍与表单相对应，问题是如何对应呢？

        我需要一种标记，依靠这种标记我可以获取表单所对应的图书的位置，问题是如果
        这种标记放在html里，那然后呢？还是我需要一个表单的循环，现在的问题是已经
        创建了想对应的表单，但这些表单都是平等的也就是说这些表单的眼里没有书，只有
        用户的post动作，但是又要如何用书的眼光看表单的？

        这是问题的关键：如何用书的眼光去看表单。显然顺序遍历是不行的!
        """
        if form_list[n].validate_on_submit():
            get_book_list[n].status = form.status.data
            get_book_list[n].user_id = current_user.id
            day = form.day.data
            get_book_list[n].end = str(datetime.datetime.now() + datetime.timedelta(day))
            return redirect(url_for('user', \
                                    username=current_user.username))

    return render_template('search_results.html',
                           form_and_book=form_and_book_list,
                           query=query,
                           form=form)


@app.route('/bookin', methods=["POST", "GET"])
def bookin():
    """
    书籍录入

        输入书籍的名字，将书籍的

            书名， 封面， 简介 录入数据库
    """
    form = BookForm()

    if form.validate_on_submit():
        bookname = form.bookname.data
        get_url = "https://api.douban.com/v2/book/search?q=%s" % bookname
        resp_1 = json.loads(urlopen(get_url).read().decode('utf-8'))
        book_id = resp_1['books'][0]['id']
        url = "https://api.douban.com/v2/book/%s" % book_id
        resp_2 = json.loads(urlopen(url).read().decode('utf-8'))
        book = Book(url=url, name=resp_2['title'], author=resp_2['author'][0], tag=form.tag.data, summary=resp_2['summary'], \
                   image=resp_2['images'].get('large'), user_id=None, end=None)
        db.session.add(book)
        db.session.commit()
        flash('书籍已录入！')
        return redirect(url_for('bookin'))

    return render_template('bookin.html', form=form)


@app.route('/login', methods=["POST", "GET"])
def login():
    """登录视图函数"""
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is not None:
            login_user(user, form.remember_me.data)
            return redirect(url_for('user', \
                           username=current_user.username))
        flash('该用户不存在')
    return render_template('login.html', form=form)


@app.route('/logout')
@login_required
def logout():
    """退出视图函数"""
    logout_user()
    flash('你已登出!')
    return redirect(url_for('home'))


@app.route('/user/<username>', methods=["POST", "GET"])
def user(username):
    """
    用户个人信息页
        显示该用户历史借阅
        显示该用户快要过期的书（3天为界）
    """
    form = BackForm()
    user_get_book = Book.query.filter_by(user_id=current_user.id)[:6]
    for book in user_get_book:
        """还是for循环的bug，简直了！"""
        if form.validate_on_submit():
            """归还此图书"""
            book.status = False
            book.end = None
            book.user_id = None
            flash('你已归还此书!')
            return redirect(url_for('user', username=username))
    return render_template('user.html', username=username,
                           user_get_book=user_get_book,
                           form=form)

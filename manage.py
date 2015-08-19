# coding:utf-8
# !/usr/bin/python

"""
    manage.py
    ~~~~~~~~

        木犀图书后台管理文件

            1>服务器启动运行
            2>python shell(Ipython) 配置
                自动加载环境
                数据库迁移
                数据库更新
            3>运行测试
            4>管理界面配置

            定义的命令：
                python manage.py --help             显示帮助
                python manage.py runserver:         启动服务器
                python manage.py db init:           创建迁移文件夹
                python manage.py db migrate -m ""   执行数据库迁移
                python manage.py db upgrade         执行数据库更新
"""

import sys
from app import app, db
from app.models import Book, User
from flask.ext.script import Manager, Shell
from flask.ext.migrate import Migrate, MigrateCommand
from flask.ext.admin import Admin
from flask.ext.admin.contrib.sqla import ModelView


"""编码设置"""
reload(sys)
sys.setdefaultencoding('utf-8')


manager = Manager(app)
migrate = Migrate(app, db)
admin = Admin(app, name='木犀图书')


def make_shell_context():
    """自动加载环境"""
    return dict(
        app=app,
        db=db,
        Book=Book,
        User=User
    )


manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)


admin.add_view(ModelView(Book, db.session))
admin.add_view(ModelView(User, db.session))


@manager.command
def test():
    """运行测试"""
    import unittest
    tests = unittest.TestLoader().discover('test')
    unittest.TextTestRunner(verbosity=2).run(tests)


if __name__ == '__main__':
    app.debug = True
    manager.run()

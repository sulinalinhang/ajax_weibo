import pymysql

import time
import secret
from models.base_model import SQLModel
from models.user_role import UserRole
from models.user import User
from models.session import Session
from models.weibo import Weibo
from models.comment import Comment


def recreate_user_table(cursor):
    cursor.execute(User.sql_create)


def recreate_session_table(cursor):
    cursor.execute(Session.sql_create)


def recreate_weibo_table(cursor):
    cursor.execute(Weibo.sql_create)


def recreate_comment_table(cursor):
    cursor.execute(Comment.sql_create)


def recreate_database():
    connection = pymysql.connect(
        host='localhost',
        user='root',
        password=secret.mysql_password,
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )

    with connection.cursor() as cursor:
        cursor.execute(
            'DROP DATABASE IF EXISTS `{}`'.format(
                SQLModel.db_name
            )
        )
        cursor.execute(
            'CREATE DATABASE `{}` DEFAULT CHARACTER SET utf8mb4'.format(
                SQLModel.db_name
            )
        )
        cursor.execute('USE `{}`'.format(SQLModel.db_name))

        recreate_user_table(cursor)
        recreate_session_table(cursor)
        recreate_weibo_table(cursor)
        recreate_comment_table(cursor)


    connection.commit()
    connection.close()


def test_user_data():
    form = dict(
        username='nana',
        password='0723',
        role=UserRole.normal,
    )
    User.register(form)

def test_session_data():
    form = dict(
        session_id='dsacbhdjshabzmsd',
        user_id=2,
        expired_time=time.time(),
    )
    Session.new(form)

def test_weibo_date():
    form = dict(
        content='nana',
        user_id=1,
    )
    Weibo.new(form)

def test_comment_date():
    form = dict(
        content='nana',
        user_id=1,
        weibo_id=1
    )
    Comment.new(form)


if __name__ == '__main__':
    recreate_database()
    SQLModel.init_connection()
    test_user_data()
    test_session_data()
    test_weibo_date()
    test_comment_date()

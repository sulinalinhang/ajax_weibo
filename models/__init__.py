import pymysql

import secret
from models.base_model import SQLModel
from models.user_role import UserRole
from models.user import User


def recreate_table(cursor):
    cursor.execute(User.sql_create)


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

        recreate_table(cursor)

    connection.commit()
    connection.close()


def test_data():
    form = dict(
        username='nana',
        password='0723',
        role=UserRole.normal,
    )
    User.register(form)


if __name__ == '__main__':
    recreate_database()
    test_data()
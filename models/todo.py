import time

from models import Model


class Todo(Model):
    def __init__(self, form):
        super().__init__(form)
        self.title = form.get('title', '')
        # 和别的数据关联的方式, 用 user_id 表明拥有它的 user 实例
        self.user_id = form.get('user_id', None)
        self.created_time = form.get('created_time', -1)
        self.updated_time = form.get('updated_time', -1)

    @classmethod
    def add(cls, form, user_id):
        t = Todo(form)
        t.user_id = user_id
        t.created_time = int(time.time())
        t.updated_time = t.created_time
        t.save()

        return t

    @classmethod
    def update(cls, form):
        todo_id = int(form['id'])
        t = Todo.find_by(id=todo_id)
        t.title = form['title']
        t.updated_time = int(time.time())
        t.save()
        return t

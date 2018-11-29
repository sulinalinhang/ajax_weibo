from utils import log
from flask import (
    jsonify,
    request,
    Blueprint,
)
from routes import current_user
from models.todo import Todo

todo_api = Blueprint('todo_api', __name__)


# 本文件只返回 json 格式的数据
# 而不是 html 格式的数据
@todo_api.route('/api/todo/all', methods=['GET'])
def all():
    todos = Todo.all_json()
    return jsonify(todos)


@todo_api.route('/api/todo/add', methods=['POST'])
def add():
    # 得到浏览器发送的表单, 浏览器用 ajax 发送 json 格式的数据过来
    # 所以这里我们用新增加的 json 函数来获取格式化后的 json 数据
    form = request.get_json()
    # 创建一个 todo
    u = current_user()
    t = Todo.add(form, u.id)
    # 把创建好的 todo 返回给浏览器
    return jsonify(t.json())


@todo_api.route('/api/todo/delete', methods=['GET'])
def delete():
    todo_id = int(request.args['id'])
    Todo.delete(todo_id)
    d = dict(
        message="成功删除 todo"
    )
    return jsonify(d)


@todo_api.route('/api/todo/update', methods=['POST'])
def update():
    """
    用于增加新 todo 的路由函数
    """
    form = request.get_json()
    log('api todo update form', form)
    t = Todo.update(form)
    return jsonify(t.json())

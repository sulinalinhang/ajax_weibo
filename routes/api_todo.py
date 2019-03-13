from utils import log
from flask import (
    jsonify,
    request,
    Blueprint,
)
from routes import current_user
from models.todo import Todo

todo_api = Blueprint('todo_api', __name__)


@todo_api.route('/api/todo/all', methods=['GET'])
def all():
    todos = Todo.all_json()
    return jsonify(todos)


@todo_api.route('/api/todo/add', methods=['POST'])
def add():
    form = request.get_json()
    u = current_user()
    t = Todo.add(form, u.id)
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
    form = request.get_json()
    log('api todo update form', form)
    t = Todo.update(form)
    return jsonify(t.json())

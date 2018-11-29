import functools

from models.todo import Todo
from flask import (
    render_template,
    Blueprint,
    redirect,
    request,
    url_for,
)
from routes import (
    redirect,
    current_user,
    login_required,
)
from utils import log

todo_view = Blueprint('todo_view', __name__)


@todo_view.route('/todo/index')
@login_required
def index():
    """
    todo 首页的路由函数
    """
    return render_template('todo_index.html')


def same_user_required(route_function):
    """
    这个函数看起来非常绕，所以你不懂也没关系
    就直接拿来复制粘贴就好了
    """

    @functools.wraps(route_function)
    def f():
        log('same_user_required')
        u = current_user()
        if 'id' in request.query:
            todo_id = request.args['id']
        else:
            todo_id = request.form['id']
        t = Todo.find_by(id=int(todo_id))

        if t.user_id == u.id:
            return route_function(request)
        else:
            return redirect(url_for('todo.index'))

    return f


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
    return render_template('todo_index.html')


def same_user_required(route_function):
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


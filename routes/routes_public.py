from flask import (
    render_template,
    Blueprint,
    send_from_directory,
    request
)

from routes import (
    current_user,
)

public = Blueprint('public', __name__)


@public.route('/')
def index():
    u = current_user()
    return render_template('index.html', username=u.username)


@public.route('/static')
def static():
    filename = request.args['file']
    return send_from_directory('static', filename)

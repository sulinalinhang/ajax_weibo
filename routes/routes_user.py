from urllib.parse import unquote_plus

from flask import (
    render_template,
    current_app,
    Blueprint,
    redirect,
    request,
    url_for,
)

from models.user_role import UserRole
from models.session import Session
from routes import (
    current_user,
    random_string,
)

from utils import log
from models.user import User

user = Blueprint('user', __name__)


@user.route('/user/login', methods=['POST'])
def login():
    form = request.form

    u, result = User.login(form)
    redirect_to_index = redirect(
        url_for('user.login_view', result=result)
    )

    if u.role != UserRole.guest:
        session_id = random_string()
        form = dict(
            session_id=session_id,
            user_id=u.id,
        )
        Session.new(form)
        response = current_app.make_response(redirect_to_index)
        response.set_cookie('session_id', value=session_id)
        return response
    else:
        return redirect_to_index


@user.route('/user/login/view', methods=['GET'])
def login_view():
    u = current_user()
    result = request.args.get('result', '')
    result = unquote_plus(result)

    return render_template(
        'login.html',
        username=u.username,
        result=result,
    )


@user.route('/user/register', methods=['POST'])
def register():
    form = request.form

    u, result = User.register(form.to_dict())
    log('register post', result)
    return redirect(
        url_for('user.register_view', result=result)
    )


@user.route('/user/register/view', methods=['GET'])
def register_view():
    result = request.args.get('result', '')
    result = unquote_plus(result)

    return render_template('register.html', result=result)

from utils import log
from routes import (
    # json_response,
    current_user,
    login_required,
)
from flask import (
    url_for,
    request,
    redirect,
    jsonify,
    Blueprint,
    current_app,
    render_template,
)
from models.weibo import Weibo
from models.comment import Comment
from models.user import User
from functools import wraps


def weibo_owner_required(route_function):
    @wraps(route_function)
    def f():
        u = current_user()
        if 'id' in request.args:
            weibo_id = request.args['id']
        else:
            weibo_id = request.get_json()['id']
        w = Weibo.one_for_id(id=int(weibo_id))
        if w.user_id == u.id:
            return route_function()
        else:
            d = dict(
                message="权限不足"
            )
            return jsonify(d)
    return f

def comment_owner_required(route_function):
    @wraps(route_function)
    def f():
        u = current_user()
        if 'id' in request.args:
            comment_id = request.args['id']
        else:
            comment_id = request.get_json()['id']
        c = Comment.one_for_id(id=int(comment_id))
        if c.user_id == u.id or c.weibo_id == u.id:
            log('AAAA')
            return route_function()
        else:
            d = dict(
                message="权限不足"
            )
            return jsonify(d)
    return f

bp = Blueprint('api_weibo', __name__)
# 本文件只返回 json 格式的数据
# 而不是 html 格式的数据
@bp.route('/api/weibo/all', methods=['GET'])
@login_required
def all():
    weibos = Weibo.all_json()
    comments = Comment.all_json()
    for weibo in weibos:
        weibo['comments'] = []
        for comment in comments:
            if weibo['id'] == comment['weibo_id']:
                weibo['comments'].append(comment)
        log('这是一个微博', weibo, type(weibo))
        weibo['username'] = User.one_for_id(id=weibo['user_id']).username
        log('这是U', User.one_for_id(id=weibo['user_id']).username)

    log('这是comm', weibos)
    return jsonify(weibos)


@bp.route('/api/weibo/add', methods=['POST'])
@login_required
def add():
    # 得到浏览器发送的表单, 浏览器用 ajax 发送 json 格式的数据过来
    # 所以这里我们用新增加的 json 函数来获取格式化后的 json 数据
    form = request.get_json()
    u = current_user()
    form['user_id'] = u.id
    w = Weibo.new(form)
    w.username = User.one_for_id(id=u.id).username
    return jsonify(w.json())


@bp.route('/api/weibo/delete', methods=['GET'])
@login_required
@weibo_owner_required
def delete():
    weibo_id = int(request.args['id'])
    Weibo.delete(weibo_id)
    comments = Comment.all(id=weibo_id)
    # log('AAAA', comments)
    for comment in comments:
        # log('BBB', comment['id'])
        Comment.delete(comment.id)
    d = dict(
        message="成功删除 weibo"
    )
    return jsonify(d)


@bp.route('/api/weibo/update', methods=['POST'])
@login_required
@weibo_owner_required
def update():
    """
    用于增加新 todo 的路由函数
    """
    form = request.get_json()
    id = form['id']
    content = form['content']
    log('api todo update form', form)
    w = Weibo.update(id, content=content)
    log()
    return jsonify(w.json())

@bp.route('/api/comment/add', methods=['POST'])
@login_required
def comment_add():
    form = request.get_json()
    u = current_user()
    form['user_id'] = u.id
    c = Comment.new(form)
    log(c)
    return jsonify(c.json())

@bp.route('/api/comment/delete', methods=['GET'])
@login_required
@comment_owner_required
def comment_delete():
    comment_id = int(request.args['id'])
    log('AAAAA', comment_id)
    Comment.delete(comment_id)
    d = dict(
        message="成功删除 comment"
    )
    return jsonify(d)

@bp.route('/api/comment/update', methods=['POST'])
@login_required
@comment_owner_required
def comment_update():
    """
    用于增加新 todo 的路由函数
    """
    form = request.get_json()
    log('api todo update form', form)
    c = Comment.comment_update(form)
    return jsonify(c.json())


# def route_dict():
#     d = {
#         '/api/weibo/all': login_required(all),
#         '/api/weibo/add': login_required(add),
#         '/api/weibo/delete': login_required(weibo_owner_required(delete)),
#         '/api/weibo/update': login_required(weibo_owner_required(update)),
#         '/api/comment/add': login_required(comment_add),
#         '/api/comment/delete': login_required(comment_owner_required(comment_delete)),
#         '/api/comment/update': login_required(comment_owner_required(comment_update)),
#     }
#     return d

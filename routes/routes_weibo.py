# from models.comment import Comment
from models.weibo import Weibo
from functools import wraps
from routes import (
    current_user,
    login_required,
)

from flask import (
    url_for,
    request,
    redirect,
    Blueprint,
    current_app,
    render_template,
)
from utils import log


def same_user_required(route_function):
    @wraps(route_function)
    def f():
        log('same_user_required')
        u = current_user()
        if 'id' in request.args:
            weibo_id = request.args['id']
        else:
            weibo_id = request.form['id']
        w = Weibo.find_by(id=int(weibo_id))

        if w.user_id == u.id:
            return route_function()
        else:
            return redirect('/weibo/index')

    return f


bp = Blueprint('routes_weibo', __name__)


@bp.route('/weibo/index', methods=['GET'])
@login_required
def index():
    u = current_user()
    weibos = Weibo.all(user_id=u.id)
    # weibos = Weibo.find_all()
    # 替换模板文件中的标记字符串
    log('所有微博', weibos)
    # body = GuaTemplate.render('weibo_index.html', weibos=weibos, user=u)
    return render_template(
        'weibo_index.html',
        weibos=weibos,
        user=u,
    )


@bp.route('/weibo/add', methods=['POST'])
@login_required
def add():
    u = current_user()
    form = request.form
    form['user_id'] = u.id
    Weibo.new(form)
    # Weibo.add(form, u.id)
    # 浏览器发送数据过来被处理后, 重定向到首页
    # 浏览器在请求新首页的时候, 就能看到新增的数据了
    # return redirect('/weibo/index')
    return redirect('/weibo/index')


@bp.route('/weibo/delete', methods=['GET'])
@login_required
@same_user_required
def delete():
    weibo_id = int(request.args['id'])
    Weibo.delete(weibo_id)
    return redirect('/weibo/index')


@bp.route('/weibo/edit', methods=['GET'])
@login_required
@same_user_required
def edit():
    weibo_id = int(request.args['id'])
    w = Weibo.one_for_id(id=weibo_id)
    # body = GuaTemplate.render('weibo_edit.html', weibo=w)
    return render_template('weibo_edit.html', weibo=w)


@bp.route('/weibo/update', methods=['POST'])
@login_required
@same_user_required
def update():
    form = request.form
    id = form['id']
    Weibo.update(id, form)
    return redirect('/weibo/index')


# @bp.route('/comment/add', methods=['POST'])
# @login_required
# def comment_add():
#     u = current_user()
#     form = request.form
#     weibo = Weibo.find_by(id=int(form['weibo_id']))
#
#     c = Comment(form)
#     c.user_id = u.id
#     c.weibo_id = weibo.id
#     c.save()
#     log('comment add', c, u, form)
#
#     return redirect('/weibo/index')


# def route_dict():
#     """
#     路由字典
#     key 是路由(路由就是 path)
#     value 是路由处理函数(就是响应)
#     """
#     d = {
#         '/weibo/add': login_required(add),
#         '/weibo/delete': login_required(same_user_required(delete)),
#         '/weibo/edit': login_required(same_user_required(edit)),
#         '/weibo/update': login_required(same_user_required(update)),
#         '/weibo/index': login_required(index),
#         # 评论功能
#         '/comment/add': login_required(comment_add),
#     }
#     return d

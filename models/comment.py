# from models import Model
from models.user import User
from models.base_model import SQLModel
# from models.weibo import Weibo


class Comment(SQLModel):
    """
    评论类
    """
    sql_create = '''
        CREATE TABLE `comment` (
            `id` INT NOT NULL AUTO_INCREMENT,
            `content` VARCHAR(100) NOT NULL,
            `user_id` INT NOT NULL,
            `weibo_id` INT NOT NULL,
            PRIMARY KEY (`id`)
        )'''
    def __init__(self, form, user_id=-1):
        super().__init__(form)
        self.content = form.get('content', '')
        # 和别的数据关联的方式, 用 user_id 表明拥有它的 user 实例
        self.user_id = form.get('user_id', user_id)
        self.weibo_id = int(form.get('weibo_id', -1))

    def user(self):
        u = User.one_for_id(id=self.user_id)
        return u

    @classmethod
    def comment_update(cls, form):
        id = form['id']
        content = form['content']
        # c = Comment.find_by(id=comment_id)
        Comment.update(id, content=content)
        c = Comment.one_for_id(id=id)

        return c

    # def weibo(self):
    #     from models.weibo import Weibo
    #     w = Weibo.find_by(id=self.weibo_id)
    # return w

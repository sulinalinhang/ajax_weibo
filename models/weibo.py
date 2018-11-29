# from models import Model
from models.base_model import SQLModel
# from models.comment import Comment


class Weibo(SQLModel):
    """
    微博类
    """
    sql_create = '''
        CREATE TABLE `weibo` (
            `id` INT NOT NULL AUTO_INCREMENT,
            `content` VARCHAR(100) NOT NULL,
            `user_id` INT NOT NULL,
            PRIMARY KEY (`id`)
        )'''
    def __init__(self, form):
        super().__init__(form)
        self.content = form.get('content', '')
        # 和别的数据关联的方式, 用 user_id 表明拥有它的 user 实例
        self.user_id = form.get('user_id', None)

    # @classmethod
    # def add(cls, form, user_id):
    #     # w = Weibo(form)
    #     form['user_id'] = user_id
    #     w = Weibo.new(form)
    #
    #     return w

    # @classmethod
    # def weibo_update(cls, form):
    #     id = form['id']
    #     content = form['content']
    #     # w = Weibo.one_for_id(id=id)
    #     # w.title = form['title']
    #     Weibo.update(id, content=content)
    #     w = Weibo.one_for_id(id=id)
    #     return w

    # def comments(self):
    #     cs = Comment.find_all(weibo_id=self.id)
    #     return cs
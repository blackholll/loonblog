from django.db import models

# Create your models here.


class Comment(models.Model):
    """
    评论
    """
    obj_type_id = models.IntegerField('对象类别')  # 1.博客 2.评论
    obj_id = models.IntegerField('对象id')
    username = models.CharField('用户名', max_length=50, null=True, blank=True)
    name = models.CharField('姓名', max_length=50, null=True, blank=True)
    email = models.EmailField('邮箱', null=True, blank=True)
    content = models.TextField('内容')
    source_ip = models.CharField('来源ip', max_length=20)

    creator = models.CharField('创建人', max_length=50)
    gmt_created = models.DateTimeField('创建时间', auto_now_add=True, help_text="")
    gmt_modified = models.DateTimeField('修改时间', auto_now=True, help_text="")
    is_deleted = models.BooleanField('已删除', default=False)

    def get_replys(self):
        """
        评论的回复
        :return:
        """
        return Comment.objects.filter(obj_type_id=2, obj_id=self.id, is_deleted=False)

from django.db import models

# Create your models here.


class Topic(models.Model):
    """
    专题
    """
    name = models.CharField('名称', max_length=50)

    creator = models.CharField('创建人', max_length=50)
    gmt_created = models.DateTimeField('创建时间', auto_now_add=True, help_text="")
    gmt_modified = models.DateTimeField('修改时间', auto_now=True, help_text="")
    is_deleted = models.BooleanField('已删除', default=False)

    class Meta:
        verbose_name = '专题'
        verbose_name_plural = '专题'



class Category(models.Model):
    """
    分类
    """
    name = models.CharField('名称', max_length=50)

    creator = models.CharField('创建人', max_length=50)
    gmt_created = models.DateTimeField('创建时间', auto_now_add=True, help_text="")
    gmt_modified = models.DateTimeField('修改时间', auto_now=True, help_text="")
    is_deleted = models.BooleanField('已删除', default=False)

    class Meta:
        verbose_name = '分类'
        verbose_name_plural = '分类'



class Tag(models.Model):
    """
    标签
    """
    name = models.CharField('名称', max_length=50)

    creator = models.CharField('创建人', max_length=50)
    gmt_created = models.DateTimeField('创建时间', auto_now_add=True, help_text="")
    gmt_modified = models.DateTimeField('修改时间', auto_now=True, help_text="")
    is_deleted = models.BooleanField('已删除', default=False)

    class Meta:
        verbose_name = '标签'
        verbose_name_plural = '标签'


class Blog(models.Model):
    """
    博客
    """
    title = models.CharField('名称', max_length=500)
    topic_id = models.IntegerField('主题id', null=True, blank=True)
    category_id = models.IntegerField('分类id')
    view_count = models.IntegerField('访问次数', default=0)   # 非实时更新，请求次数写入redis。 当redis值大于10时候再更新数据库

    content = models.TextField('内容')
    creator = models.CharField('创建人', max_length=50)
    gmt_created = models.DateTimeField('创建时间', auto_now_add=True, help_text="")
    gmt_modified = models.DateTimeField('修改时间', auto_now=True, help_text="")
    is_deleted = models.BooleanField('已删除', default=False)


class BlogTag(models.Model):
    """
    博客标签
    """
    blog_id = models.IntegerField('博客id')
    tag_id = models.IntegerField('标签id')

    creator = models.CharField('创建人', max_length=50)
    gmt_created = models.DateTimeField('创建时间', auto_now_add=True, help_text="")
    gmt_modified = models.DateTimeField('修改时间', auto_now=True, help_text="")
    is_deleted = models.BooleanField('已删除', default=False)

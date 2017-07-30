from django.db import models

# Create your models here.

class AboutMe(models.Model):
    """
    关于我
    """
    description = models.TextField('内容')

    creator = models.CharField('创建人', max_length=50)
    gmt_created = models.DateTimeField('创建时间', auto_now_add=True, help_text="")
    gmt_modified = models.DateTimeField('修改时间', auto_now=True, help_text="")
    is_deleted = models.BooleanField('已删除', default=False)

class AboutLoonapp(models.Model):
    """
    关于loonapp
    """
    description = models.TextField('内容')

    creator = models.CharField('创建人', max_length=50)
    gmt_created = models.DateTimeField('创建时间', auto_now_add=True, help_text="")
    gmt_modified = models.DateTimeField('修改时间', auto_now=True, help_text="")
    is_deleted = models.BooleanField('已删除', default=False)

class AboutCopyright(models.Model):
    """
    关于版权
    """
    description = models.TextField('内容')

    creator = models.CharField('创建人', max_length=50)
    gmt_created = models.DateTimeField('创建时间', auto_now_add=True, help_text="")
    gmt_modified = models.DateTimeField('修改时间', auto_now=True, help_text="")
    is_deleted = models.BooleanField('已删除', default=False)


from django.contrib.auth.base_user import AbstractBaseUser,BaseUserManager
from django.db import models

# Create your models here.



class MyUserManager(BaseUserManager):
    def create_user(self, email, username, password=None, dep=0):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            username = username,
            email=self.normalize_email(email),

        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username,password):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email=self.normalize_email(email),
            username=username,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class MyUser(AbstractBaseUser):
    """
    用户模型
    """
    username = models.CharField(u'用户名', max_length=20, unique=True)
    chinese_name = models.CharField(u'中文名',max_length=20)
    email = models.EmailField(u'邮箱', max_length=50, unique=True)

    is_staff = models.BooleanField(u'职员', default=True)
    is_active = models.BooleanField(u'激活', default=True)
    is_admin = models.BooleanField(u'管理员', default=False)
    objects = MyUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def get_chinese_name(self):
        # The user is identified by their email address
        return self.chinese_name

    def get_short_name(self):
        # The user is identified by their email address
        return self.chinese_name

    def get_username(self):
        # The user is identified by their email address
        return self.username

    def get_full_name(self):
        # The user is identified by their email address
        return self.chinese_name

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        return True


    # On Python 3: def __str__(self):
    def __unicode__(self):
        return self.chinese_name



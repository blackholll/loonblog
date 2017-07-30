# loonblog
基于django的个人博客系统 a blog base django

## 介绍
- 本系统基于python(3.5)+ django(1.11.2)开发
- 前端使用的是 http://www.dannysite.com/ 曾经的开源版本。 后端全部本人重写的
- 欢迎访问我的个人博客 http://www.loonapp.com，使用的是本项目代码部署


## 部署说明:
- 目录结构说明
     
     apps: 功能模块列表，如博客、评论、图片、账号等等功能
     
     loonblog: 路由及wsgi配置
     
     media: 媒体文件，用于blog文章中的图片及附件保存路径
     
     requirement: 依赖说明，分为生产、开发、线上环境的依赖说明
     
     service: 服务层，具体的逻辑，与view分离
     
     settings: 配置文件，分为生产、开发、线上环境
     
     static: 静态文件
     
     templates: 模板文件
   
- 安装依赖
    1. 建议使用虚拟环境部署，请百度 virtualenv和virtualenvwrapper用法
    2. 进入虚拟环境，cd到项目根目录，pip install -r requirement/pro.txt
  
- 配置文件
    1. 复制settings/dev.py为settings.pro，修改必要的配置，如DEBUG、MEDIA目录、数据库配置、日志文件路径等
    

- 收集静态文件（本系统部分使用了django自带的admin后台的功能）
    1. python manager collectstatic

- 数据库初始化
    1. python manage.py makemigrations
    2. python manage.py migrate

- 创建管理员账号
    1. python manage.py creatsuperuser
    
- 其他
    1. 开发环境可以直接 python manager.py runserver
    2. 线上环境建议使用nginx+uwsgi来部署.可参考 http://www.loonapp.com/blog/1/

## 如何写博客

- 登录管理员账号
    1. 点击页面下方的"管理登录"
    2. 使用上面创建的账号密码登录
    
- 点击下方的"文章管理"
    1. 注意:因为首页使用了缓存（默认5分钟），所以登录后还是显示的"管理登录"（这个后续会优化下）,你可以登陆后访问系统首页，然后点击上方的"文章"后，页面下方就会出现"文章管理"
    了

    
  
  



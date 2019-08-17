from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand
from app import create_app, db
from app.models import Source, Article, User, BlogInfo, BlogView

app = create_app()
manager = Manager(app)
migrate = Migrate(app,db)
manager.add_command('ab',MigrateCommand)

# jinjia2 全局环境变量定义
app.jinja_env.globals['BlogInfo'] = BlogInfo
app.jinja_env.globals['Source'] = Source
app.jinja_env.globals['Article'] = Article
app.jinja_env.globals['BlogView'] = BlogView

# 上下文函数
def make_shell_context():
    return dict(db=db, Source=Source, Article=Article, User=User,
                BlogInfo=BlogInfo, BlogView=BlogView)

manager.add_command("shell", Shell(make_context=make_shell_context))

# 部署函数
@manager.command
def deploy(deploy_type):
    from flask_migrate import upgrade
    from app.models import BlogInfo, User, Source, BlogView
    # 导入数据模型
    # from app.models import ......

    # upgrade database to the latest version
    upgrade()

    if deploy_type == 'product':
        # step_1:insert basic blog info
        BlogInfo.insert_blog_info()
        # step_2:insert admin account
        User.insert_admin(email='master@xxx.com', username='master', password='root')
        # step_3:insert source
        Source.insert_sources()
        # step_4:insert blog view
        BlogView.insert_view()

    # You must run `python manage.py deploy(product)` before run `python manage.py deploy(test_data)`
    elif deploy_type == 'test_data':
        Article.generate_fake(20)

    else:
        pass

if __name__ == '__main__':
    manager.run()

from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

from apps import create_app
from models import *

app = create_app()
manager = Manager(app)
migrate = Migrate(app, db, render_as_batch=True)
manager.add_command('db', MigrateCommand)


@manager.option('--app_id', dest='app_id', help='app_id', default='fof_username')
@manager.option('--app_sec', dest='app_sec', help='app_sec', default='fof_password')
def init_sec(app_id, app_sec):

    # create
    u = AuthSecret(
        app_id=app_id,
        app_sec=app_sec,
    )
    u.save()
    print('\033[32m {} 创建成功！！！请牢记您的账号和密码。'.format(app_id))


if __name__ == '__main__':
    manager.run()



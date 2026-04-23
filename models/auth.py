from werkzeug.security import generate_password_hash, check_password_hash
from bases.dbwrapper import db, BaseModel


class AuthSecret(BaseModel):
    """账户管理"""
    __tablename__ = 'auth_secret'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    app_id = db.Column(db.String(127), unique=True)
    app_sec_hash = db.Column(db.String(127))
    last_date = db.Column(db.String(20))
    date_token_num = db.Column(db.String(20))
    last_auth_time = db.Column(db.DATETIME)

    @property
    def app_sec(self):
        raise AttributeError("当前属性不可读")

    @app_sec.setter
    def app_sec(self, value):
        self.app_sec_hash = generate_password_hash(value)

    def check_app_hash(self, app_sec):
        return check_password_hash(self.app_sec_hash, app_sec)




from flask import Flask

from flask_sqlalchemy import SQLAlchemy

from flask_cors import CORS


class Config():
    ECRET_KEY = "asdasda"
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:4343594.@127.0.0.1:3306/webserver"
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    MAX_CONTENT_LENGTH = 40 * 1024 * 1024
    SQLALCHEMY_POOL_SIZE = 1024
    SQLALCHEMY_POOL_TIMEOUT = 90
    SQLALCHEMY_POOL_RECYCLE = 3
    SQLALCHEMY_MAX_OVERFLOW = 1024


app = Flask(__name__)
app.config.from_object(Config)
CORS(app)
db = SQLAlchemy(app)


class Item(db.Model):
    # 事项id
    __tablename__ = "item_info"
    id = db.Column(db.Integer, primary_key=True)
    # 事项内容
    content = db.Column(db.Text, nullable=False)
    # 事项完成状态,已完成为1，待办为0，默认为待办
    status = db.Column(db.Integer, nullable=False)
    # 事项添加 时间
    addtime = db.Column(db.String(255), nullable=False)
    # 事项截止时间
    deadline = db.Column(db.String(255), nullable=False)

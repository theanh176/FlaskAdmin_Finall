from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_login import LoginManager

app = Flask("__name__")
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:11111111@localhost/dbhospital?charset=utf8mb4"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
app.secret_key = "!@*$&(@*#&(!d"


db = SQLAlchemy(app=app)
admin = Admin(app=app, name="HOSPITAL", template_mode="bootstrap4")
admin_Login = LoginManager(app=app)

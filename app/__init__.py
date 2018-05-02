from flask import Flask,render_template
from flask_sqlalchemy import SQLAlchemy
import pymysql
import os
from flask_mail import Mail

app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://root:root@127.0.0.1:3306/ethos'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['UP_DIR'] =os.path.join(os.path.abspath(os.path.dirname(__file__)),'static/')
app.debug=True
app.config['SECRET_KEY']='x\xaccgzR\xbeN\xec\xa5*\x12\x1a)\xb0\xca\x0f\xe1A$\xcd\xf4\x07\xf9'

app.config['SECURITY_PASSWORD_SALT'] = '\xda{\xeawq>B\xdc\xf8P\x0eC<\xe1\xd8P\x11{\x08&\xf7\xba\x0e*'

app.config['MAIL_DEBUG'] = True             # 开启debug，便于调试看信息
app.config['MAIL_SUPPRESS_SEND'] = False    # 发送邮件，为True则不发送
app.config['MAIL_SERVER'] = 'smtp.163.com'   # 邮箱服务器
app.config['MAIL_PORT'] = 465              # 端口
app.config['MAIL_USE_SSL'] = True           # 重要，qq邮箱需要使用SSL
app.config['MAIL_USE_TLS'] = False          # 不需要使用TLS
app.config['MAIL_USERNAME'] = '17091390354@163.com'  # 填邮箱
app.config['MAIL_PASSWORD'] = 'zxc949461747'      # 填授权码
app.config['MAIL_DEFAULT_SENDER'] = '17091390354@163.com'  # 填邮箱，默认发送者

mail = Mail(app)

db=SQLAlchemy(app)

from app.home import home as home_blueprint
from app.admin import admin as admin_blueprint


app.register_blueprint(home_blueprint)
app.register_blueprint(admin_blueprint,url_prefix='/admin')

@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html') ,404
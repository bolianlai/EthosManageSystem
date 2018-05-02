#coding:utf8
from . import home
from app.models import Accounts,Email_Already,Stats
from app.home.forms import RegistForm ,LoginForm#,UserForm,PwdForm,CommentForm
from flask import Flask, render_template, redirect, url_for, flash, session, request,abort
from functools import wraps
from app import db, app
from datetime import datetime
from werkzeug.utils import secure_filename
import os, stat
from werkzeug.security import generate_password_hash,check_password_hash
import json
from itsdangerous import URLSafeTimedSerializer
from flask_mail import Message
from app import mail
import win_unicode_console
win_unicode_console.streams.stdout_text_transcoded.buffer = win_unicode_console.streams.stdout_text_str
win_unicode_console.enable()


# 登陆验证装饰器
def user_login_req(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user" not in session:
            return redirect(url_for("home.login", error='您未登录！'))
        if 'user' in session and session['confirmed']==0:
            return redirect(url_for("home.login", error='请验证邮箱后登陆！'))
        return f(*args, **kwargs)
    return decorated_function

def user_redister_req(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user" not in session:
            return redirect(url_for("home.register", error='无效验证，请重新注册验证邮箱！'))
        return f(*args, **kwargs)
    return decorated_function

def timestran(s):
    days=int(int(s)/(24*3600))
    time = int((int(s) - days * 24 * 3600) / 3600)
    minute = int((int(s) - days * 24 * 3600 - time * 3600) / 60)
    return str(days)+"天"+str(time)+"时"+str(minute)+"分"

def is_expired(s):
    nowtime = datetime.now()
    updatetime = datetime.strptime(s,"%Y-%m-%d %H:%M:%S")
    if (nowtime - updatetime).seconds>5:
        return False
    return True


@home.route('/')
def index():
    return render_template('index.html')

@home.route('/index/<username>')
@user_login_req
def userpage(username):
    account=Accounts.query.filter_by(username=username).first()
    #statuslist=Stats.query.filter_by(rack_loc=account.username).all()
    statuslist=Stats.query.filter_by(rack_loc="XMR131").all()
    if datetime.now().strftime("%Y-%m-%d %H:%M:%S") > str(account.stop_vip):
        account.is_vip=0
        db.session.add(account)
        db.session.commit()
        account = Accounts.query.filter_by(username=username).first()
    if account.is_vip:
        return render_template('home/index.html',statuslist=statuslist[0:account.display_num],timestran=timestran,stop_vip=account.stop_vip,username=username,is_expired=is_expired)
    else:
        flash('您当前不是会员,只能显示五条矿机信息,注册VIP会员后才能显示余下信息！','ok')
        return render_template('home/index.html',statuslist=statuslist[0:5],timestran=timestran,stop_vip=None,username=username,is_expired=is_expired)




@home.route('/login/',methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        data=form.data
        account=data['account']
        account=Accounts.query.filter_by(username=account).first()
        if not account.check_pass_hash(data['pwd']):
            return redirect(url_for('home.login',error='密码错误!'))
        session['user'] = data['account']
        session['confirmed'] = 1

        return redirect(url_for('home.userpage',username=data['account']))
    return render_template('home/login.html',form=form)

@home.route('/logout/')
def logout():
    session.pop("user", None)
    session.pop("confirmed", None)
    return redirect(url_for('home.login'))



@home.route('/register/',methods=['GET','POST'])
def register():
    form = RegistForm()
    if form.validate_on_submit():
        data = form.data
        account = data['account']
        pwd =generate_password_hash(data['pwd']),
        miners = data['miners']
        username=Accounts.query.filter_by(username=account).first()
        if not username:
            username = Accounts(
                username=account,
                pass_hash=pwd,
                miners=miners,
            )
        username.pass_hash=pwd
        username.miners=miners
        db.session.add(username)
        db.session.commit()
        token = generate_confirmation_token(data['account'])
        confirm_url = url_for('home.confirm_email', token=token, _external=True)
        subject = "Ethos注册激活验证"
        send_email(data['account'], subject, confirm_url)
        session['user'] = data['account']
        session['confirmed'] = 0
        return redirect(url_for("home.login",error='激活邮件已发送，请激活邮箱后登陆！'))
    return render_template('home/register.html', form=form)

def generate_confirmation_token(username):
    serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    return serializer.dumps(username, salt=app.config['SECURITY_PASSWORD_SALT'])

def confirm_token(token, expiration=3600):
    serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    try:
        username = serializer.loads(
            token,
            salt=app.config['SECURITY_PASSWORD_SALT'],
            max_age=expiration
        )
    except:
        return False
    return username

@home.route('/confirm/<token>')
@user_redister_req
def confirm_email(token):
    form = RegistForm()
    try:
        username = confirm_token(token)
    except:
        return redirect(url_for("home.register",error='激活验证过期,请重新注册验证邮箱！'))
    username = Accounts.query.filter_by(username=username).first()
    if username:
        if username.confirmed==1:
            return redirect(url_for("home.login",error="账号已经激活！请直接登陆!"))
        username.confirmed = 1
        username.confirmed_on = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        db.session.add(username)
        db.session.commit()
        session['user']=username.username
        session['confirmed']=1
        return redirect(url_for("home.index"))
    else:
        return redirect(url_for("register",error='无效验证，请重新注册验证邮箱！'))

def send_email(to, subject, confirm_url):
    msg = Message(
        subject=subject,
        recipients=[to, ],
        html="<p>Welcome! Thanks for signing up. Please follow this link to activate your account:</p><p><a href='" + confirm_url + "'" + ">" + confirm_url + "</a></p><br><p>Cheers!</p>",
        sender=app.config['MAIL_DEFAULT_SENDER']
    )
    mail.send(msg)




    # form = RegistForm()
    # if request.method == 'GET':
    #     return render_template('register.html', title='注册', form=form)
    # elif request.method == 'POST':
    #     username = request.form['username']
    #     password = request.form['password']
    #     sql_info = search_accounts_sql(username)
    #     if len(sql_info) > 0:
    #         if sql_info[0][4] == 1:
    #             return redirect(url_for('login', error='账户已存在！请直接登陆！'))
    #         if sql_info[0][4] == 0:
    #             password = generate_password_hash(password)
    #             update_account(sql_info[0][4], password)
    #             token = generate_confirmation_token(username)
    #             confirm_url = url_for('confirm_email', token=token, _external=True)
    #             subject = "Please confirm your email"
    #             send_email(username, subject, confirm_url)
    #             session['user'] = username
    #             session['auto'] = ''
    #             return redirect(url_for('login', error='！'))
    # else:
    #     password = generate_password_hash(password)
    #     insert_sql_accounts(username, password)
    #     token = generate_confirmation_token(username)
    #     confirm_url = url_for('confirm_email', token=token, _external=True)
    #     subject = "Please confirm your email"
    #     send_email(username, subject, confirm_url)
    #     session['user'] = username
    #     session['auto'] = ''
    #     return redirect(url_for("login", error="验证邮箱后登陆"))
    # return render_template('home/register.html')
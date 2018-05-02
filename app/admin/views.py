#coding:utf8
from . import admin
from app.models import Accounts,Admin
from app.admin.forms import LoginForm,EditForm
from flask import Flask, render_template, redirect, url_for, flash, session, request,abort
from functools import wraps
from app import db, app
from datetime import datetime
from werkzeug.security import generate_password_hash
import json

# 登陆验证装饰器
def user_login_req(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "adminuser" not in session:
            return redirect(url_for("admin.login", error='您未登录！'))
        return f(*args, **kwargs)
    return decorated_function

@admin.route('/login/',methods=['GET','POST'])
def login():
    form=LoginForm()
    if form.validate_on_submit():
        data=form.data
        account=data['account']
        account=Admin.query.filter_by(name=account).first()
        if not account.check_pwd(data['pwd']):
            return redirect(url_for('admin.login',error='密码错误!'))
        session['adminuser'] = data['account']
        return redirect(url_for('admin.userpage'))
    return render_template('admin/login.html',form=form)

@admin.route('/logout/')
def logout():
    session.pop("adminuser", None)
    return redirect(url_for('admin.login'))



@admin.route('/')
@user_login_req
def userpage():
    accountlist=Accounts.query.filter_by().all()
    return render_template('admin/index.html', accountlist=accountlist)


@admin.route('/delete/<id>')
@user_login_req
def delete(id):
    if not id:
        return redirect('admin.userpage')
    account = Accounts.query.filter_by(id=id).first_or_404()
    db.session.delete(account)
    db.session.commit()
    flash('删除用户成功！', 'ok')
    return redirect('admin.userpage')

@admin.route('/edit/')
@admin.route('/edit/<id>',methods=['GET','POST'])
@user_login_req
def edit(id=None):
    form=EditForm()
    if not id:
        return render_template('admin/edit.html', form=form, id=id)
    if form.validate_on_submit():
        #print(form.data)
        data=form.data
        account=data['account']
        account=Accounts.query.filter_by(username=account).first_or_404()
        if data['pwd']:
            account.pass_hash = generate_password_hash(data['pwd'])
        account.registered_on = data['registered_on']
        account.confirmed=data['confirmed'] if data['is_vip'] else 0
        account.confirmed_on=data['confirmed_on'] if data['is_vip'] else None
        account.is_vip=data['is_vip'] if data['is_vip'] else None
        account.stop_vip=data['stop_vip'] if data['is_vip'] else None
        account.display_num=data['display_num'] if data['is_vip'] else None
        print(account)
        db.session.add(account)
        db.session.commit()
        flash('用户修改成功！','ok')
        return redirect(url_for('admin.userpage'))
    account = Accounts.query.filter_by(id=id).first_or_404()
    return render_template('admin/edit.html', form=form,account=account, id=id)
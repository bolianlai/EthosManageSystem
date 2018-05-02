# coding=utf-8
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField, FileField, TextAreaField, SelectField, \
    DateField, SelectMultipleField, RadioField, BooleanField
from wtforms.validators import DataRequired, ValidationError, EqualTo, Email, Regexp
from app.models import *


class RegistForm(FlaskForm):
    account=StringField(
        label='邮箱',
        validators=[
            DataRequired("请输入邮箱！"),
            Email("邮箱格式不正确！")
        ],
        description='邮箱',
        render_kw={
            "class":"",
            "placeholder":"请输入邮箱！",
        }
    )
    pwd=PasswordField(
        label='密码',
        validators=[
            DataRequired("请输入密码！"),
        ],
        description='密码',
        render_kw={
            "class":"",
            "placeholder":"请输入密码！"
        }
    )
    repwd = PasswordField(
        label='确认密码',
        validators=[
            DataRequired("请输入确认密码！"),
            EqualTo('pwd', message="两次密码不一致！")
        ],
        description='确认密码',
        render_kw={
            "class": "",
            "placeholder": "请输入确认密码！",
        }
    )
    miners = StringField(
        label='6位字符串',
        validators=[
            DataRequired("请输入6位字符串作为你的唯一标识！"),
        ],
        description='6位字符串',
        render_kw={
            "class": "",
            "placeholder": "请输入6位字符串作为你的唯一标识！",
        }
    )

    submit = SubmitField(
        "注册",
        render_kw={
            "class": "",
            "style": "width: 300px;height: 45px;border: none;color:  # FFFFFF;font - size: 14px;background: red;cursor: pointer;"

        }
    )


    def validate_account(self, field):
        account = field.data
        account_count = Accounts.query.filter_by(username=account).first()
        if account_count:
            if account_count.confirmed==1:
                raise ValidationError("该邮箱已存在！请直接登陆！")



    def validate_miners(self, field):
        miners = field.data

        if len(miners)!=6:
            raise ValidationError('字符不符合格式！')
        miners_count = Accounts.query.filter_by(miners=miners).count()
        if miners_count == 1:
            raise ValidationError('该标识已被使用！')



class LoginForm(FlaskForm):
    account = StringField(
        label='邮箱',
        validators=[
            DataRequired("请输入邮箱！")
        ],
        description='账号',
        render_kw={
            "class": "",
            "placeholder": "请输入邮箱！",
        }
    )
    pwd = PasswordField(
        label='密码',
        validators=[
            DataRequired("请输入密码！")
        ],
        description='密码',
        render_kw={
            "class": "",
            "placeholder": "请输入密码！",
        }
    )
    submit = SubmitField(
        "登陆",
        render_kw={
            "class": "",
            "style":"width: 300px;height: 45px;border: none;color:  # FFFFFF;font - size: 14px;background: red;cursor: pointer;"
        }
    )

    def validate_account(self, field):
        account = field.data
        account_count = Accounts.query.filter_by(username=account).count()
        if account_count == 0:
            raise ValidationError('无效账号！')


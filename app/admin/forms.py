# coding=utf-8
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField, FileField, TextAreaField, SelectField, \
    DateField, SelectMultipleField, RadioField, BooleanField
from wtforms.validators import DataRequired, ValidationError, EqualTo, Email, Regexp
from app.models import *

class LoginForm(FlaskForm):
    account = StringField(
        label='管理员账号',
        validators=[
            DataRequired("请输入管理员账号！")
        ],
        description='账号',
        render_kw={
            "class": "",
            "placeholder": "请输入管理员账号！",
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
        account_count = Admin.query.filter_by(name=account).count()
        if account_count == 0:
            raise ValidationError('无效账号！')


class EditForm(FlaskForm):
    account = StringField(
        label='账号',
        validators=[
            DataRequired("请输入用户账号！")
        ],
        description='用户账号',
        render_kw={
            "class": "",
            "placeholder": "请输入用户账号！",
        }
    )
    pwd = PasswordField(
        label='密码',
        # validators=[
        #     DataRequired("请输入密码！")
        # ],
        description='密码',
        render_kw={
            "class": "",
            "placeholder": "请输入密码！",
        }
    )
    registered_on = StringField(
        label='注册时间',
        # validators=[
        #     DataRequired("请选择注册时间！")
        # ],
        description='注册时间',
        render_kw={
            "class": "form-control input_release_time",
            "placeholder": "注册时间",
        }
    )
    miners = StringField(
        label='6位字符串',
        # validators=[
        #     DataRequired("请输入6位字符串作为唯一标识！"),
        # ],
        description='6位字符串',
        render_kw={
            "class": "",
            "placeholder": "请输入6位字符串作为唯一标识！",
        }
    )

    confirmed = StringField(
        label='激活',
        # validators=[
        #     DataRequired("激活:1 | 非激活：0"),
        # ],
        description='激活',
        render_kw={
            "class": "",
            "placeholder": "激活:1 | 非激活：0",
        }
    )
    confirmed_on = StringField(
        label='激活时间',
        # validators=[
        #     DataRequired("请选择激活时间！")
        # ],
        description='激活时间',
        render_kw={
            "class": "form-control input_release_time",
            "placeholder": "激活时间",
        }
    )

    is_vip = StringField(
        label='VIP',
        # validators=[
        #     DataRequired("VIP:1 | 非VIP：0"),
        # ],
        description='VIP',
        render_kw={
            "class": "",
            "placeholder": "VIP:1 | 非VIP：0",
        }
    )
    stop_vip = StringField(
        label='会员到期时间',
        # validators=[
        #     DataRequired("请选择会员到期时间！")
        # ],
        description='会员到期时间',
        render_kw={
            "class": "form-control input_release_time",
            "placeholder": "请选择会员到期时间！",
        }
    )
    display_num = StringField(
        label='展示数据条数',
        # validators=[
        #     DataRequired("请输入展示数据条数！")
        # ],
        description='展示数据条数',
        render_kw={
            "class": "",
            "placeholder": "请输入展示数据条数！",
        }
    )
    submit = SubmitField(
        "编辑",
        render_kw={
            "class": "btn btn-defaultbtn-primary btn-lg",
            "data-toggle":"modal",
            "data-target":"#myModal"
        }
    )

    # def validate_miners(self, field):
    #     miners = field.data
    #     # if len(miners)!=6:
    #     #     raise ValidationError('字符不符合格式！')
    #     miners_count = Accounts.query.filter_by(miners=miners).count()
    #     if miners_count == 1:
    #         raise ValidationError('该标识已被使用！')

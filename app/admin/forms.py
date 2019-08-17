# coding:utf-8
from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, TextAreaField, SubmitField, \
    PasswordField
from wtforms.validators import DataRequired, Length, Email, EqualTo


class CommonForm(FlaskForm):
    source = SelectField(u'博文来源', coerce=int, validators=[DataRequired()])


class SubmitArticlesForm(CommonForm):
    title = StringField(u'标题', validators=[DataRequired(), Length(1, 64)])
    content = TextAreaField(u'博文内容', validators=[DataRequired()])
    summary = TextAreaField(u'博文摘要', validators=[DataRequired()])


class ManageArticlesForm(CommonForm):
    pass


class DeleteArticleForm(FlaskForm):
    articleId = StringField(validators=[DataRequired()])


class DeleteArticlesForm(FlaskForm):
    articleIds = StringField(validators=[DataRequired()])


class CustomBlogInfoForm(FlaskForm):
    title = StringField(u'博客标题', validators=[DataRequired()])
    signature = TextAreaField(u'个性签名', validators=[DataRequired()])


class ChangePasswordForm(FlaskForm):
    old_password = PasswordField(u'原来密码', validators=[DataRequired()])
    password = PasswordField(u'新密码', validators=[
        DataRequired(), EqualTo('password2', message=u'两次输入密码不一致！')])
    password2 = PasswordField(u'确认新密码', validators=[DataRequired()])


class EditUserInfoForm(FlaskForm):
    username = StringField(u'昵称', validators=[DataRequired()])
    email = StringField(u'电子邮件', validators=[DataRequired(), Length(1, 64), Email()])
    password = PasswordField(u'密码确认', validators=[DataRequired()])

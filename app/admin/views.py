# coding:utf-8
import json
from flask import render_template, redirect, flash,\
    url_for, request, current_app, jsonify
from flask_login import login_required, current_user
from . import admin
from ..models import Source, Article, BlogInfo
from .forms import SubmitArticlesForm, DeleteArticleForm, ManageArticlesForm, \
    DeleteArticlesForm, CustomBlogInfoForm, ChangePasswordForm, EditUserInfoForm
from .. import db

@admin.route('/')
@login_required
def manager():
    return render_template('admin/admin_base.html')

@admin.route('/submit-articles', methods=['GET','POST'])
@login_required
def submitArticles():
    form = SubmitArticlesForm()

    sources = [(s.id, s.name) for s in Source.query.all()]
    form.source.choices = sources

    if form.is_submitted():
        title = form.title.data
        source_id = form.source.data
        content = form.content.data
        summary = form.summary.data

        source = Source.query.get(source_id)

        if source :
            article = Article(title=title, content=content, summary=summary, source=source)
            db.session.add(article)
            db.session.commit()
            flash(u"发布成功",'success')
            article_id = Article.query.filter_by(title=title).first().id
            return redirect(url_for('main.articleDetails', id=article_id))
    if form.errors:
        flash(u"发布失败", 'Error')

    return render_template('admin/submit_articles.html', form=form)


@admin.route('/manage-articles', methods=['GET', 'POST'])
@login_required
def manage_articles():
    source_id = request.args.get('source_id', -1, type=int)
    form = ManageArticlesForm(request.form, source=source_id)
    form2 = DeleteArticleForm()  # for delete an article
    from3 = DeleteArticlesForm()  # for delete articles

    sources = [(s.id, s.name) for s in Source.query.all()]
    sources.append((-1, u'全部来源'))
    form.source.choices = sources

    pagination_search = 0

    if form.validate_on_submit() or \
            (request.args.get('types_id') is not None and request.args.get('source_id') is not None):

        if form.validate_on_submit():
            source_id = form.source.data
            page = 1
        else:
            source_id = request.args.get('source_id', type=int)
            form.source.data = source_id
            page = request.args.get('page', 1, type=int)

        result = Article.query.order_by(Article.create_time.desc())
        if source_id != -1:
            source = Source.query.get_or_404(source_id)
            result = result.filter_by(source=source)
        pagination_search = result.paginate(
                page, per_page=current_app.config['ARTICLES_PER_PAGE'], error_out=False)

    if pagination_search != 0:
        pagination = pagination_search
        articles = pagination_search.items
    else:
        page = request.args.get('page', 1, type=int)
        pagination = Article.query.order_by(Article.create_time.desc()).paginate(
                page, per_page=current_app.config['ARTICLES_PER_PAGE'],
                error_out=False)
        articles = pagination.items

    return render_template('admin/manage_articles.html', Article=Article,
                           articles=articles, pagination=pagination,
                           endpoint='admin.manage_articles',
                           form=form, form2=form2, form3=from3,
                           source_id=source_id, page=page)


@admin.route('/manage-article/delete-article', methods=['GET', 'POST'])
@login_required
def delete_article():
    source_id = request.args.get('source_id', -1, type=int)
    form = DeleteArticleForm()

    if form.validate_on_submit():
        articleId = int(form.articleId.data)
        article = Article.query.get_or_404(articleId)
        db.session.delete(article)
        try:
            db.session.commit()
        except:
            db.session.rollback()
            flash(u'删除失败！', 'danger')
        else:
            flash(u'成功删除博文！', 'success')
    if form.errors:
        flash(u'删除失败！', 'danger')

    return redirect(url_for('admin.manage_articles', source_id=source_id,
                            page=request.args.get('page', 1, type=int)))


@admin.route('/manage-articles/delete-articles', methods=['GET', 'POST'])
@login_required
def delete_articles():
    source_id = request.args.get('source_id', -1, type=int)

    form = DeleteArticlesForm()

    if form.validate_on_submit():
        articleIds = json.loads(form.articleIds.data)
        for articleId in articleIds:
            article = Article.query.get_or_404(int(articleId))
            db.session.delete(article)
        try:
            db.session.commit()
        except:
            db.session.rollback()
            flash(u'删除失败！', 'danger')
        else:
            flash(u'成功删除%s篇博文！' % len(articleIds), 'success')
    if form.errors:
        flash(u'删除失败！', 'danger')

    return redirect(url_for('admin.manage_articles', source_id=source_id,
                            page=request.args.get('page', 1, type=int)))


@admin.route('/blog-info', methods=['GET', 'POST'])
@login_required
def custom_blog_info():
    form = CustomBlogInfoForm()
    bloginfo = BlogInfo.query.first()
    if form.validate_on_submit():
        blog = BlogInfo.query.first()
        blog.title = form.title.data
        blog.signature = form.signature.data
        db.session.add(blog)
        db.session.commit()

        flash(u'修改博客基本信息成功！', 'success')
        return redirect(url_for('admin.custom_blog_info'))

    return render_template('admin/blog_info.html', form=form, bloginfo=bloginfo)

@admin.route('/custom/blog-info/get')
@login_required
def get_blog_info():
    if request.is_xhr:
        blog = BlogInfo.query.first()
        return jsonify({
            'title': blog.title,
            'signature':blog.signature
        })
    return 'OK'

@admin.route('/account/')
@login_required
def account():
    form = ChangePasswordForm()
    form2 = EditUserInfoForm()

    return render_template('admin/admin_account.html',
                           form=form, form2=form2)


@admin.route('/account/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    form = ChangePasswordForm()

    if form.password.data!=form.password2.data:
        return redirect(url_for('admin.account'))

    if form.validate_on_submit():
        if current_user.verify_password(form.old_password.data):
            current_user.password = form.password.data
            db.session.add(current_user)
            db.session.commit()
            flash(u'修改密码成功！', 'success')
            return redirect(url_for('admin.account'))
        else:
            flash(u'修改密码失败！密码不正确！', 'danger')
            return redirect(url_for('admin.account'))


@admin.route('/account/edit-user-info', methods=['GET', 'POST'])
@login_required
def edit_user_info():
    form2 = EditUserInfoForm()

    if form2.validate_on_submit():
        if current_user.verify_password(form2.password.data):
            current_user.username = form2.username.data
            current_user.email = form2.email.data
            db.session.add(current_user)
            db.session.commit()
            flash(u'修改用户信息成功！', 'success')
            return redirect(url_for('admin.account'))
        else:
            flash(u'修改用户信息失败！密码不正确！', 'danger')
            return redirect(url_for('admin.account'))

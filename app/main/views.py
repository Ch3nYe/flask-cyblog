#coding:utf-8
from flask import render_template, request, current_app, redirect,\
    url_for
from . import main
from ..models import Article, BlogView, BlogInfo
from .. import db

@main.route('/index')
def index():
    BlogView.add_view(db)
    bloginfo = BlogInfo.query.first()
    title = bloginfo.title
    signature = bloginfo.signature
    return render_template('index.html', endpoint='.index',Title=title,Signature=signature)

@main.route('/')
def index0():
    return redirect(url_for('main.index'))


@main.route('/post')
def post():
    BlogView.add_view(db)
    page = request.args.get('page', 1, type=int)
    pagination = Article.query.order_by(Article.create_time.desc()).paginate(
        page, per_page=current_app.config['ARTICLES_PER_PAGE'],
        error_out=False
    )
    title = BlogInfo.query.first().title
    articles = pagination.items
    return render_template('post.html', articles=articles,
                           pagination=pagination, endpoint='.post',Titile=title)


@main.route('/article-details/<int:id>', methods=['GET'])
def articleDetails(id):
    BlogView.add_view(db)
    article = Article.query.get_or_404(id)
    article.add_view(article, db)
    return render_template('article_details.html', article=article,
                           endpoint='.articleDetails', id=article.id)
    # page=page, this is used to return the current page args to the
    # disable comment or enable comment endpoint to pass it to the articleDetails endpoint


@main.route('/friends_link')
def friendslink():
        return render_template('friends_link.html')

@main.route('/about')
def about():
        return render_template('about.html')

@main.route('/login')
def MainTestLogin():
    return render_template('testadmin.html')
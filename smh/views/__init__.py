from flask import render_template, flash, redirect, session, url_for, request, abort
from flask.ext.login import login_user, logout_user, current_user, login_required
from smh import app, db, lm, oid, blogic
from smh.forms import LoginForm, NameForm
from smh.models.models import User, Post
from datetime import datetime
from smh.auth import *

@app.route('/posts', methods=['GET', 'POST'])
def posts():
    all_user_posts = Post.query.all()
    session_user_identity = User.query.filter_by(nickname="gogosanka").first()
    session_user_posts = Post.query.filter_by(author=session_user_identity, rebin='false').all()
    session_user_posts_count = Post.query.filter_by(author=session_user_identity, rebin='true').count()
    session_user_recycled_posts = Post.query.filter_by(author=session_user_identity).all()
    session_user_hidden_posts = Post.query.filter_by(author=session_user_identity, hidden='true').all()
    user = 'temp' #create session logins and place user object here
    return render_template('posts-test.html',
                            title="My Pages",
                            user=user,
                            post=session_user_posts,
                            count=session_user_posts_count)

@app.route('/bin', methods=['GET', 'POST'])
def bin():
    session_user_identity = User.query.filter_by(nickname="gogosanka").first()
    session_user_posts_count = Post.query.filter_by(author=session_user_identity, rebin='true').count()
    session_user_recycled_posts = Post.query.filter_by(author=session_user_identity).all()
    user = 'temp' #create session logins and place user object here
    return render_template('bin.html',
                            title="Recycling Bin",
                            user=user,
                            post=session_user_recycled_posts,
                            count=session_user_posts_count)

@app.route('/update', methods=['POST'])
def update_post():
    body = request.form['body']
    author = request.form['author']
    postid = request.form['postid']
    title = request.form['title']
    blogic.update(body,author,postid,title)
    return redirect(url_for('posts'))

@app.route('/edit/<int:postid>/', methods=['GET'])
def edit(postid):
    post_record = Post.query.get(postid)
    if post_record:
        return render_template('edit.html',
                            title="Edit DA Post",
                            post=post_record)
    else:
        return render_template('404.html')

@app.route('/show/<int:postid>/', methods=['GET'])
def show(postid):
    post_record = Post.query.get(postid)
    if post_record:
        return render_template('show.html',
                            title="View Post",
                            post=post_record)
    else:
        return render_template('404.html')


@app.route('/delete/<postid>/', methods=['GET'])
def delete(postid):
    post = Post.query.filter_by(id=postid).first()
    if post:
        blogic.delete(post)
        return redirect(url_for('bin'))
    else:
        return render_template('404.html')

@app.route('/recycle/<postid>/', methods=['GET'])
def recycle(postid):
    post = Post.query.filter_by(id=postid).first()
    if post:
        blogic.recycle(post)
        return redirect(url_for('posts'))
    else:
        return render_template('404.html')

@app.route('/create', methods=['POST'])
def create():
    post = request.form['body']
    author = request.form['author']
    title = request.form['title']
    if post:
        if author:
            blogic.new(post,author,title)
            return redirect(url_for('posts'))
    else:
        return render_template('404.html')

@app.route('/template')
def template():
    return render_template('index2.html')

@app.route('/new')
def new():
    session_user_identity = User.query.filter_by(nickname="gogosanka").first()
    return render_template('create.html',
                            title="My Pages",
                            user = session_user_identity)

@app.route('/index')
def index():
    author = 'temp'
    return render_template('index.html',
                            title="Style Makeup Hair Magazine",
                            author=author)

@auth.route('/login')
def login():
    return render_template('/auth/login.html')

@app.route('/js')
def js():
    return "/static/style/js"

@app.route('/css')
def css():
    return "/static/style/css/"

if __name__ == '__main__':
    app.run()
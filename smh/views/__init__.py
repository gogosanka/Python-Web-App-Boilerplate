from flask import render_template, flash, redirect, session, url_for, request, abort
from flask.ext.login import login_user, logout_user, current_user, login_required
from smh import app, db, lm, blogic
from smh.forms import LoginForm, NameForm, SignupForm
from smh.models.models import User, Post
from datetime import datetime
from smh.auth import *

@app.route('/posts', methods=['GET', 'POST'])
@login_required
def posts():
    feed = Post.query.filter_by(rebin='false').all()
    follower = '0 for now' #count for followers. will need to update the db model
    user = 'Stranger'
    if current_user.is_authenticated():
        user = User.query.filter_by(nickname=current_user.nickname).first()
        posts = Post.query.filter_by(author=user).all()
        posts_count = Post.query.filter_by(author=user, rebin='false').count()
        bin_posts = Post.query.filter_by(author=user, rebin='true').all() #all recycled posts object        
        bin_count = Post.query.filter_by(author=user, rebin='true').count() #recycled posts count
        #hidden_posts = Post.query.filter_by(author=user, rebin='false', hidden='true').all() #make sure to change blogic so that when hidden items are deleted their status goes back to visible
        return render_template('posts-test.html',
                                title="My Pages",
                                user=user,
                                post=posts,
                                posts_count=posts_count,
                                bin_posts=bin_posts,
                                bin_count=bin_count,
                                follower=follower,
                                feed=feed)
    return redirect(url_for('auth.login'))

@app.route('/bin', methods=['GET', 'POST'])
@login_required
def bin():
    feed = Post.query.filter_by(rebin='false').all()
    follower = '0 for now' #count for followers. will need to update the db model
    user = 'Stranger'
    if current_user.is_authenticated():
        user = User.query.filter_by(nickname=current_user.nickname).first()
        posts = Post.query.filter_by(author=user).all()
        posts_count = Post.query.filter_by(author=user, rebin='false').count()
        bin_posts = Post.query.filter_by(author=user, rebin='true').all() #all recycled posts object        
        bin_count = Post.query.filter_by(author=user, rebin='true').count() #recycled posts count
        #hidden_posts = Post.query.filter_by(author=user, rebin='false', hidden='true').all() #make sure to change blogic so that when hidden items are deleted their status goes back to visible
        return render_template('bin.html',
                                title="Recycling Bin",
                                user=user,
                                post=posts,
                                posts_count=posts_count,
                                bin_posts=bin_posts,
                                bin_count=bin_count,
                                follower=follower,
                                feed=feed)
    return render_template('auth/login.html',
                            title="Discover",
                            feed=feed,
                            user=user,
                            follower=follower)

@app.route('/update', methods=['POST'])
@login_required
def update_post():
    body = request.form['body']
    author = request.form['author']
    postid = request.form['postid']
    title = request.form['title']
    blogic.update(body,author,postid,title)
    return redirect(url_for('posts'))

@app.route('/edit/<int:postid>/', methods=['GET'])
@login_required
def edit(postid):
    post = Post.query.get(postid)
    if post:
        return render_template('edit.html',
                            title="Edit Post",
                            post=post)
    else:
        return render_template('404.html')

@app.route('/show/<int:postid>/', methods=['GET'])
@login_required
def show(postid):
    post = Post.query.get(postid)
    if post:
        return render_template('show.html',
                            title="View Post",
                            post=post)
    else:
        return render_template('404.html')


@app.route('/delete/<postid>/', methods=['GET'])
@login_required
def delete(postid):
    post = Post.query.filter_by(id=postid).first()
    if post:
        blogic.delete(post)
        return redirect(url_for('bin'))
    else:
        return render_template('404.html')

@app.route('/recycle/<postid>/', methods=['GET'])
@login_required
def recycle(postid):
    post = Post.query.filter_by(id=postid).first()
    if post:
        blogic.recycle(post)
        if post.rebin == 'true':
            return redirect(url_for('posts'))
        return redirect(url_for('bin'))
    else:
        return render_template('404.html')

@app.route('/create', methods=['POST'])
@login_required
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

@app.route('/modal')
def modal():
    return render_template('modal.html')

@app.route('/new')
@login_required
def new():
    feed = Post.query.filter_by(rebin='false').all()
    follower = '0 for now' #count for followers. will need to update the db model
    user = 'Stranger'
    if current_user.is_authenticated():
        user = User.query.filter_by(nickname=current_user.nickname).first()
        posts = Post.query.filter_by(author=user).all()
        posts_count = Post.query.filter_by(author=user, rebin='false').count()
        bin_posts = Post.query.filter_by(author=user, rebin='true').all() #all recycled posts object        
        bin_count = Post.query.filter_by(author=user, rebin='true').count() #recycled posts count
        #hidden_posts = Post.query.filter_by(author=user, rebin='false', hidden='true').all() #make sure to change blogic so that when hidden items are deleted their status goes back to visible
        return render_template('create.html',
                                title="Discover",
                                user=user,
                                posts_count=posts_count,
                                bin_posts=bin_posts,
                                bin_count=bin_count,
                                follower=follower,
                                feed=feed)
    return render_template('posts.html',
                            title="New Post",
                            user=user,
                            follower=follower)


@app.route('/', methods=['GET'])
@app.route('/discover', methods=['GET'])
def discover():
    feed = Post.query.filter_by(rebin='false').all()
    follower = '0 for now' #count for followers. will need to update the db model
    user = 'Stranger'
    if current_user.is_authenticated():
        user = User.query.filter_by(nickname=current_user.nickname).first()
        posts = Post.query.filter_by(author=user).all()
        posts_count = Post.query.filter_by(author=user, rebin='false').count()
        bin_posts = Post.query.filter_by(author=user, rebin='true').all() #all recycled posts object        
        bin_count = Post.query.filter_by(author=user, rebin='true').count() #recycled posts count
        #hidden_posts = Post.query.filter_by(author=user, rebin='false', hidden='true').all() #make sure to change blogic so that when hidden items are deleted their status goes back to visible
        return render_template('home.html',
                                title="Discover",
                                user=user,
                                posts_count=posts_count,
                                bin_posts=bin_posts,
                                bin_count=bin_count,
                                follower=follower,
                                feed=feed)
    return render_template('home.html',
                            title="Discover",
                            feed=feed,
                            user=user,
                            follower=follower)


@app.route('/login', methods=['GET', 'POST'])
@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    user = 'Stranger'
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            return redirect(request.args.get('next') or url_for('discover'))
        flash('Invalid username or password.')
    return render_template('auth/login.html',
                                title="Log In",
                                form=form,
                                user=user)
@auth.route('/logout')
def logout():
    try:
        logout_user()
        flash('You have been logged out.')
        return redirect(url_for('discover'))
    except:
        return redirect(url_for('discover'))

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    user = 'Stranger'
    if form.validate_on_submit():
        user = User(nickname=form.nickname.data, email=form.email.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
        login_user(user, form.remember_me.data)
        return redirect(request.args.get('next') or url_for('discover'))
    return render_template('signup.html',
                                title="Log In",
                                form=form,
                                user=user)

'''@app.route('/js')
def js():
    return "/static/style/js"

@app.route('/css')
def css():
    return "/static/style/css/"'''

if __name__ == '__main__':
    app.run()
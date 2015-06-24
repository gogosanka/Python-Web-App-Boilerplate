from flask import render_template, flash, redirect, session, url_for, request, jsonify
from flask.ext.login import login_user, logout_user, current_user, login_required
from smh import app, db, lm, oid, blogic
from .forms import LoginForm
from .models import User, Post
import json

@app.route('/posts', methods=['GET', 'POST'])
def posts():
    all_user_posts = Post.query.all()
    user = 'temp' #create session logins and place user object here
    return render_template('posts.html',
                            title="My Pages",
                            user=user,
                            post=all_user_posts)

@app.route('/222', methods=['POST'])
def editpost():
    body = request.form['body']
    author = request.form['author']
    postid = request.form['postid']
    blogic.update(body,author,postid)
    return redirect(url_for('posts'))

@app.route('/edit/<int:postid>/', methods=['GET'])
def edit(postid):
    post = Post.query.get(postid)
    if post:
        return render_template('edit.html',
                            title="Edit DA Post",
                            post=post)
    else:
        return render_template('404.html')

@app.route('/delete/<postid>/', methods=['GET'])
def delete(postid):
    post = Post.query.get(postid)
    if post:
        blogic.delete(post)
        return redirect(url_for('posts'))
    else:
        return render_template('404.html')

@app.route('/create', methods=['POST'])
def create():
    post = request.form['body']
    author = request.form['author']
    if post:
        if author:
            blogic.new(post,author)
            return redirect(url_for('posts'))
    else:
        return render_template('404.html')

@app.route('/new')
def new():
    user = 'temp' #create session logins and place user object here
    return render_template('create.html',
                            title="My Pages")

@app.route('/')
@app.route('/index')
def index():
    author = 'temp'
    return render_template('index.html',
                            title="Style Makeup Hair Magazine",
                            author=author)

@app.route('/static')
def debug():
    return "/static/style/css"

@app.route('/api/users', methods = ['POST'])
def new_user():
    username = request.json.get('username')
    password = request.json.get('password')
    if username is None or password is None:
        abort(400) # missing arguments
    if User.query.filter_by(nickname = username).first() is not None:
        abort(400) # existing user
    this_user = User(nickname = username)
    this_user.hash_password(password)
    db.session.add(this_user)
    db.session.commit()
    return jsonify({ 'username': this_user.nickname }), 201, {'Location': url_for('get_user', id = this_user.id, _external = True)}

@app.route('/api/resource')
# @auth.login_required
def get_resource():
    return jsonify({ 'data': 'Hello, %s!' % g.user.username })

if __name__ == '__main__':
    app.run()
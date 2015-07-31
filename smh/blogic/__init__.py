from smh import db
from smh.models.models import *
from flask import session, redirect, url_for
import datetime

default_titles = ['Lily', 'Jeanna', 'Angelika', 'Ronald', 'Brandie', 'Doreatha', 'Leann', 'Vivienne', 'Sabina', 'Elois', 'Bernita', 'Londa', 'Rosa',
'Alba', 'Blanche', 'Doug', 'Mana', 'Sherrill', 'Masako', 'Rod', 'Herb', 'Myriam', 'Ciara', 'Katy', 'Kisha', 'Kym', 'Xochitl', 'Flo',
 'Sherill', 'Anika', 'Jannie', 'Patti', 'Jamar', 'Delilah', 'Maris', 'Glenna', 'Ling', 'Roselyn', 'Beatris', 'Rae']

def update(body,author,postid,title="Untitled"):
    '''user and data scope is for the database to understand
        who the user is, and then create a Post db object
        containing the author of the post, and the body of
        the post.'''
    post_record = Post.query.filter_by(id=postid).first()
    post_record.body = body
    post_record.title = title
    db.session.commit()

def delete(post):
    '''delete a post.'''
    db.session.delete(post)
    db.session.commit()
    
def recycle(post):
    '''recycle a post'''
    if post.rebin == 'true':
        post.rebin = 'false'
    elif post.rebin == 'false':
        post.rebin = 'true'
    db.session.commit()

def new(post,author,title="Untitled"):
    '''create a new post.'''
    time = datetime.datetime.utcnow()
    user = User.query.filter_by(nickname=author).first()
    entry = Post(body=post, author=user, title=title, timestamp=time, rebin='false', public='true')
    db.session.add(entry)
    db.session.commit()

def check_username(username,password):
    user = User.query.filter_by(nickname=username).first()
    passw = user.password
    if passw == password:
        session['current_user'] = username
        return redirect(url_for('posts'))

def send_vibe(sender, vibe, recipient):
    recipient.vibes.append(vibe)
    db.session.add(recipient)
    db.session.commit()

def delete_vibe(user, vibe):
    user.vibes.remove(vibe)
    db.session.add(user)
    db.session.commit()
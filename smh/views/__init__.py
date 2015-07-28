from flask import render_template, flash, redirect, session, url_for, request, abort, send_from_directory
from flask.ext.login import login_user, logout_user, current_user, login_required
from smh import app, db, lm, blogic
from smh.forms import LoginForm, NameForm, SignupForm, VibeMe, VibeBroadcast
from smh.models.models import User, Post
from datetime import datetime   
from smh.auth import *
from werkzeug import secure_filename
import os

@app.route('/posts/<nickname>', methods=['GET', 'POST'])
@login_required
def posts(nickname):
    feed = Post.query.filter_by(rebin='false').all()
    current = User.query.filter_by(id=current_user.id).first()
    followers = current_user.followers
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
                                followers=followers,
                                feed=feed)
    return redirect(url_for('auth.login'))

#user profile page is the same page that showcases their posts to other users. Also known as magazines in development.
#magazines should have a banner, a grid of recent work, a word cloud of tags that are used by the user, a follow button
#clicking on an image should be a modal popup of the description, also known as tips. if they are videos, it should embed
#is this loa??? can i really have dating, gaming, trading, and content creation in this app??? baybae?
#barter with friends, family, strangers
#anonymous dating, flirting
#showcase your work, art, fashion, etc, with magazines
#create announcements for those who follow you or link your twitter
#boston's own interaction application, interapp...we'll see. even add the "home-for-dinner" interface for the gamers meetup module.
#that's it. it's a moduler networking tool that has a few core apps from viewbook, LOA, and Bayfarm
#also add an inbox feature that works across the main app
@app.route('/admin/allusers', methods=['GET'])
@login_required
def allusers():
    users = User.query.all()
    return render_template('admin/allusers.html', users=users)

#user dashboard/profile
@app.route('/<nickname>', methods=['GET', 'POST'])
@login_required
def profile(nickname):
    feed = Post.query.filter_by(rebin='false').all()
    user = User.query.filter_by(nickname=nickname).first()
    current = User.query.filter_by(id=current_user.id).first()
    if user:
        posts = Post.query.filter_by(author=user).all()
        posts_count = Post.query.filter_by(author=user, rebin='false').count()
        bin_posts = Post.query.filter_by(author=user, rebin='true').all() #all recycled posts object        
        bin_count = Post.query.filter_by(author=user, rebin='true').count() #recycled posts count
        return render_template('profile.html',
                                title="My Pages",
                                user=user,
                                post=posts,
                                posts_count=posts_count,
                                bin_posts=bin_posts,
                                bin_count=bin_count,
                                current=current)
    return redirect(url_for('discover'))

@app.route('/update', methods=['POST'])
@login_required
def update_post():
    body = request.form['body']
    author = request.form['author']
    postid = request.form['postid']
    title = request.form['title']
    post = Post.query.get(postid)
    if post.author.nickname == current_user.nickname:
        blogic.update(body,author,postid,title)
        return redirect(url_for('posts', nickname=current_user.nickname))
    return redirect(url_for('posts', nickname=current_user.nickname))

@app.route('/edit/<int:postid>/', methods=['GET'])
@login_required
def edit(postid):
    if current_user.is_authenticated():
        user = User.query.filter_by(nickname=current_user.nickname).first()
        posts_count = Post.query.filter_by(author=user, rebin='false').count()
        bin_posts = Post.query.filter_by(author=user, rebin='true').all() #all recycled posts object        
        bin_count = Post.query.filter_by(author=user, rebin='true').count() #recycled posts count
        post = Post.query.get(postid)
        if post:
            if post.author.nickname == current_user.nickname:
                return render_template('edit.html',
                                    title="Edit Post",
                                    user=user,
                                    post=post, #recognize that it is written singular tense here, as we are showing 1 post not multiple
                                    posts_count=posts_count,
                                    bin_posts=bin_posts,
                                    bin_count=bin_count,
                                    follower=follower)
            else:
                return redirect(url_for('posts', nickname=current_user.nickname))
        return render_template('404.html')
    else:
        return render_template('404.html')

@app.route('/show/<int:postid>/', methods=['GET'])
@login_required
def show(postid):
    feed = Post.query.filter_by(rebin='false').all()
    follower = '0 for now' #count for followers. will need to update the db model
    user = 'Stranger'
    if current_user.is_authenticated():
        user = User.query.filter_by(nickname=current_user.nickname).first()
        posts_count = Post.query.filter_by(author=user, rebin='false').count()
        bin_posts = Post.query.filter_by(author=user, rebin='true').all() #all recycled posts object        
        bin_count = Post.query.filter_by(author=user, rebin='true').count() #recycled posts count
        post = Post.query.get(postid)
        if post:
            return render_template('show.html',
                                    title="View Post",
                                    user=user,
                                    post=post, #recognize that it is written singular tense here, as we are showing 1 post not multiple
                                    posts_count=posts_count,
                                    bin_posts=bin_posts,
                                    bin_count=bin_count,
                                    follower=follower)
    else:
        return render_template('404.html')

@app.route('/delete/<postid>/', methods=['GET'])
@login_required
def delete(postid):
    post = Post.query.filter_by(id=postid).first()
    if post:
        blogic.delete(post)
        flash("Deleted post!")
        return redirect(url_for('bin', nickname=current_user.nickname))
    else:
        return render_template('404.html')

@app.route('/recycle/<postid>/', methods=['GET'])
@login_required
def recycle(postid):
    post = Post.query.filter_by(id=postid).first()
    if post:
        blogic.recycle(post)
        if post.rebin == 'true':
            flash("Post was sent to recycling bin!")
            return redirect(url_for('profile', nickname=current_user.nickname))
        flash("Your post was restored!")
        return redirect(url_for('bin', nickname=current_user.nickname))
    else:
        return render_template('404.html')

@app.route('/<nickname>/bin', methods=['GET', 'POST'])
@login_required
def bin(nickname=current_user):
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

@app.route('/visible/<postid>/', methods=['GET'])
@login_required
def visible(postid):
    post = Post.query.filter_by(id=postid).first()
    if post:
        if post.public == 'true':
            post.hide()
            flash("Vibe was hidden.")
            return redirect(url_for('profile', nickname=current_user.nickname))
        post.unhide()
        flash("Now sharing vibe.")
        return redirect(url_for('profile', nickname=current_user.nickname))
    else:
        return render_template('404.html')

@app.route('/create', methods=['POST'])
@login_required
def create():
    user = User.query.filter_by(nickname=current_user.nickname).first()
    post = request.form['body']
    author = request.form['author']
    title = request.form['title']
    if post:
        if author:
            blogic.new(post,author,title)
            flash("created post successfully!")
            return redirect(url_for('posts', nickname=current_user.nickname))
    else:
        return render_template('404.html')

#ignore this route until you're done testing vibe creation with db
@app.route('/create_vibe', methods=['POST'])
@login_required
def create_vibe():
    user = User.query.filter_by(nickname=current_user.nickname).first()
    post = request.form['body']
    author = request.form['author']
    title = request.form['title']
    if post:
        if author:
            blogic.new(post,author,title)
            flash("created post successfully!")
            return redirect(url_for('posts', nickname=current_user.nickname))
    else:
        return render_template('404.html')


@app.route('/nopage')
def no_page():
    return render_template('404.html')

@app.route('/modal')
def modal():
    return render_template('modal.html')

@app.route('/posts/<nickname>/new')
@login_required
def new(nickname):
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

#send a vibe to a follower of your choosing
@app.route('/vibewith')
@login_required
def vibebroadcast():
    form = VibeBroadcast()
    if current_user.is_authenticated():
        user = User.query.all()
        #hidden_posts = Post.query.filter_by(author=user, rebin='false', hidden='true').all() #make sure to change blogic so that when hidden items are deleted their status goes back to visible
        return render_template('create-vibe.html', form=form)
    return render_template('posts.html',
                            title="New Post",
                            user=user,
                            follower=follower)

@app.route('/vms')
@app.route('/<nickname>/vms')
@login_required
def myvibes(nickname):
    vibes = current_user.vibes
    if current_user.is_authenticated():
        user = User.query.all()
        #hidden_posts = Post.query.filter_by(author=user, rebin='false', hidden='true').all() #make sure to change blogic so that when hidden items are deleted their status goes back to visible
        return render_template('create-vibe.html', form=form)
    return redirect(url_for('discover'))

#send a vibe directly to someone via their profile
@app.route('/vibewith/<nickname>')
@app.route('/vm/<nickname>')
@app.route('/vm<nickname>')
@login_required
def vibeme(nickname):
    form = VibeMe()
    form.recipient.data = nickname
    if current_user.is_authenticated():
        user = User.query.all()
        #hidden_posts = Post.query.filter_by(author=user, rebin='false', hidden='true').all() #make sure to change blogic so that when hidden items are deleted their status goes back to visible
        return render_template('create-vibe.html', form=form)
    return redirect(url_for('discover'))

@app.route('/', methods=['GET'])
@app.route('/discover', methods=['GET'])
def discover():
    feed = Post.query.filter_by(rebin='false', public='true').all()
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
        user = User.query.filter_by(nickname=form.nickname.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            if request.args.get('next') is url_for('auth.login'):
                return redirect(url_for('discover'))
            return redirect(request.args.get('next') or url_for('discover'))
        flash('Invalid username or password.')
        return render_template('auth/login.html',
                                title="Log In",
                                form=form,
                                user=user)
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
    created_time = datetime.utcnow()
    check_email = User.query.filter_by(email=form.email.data).first()
    check_nickname = User.query.filter_by(nickname=form.nickname.data).first()
    if form.validate_on_submit():
        if not check_email and not check_nickname:
            user = User(nickname=form.nickname.data, created=created_time, email=form.email.data, password=form.password.data)
            db.session.add(user)
            db.session.commit()
            #make user follow themself
            db.session.add(user.follow(user))
            db.session.commit()
            login_user(user, form.remember_me.data)
            flash('Account created successfully!')
            return redirect(request.args.get('next') or url_for('discover'))
        flash('Username or password is already taken. If this is you please sign in.')
    return render_template('signup.html',
                                title="Log In",
                                form=form,
                                user=user)

@app.route('/follow/<nickname>')
@login_required
def follow(nickname):
    #user is the db object of the nickname argument
    user = User.query.filter_by(nickname=nickname).first()
    #current is the db object of the current logged in user
    current = User.query.filter_by(nickname=current_user.nickname).first()
    if user is None:
        flash('User %s not found.' % nickname)
        return redirect(url_for('discover'))
    #check if the current logged in user is the same as the one we are trying to follow
    if user.id == current_user.id:
        flash('You can\'t follow yourself!')
        return redirect(url_for('profile', nickname=nickname))
    #otherwise, let's follow the user!
    u = current.follow(user)
    if u is None:
        flash('Already following ' + nickname + '.')
        return redirect(url_for('profile', nickname=nickname))
    db.session.add(u)
    db.session.commit()
    flash('You are now following ' + nickname + '!')
    return redirect(url_for('profile', nickname=nickname))

@app.route('/unfollow/<nickname>')
@login_required
def unfollow(nickname):
    user = User.query.filter_by(nickname=nickname).first()
    #current is the db object of the current logged in user
    current = User.query.filter_by(id=current_user.id).first()
    if user is None:
        flash('User %s not found.' % nickname)
        return redirect(url_for('discover'))
    if user.id == current_user.id:
        flash('You can\'t unfollow yourself!')
        return redirect(url_for('profile', nickname=nickname))
    u = current.unfollow(user)
    if u is None:
        flash('You are not following ' + nickname + '.')
        return redirect(url_for('profile', nickname=nickname))
    db.session.add(u)
    db.session.commit()
    flash('You have stopped following ' + nickname + '.')
    return redirect(url_for('profile', nickname=nickname))

'''@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return render_template('uploads.html', filename=filename)'''

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            user_folder = ('/'  + current_user.nickname)
            path = app.config['UPLOAD_FOLDER']
            new_path = path + user_folder
            if not os.path.exists(new_path):
                os.makedirs(new_path)
            if not os.path.exists(os.path.join(new_path, filename)):
                file.save(os.path.join(new_path, filename))
            elif os.path.exists(os.path.join(new_path, filename)):
                flash('Filename already exists')
            return redirect(url_for('uploaded_file', filename=filename))
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form action="/upload" method=post enctype=multipart/form-data>
      <p><input type=file name=file>
         <input type=submit value=Upload>
    </form>
    '''

@app.route('/uploaded/<filename>')
def upped(filename):
    path = app.config['UPLOAD_FOLDER']
    new_path = (path + '/' + current_user.nickname + '/')
    return new_path + filename

if __name__ == '__main__':
    app.run()
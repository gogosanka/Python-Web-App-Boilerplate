from smh import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask.ext.login import UserMixin
from smh import lm
from hashlib import md5

@lm.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

'''the db.Model class has a all() method which queries the db
   and returns all the db rows created. For example,
   users = User.query.get(1) #returns the 1st user object
   users.posts.all() #will return all the posts associated with user 1
   the Post class is defined below, and has a relationship within
   the User class, which is why this works.'''

followers = db.Table('followers',
    db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('followed_id', db.Integer, db.ForeignKey('user.id'))
)

vibes = db.Table('vibes',
    db.Column('vibe_id', db.Integer, db.ForeignKey('vibe.id')),
    db.Column('vibing_id', db.Integer, db.ForeignKey('user.id'))
)

tags = db.Table('tags',
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id')),
    db.Column('post_id', db.Integer, db.ForeignKey('post.id'))
) 

class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String(32), index=True, unique=True)
    email = db.Column(db.String(64), index=True, unique=True)
    post = db.relationship('Post', backref='author', lazy='dynamic')
    album = db.relationship('Album', backref='author', lazy='dynamic')
    images = db.relationship('Image', backref='author', lazy='dynamic')
    created = db.Column(db.DateTime)
    about_me =db.Column(db.String(140))
    last_seen = db.Column(db.DateTime)
    followed = db.relationship('User',
                                secondary=followers,
                                primaryjoin=(followers.c.follower_id == id),
                                secondaryjoin=(followers.c.followed_id == id),
                                backref=db.backref('followers', lazy='dynamic'),
                                lazy='dynamic')
    def followed_posts(self):
        return Post.query.join(followers, (followers.c.followed_id == Post.user_id)).filter(followers.c.follower_id == self.id).order_by(Post.timestamp.desc()) #read this thoroughly to understand it
    password_hash = db.Column(db.String(128))
    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')
    @password.setter
    def password(self,password):
        self.password_hash = generate_password_hash(password)
    def verify_password(self,password):
        return check_password_hash(self.password_hash,password)
    def is_anonymous():
        return False
    def get_id(self):
        return (self.id)
    def __repr__(self):
        return (self.nickname)
    def follow(self, user):
        if not self.is_following(user):
            self.followed.append(user)
            return self
    def unfollow(self, user):
        if self.is_following(user):
            self.followed.remove(user)
            return self
    def is_following(self, user):
        return self.followed.filter(followers.c.followed_id == user.id).count() > 0
    def avatar(self, size):
        return 'http://www.gravatar.com/avatar/%s?d=mm&s=%d' % (md5(self.email.encode('utf-8')).hexdigest(), size)

#Vibe Vibes are the easiest way for people to get in touch to do something in particular. 
class Vibe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    vibe_img = db.Column(db.LargeBinary)
    vibe_txt = db.Column(db.String(77))
    timestamp = db.Column(db.DateTime)
    vibe_seen = False
    #vibing_id is the user_id
    vibing = db.relationship('Vibe',
                            secondary=vibes,
                            primaryjoin=(vibes.c.vibe_id == id),
                            secondaryjoin=(vibes.c.vibing_id == id),
                            backref=db.backref('vibers', lazy='dynamic'),
                            lazy='dynamic')
    
class Image(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    image = db.Column(db.LargeBinary)
    timestamp = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    post_id = db.Column(db.String(500), db.ForeignKey('post.id'))

class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(20))
    timestamp = db.Column(db.DateTime)

class Album(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(20))
    timestamp = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    #create an association table for the many-to-many relationship

class Cover(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cover = db.Column(db.LargeBinary)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    main = db.Column(db.Integer)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    rebin = db.Column(db.String(5))
    hidden = db.Column(db.String(5))
    body = db.Column(db.String(500))
    title = db.Column(db.String(32))
    timestamp = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    album_id = db.Column(db.Integer, db.ForeignKey('album.id'))
    tags = db.relationship('Tag', secondary = tags, backref=db.backref('posts', lazy='dynamic'))
    image = db.relationship('Image', backref='post', lazy='dynamic')
    rating = db.Column(db.Boolean)
    def __repr__(self):
        repre = "%r" % self.body
        return str(repre)


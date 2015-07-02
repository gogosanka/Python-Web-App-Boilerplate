from smh import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask.ext.login import UserMixin

'''the db.Model class has a all() method which queries the db
   and returns all the db rows created. For example,
   users = User.query.get(1) #returns the 1st user object
   users.posts.all() #will return all the posts associated with user 1
   the Post class is defined below, and has a relationship within
   the User class, which is why this works.'''

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String(32), index=True, unique=True)
    email = db.Column(db.String(64), index=True, unique=True)
    post = db.relationship('Post', backref='author', lazy='dynamic')
    album = db.relationship('Album', backref='author', lazy='dynamic')
    images = db.relationship('Image', backref='author', lazy='dynamic')
    created = db.Column(db.DateTime)
    password_hash = db.Column(db.String(128))
    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')
    @password.setter
    def password(self,password):
        self.password_hash = generate_password_hash(password)
    def verify_password(self,password):
        return check_password_hash(self.password_hash,password)
    is_authenticated = True
    is_active = True
    is_anonymous = False
    def get_id(self):
        return (self.id)
    def __repr__(self):
        return (self.nickname)

class Image(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    image = db.Column(db.LargeBinary)
    timestamp = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    post_body = db.Column(db.String(500), db.ForeignKey('post.body'))

class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(20))
    timestamp = db.Column(db.DateTime)
    #create an association table for the many-to-many relationship

class Album(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(20))
    timestamp = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    #create an association table for the many-to-many relationship

tags = db.Table('tags', db.Column('tag_id', db.Integer, db.ForeignKey('tag.id')), db.Column('post_id', db.Integer, db.ForeignKey('post.id')))

class Post(db.Model):
    #unique id of the post
    id = db.Column(db.Integer, primary_key=True)
    rebin = db.Column(db.String(5))
    hidden = db.Column(db.String(5))
    #the text data of the post (can be null)
    body = db.Column(db.String(500))
    title = db.Column(db.String(32))
    #the timestamp for each post created
    timestamp = db.Column(db.DateTime)
    #the user who wrote the post (foreign key)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    album_id = db.Column(db.Integer, db.ForeignKey('album.id'))
    tags = db.relationship('Tag', secondary = tags, backref=db.backref('posts', lazy='dynamic'))
    image = db.relationship('Image', backref='post', lazy='dynamic')
    rating = db.Column(db.Boolean)
    def __repr__(self):
        repre = "%r" % self.body
        return str(repre)
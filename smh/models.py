from smh import db
from passlib.apps import custom_app_context as pwd_context

'''the db.Model class has a all() method which queries the db
   and returns all the db rows created. For example,
   users = User.query.get(1) #returns the 1st user object
   users.posts.all() #will return all the posts associated with user 1
   the Post class is defined below, and has a relationship within
   the User class, which is why this works.'''

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String(32), index=True, unique=True)
    # password_hash = db.Column(db.String(128))
    email = db.Column(db.String(120), index=True, unique=True)
    post = db.relationship('Post', backref='author', lazy='dynamic')
    images = db.relationship('Image', backref='uploader', lazy='dynamic')
    created = db.Column(db.DateTime)
    def hash_password(self, password):
        self.password_hash = pwd_context.encrypt(password)
    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)
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
    #create an association table for the many-to-many relationship

tags = db.Table('tags', db.Column('tag_id', db.Integer, db.ForeignKey('tag.id')), db.Column('post_id', db.Integer, db.ForeignKey('post.id')))

class Post(db.Model):
    #unique id of the post
    id = db.Column(db.Integer, primary_key=True)
    #the text data of the post (can be null)
    body = db.Column(db.String(500))
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
from smh import db, models

def update(body,author,postid):
	'''user and data scope is for the database to understand
		who the user is, and then create a Post db object
		containing the author of the post, and the body of
		the post.'''
	post_record = models.Post.query.get(postid)
	post_record.body = body
	post_record.author = models.User(nickname=author)
	db.session.commit()

def delete(post):
	'''delete a post.'''
	db.session.delete(post)
	db.session.commit()
	

def new(post,author):
	'''create a new post.'''
	post_author = models.User(nickname=author)
	post_record = models.Post(body=post, author = post_author)
	db.session.add(post_record)
	db.session.commit()
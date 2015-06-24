from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
album = Table('album', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('title', String(length=20)),
    Column('timestamp', DateTime),
)

image = Table('image', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('image', LargeBinary),
    Column('timestamp', DateTime),
    Column('user_id', Integer),
    Column('post_body', String(length=500)),
)

post = Table('post', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('body', String(length=500)),
    Column('timestamp', DateTime),
    Column('user_id', Integer),
    Column('album_id', Integer),
    Column('rating', Boolean),
)

tag = Table('tag', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('text', String(length=20)),
    Column('timestamp', DateTime),
)

tags = Table('tags', post_meta,
    Column('tag_id', Integer),
    Column('post_id', Integer),
)

user = Table('user', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('nickname', String(length=64)),
    Column('email', String(length=120)),
    Column('password', String(length=12)),
    Column('created', DateTime),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['album'].create()
    post_meta.tables['image'].create()
    post_meta.tables['post'].create()
    post_meta.tables['tag'].create()
    post_meta.tables['tags'].create()
    post_meta.tables['user'].columns['created'].create()
    post_meta.tables['user'].columns['password'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['album'].drop()
    post_meta.tables['image'].drop()
    post_meta.tables['post'].drop()
    post_meta.tables['tag'].drop()
    post_meta.tables['tags'].drop()
    post_meta.tables['user'].columns['created'].drop()
    post_meta.tables['user'].columns['password'].drop()

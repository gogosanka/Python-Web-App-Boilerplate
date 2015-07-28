from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
vibe = Table('vibe', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('vibe_img', BLOB),
    Column('vibe_txt', VARCHAR(length=77)),
    Column('timestamp', DATETIME),
)

vibe = Table('vibe', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('image', LargeBinary),
    Column('message', String(length=77)),
    Column('timestamp', DateTime),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['vibe'].columns['vibe_img'].drop()
    pre_meta.tables['vibe'].columns['vibe_txt'].drop()
    post_meta.tables['vibe'].columns['image'].create()
    post_meta.tables['vibe'].columns['message'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['vibe'].columns['vibe_img'].create()
    pre_meta.tables['vibe'].columns['vibe_txt'].create()
    post_meta.tables['vibe'].columns['image'].drop()
    post_meta.tables['vibe'].columns['message'].drop()

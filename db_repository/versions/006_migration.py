from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
vibe = Table('vibe', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('timestamp', DATETIME),
    Column('image', BLOB),
    Column('message', VARCHAR(length=77)),
)

vibe = Table('vibe', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('image', LargeBinary),
    Column('message', String(length=77)),
    Column('accepted', Boolean),
    Column('accepted_by', Boolean),
    Column('public', Boolean),
    Column('created_timestamp', DateTime),
    Column('seen_timestamp', DateTime),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['vibe'].columns['timestamp'].drop()
    post_meta.tables['vibe'].columns['accepted'].create()
    post_meta.tables['vibe'].columns['accepted_by'].create()
    post_meta.tables['vibe'].columns['created_timestamp'].create()
    post_meta.tables['vibe'].columns['public'].create()
    post_meta.tables['vibe'].columns['seen_timestamp'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['vibe'].columns['timestamp'].create()
    post_meta.tables['vibe'].columns['accepted'].drop()
    post_meta.tables['vibe'].columns['accepted_by'].drop()
    post_meta.tables['vibe'].columns['created_timestamp'].drop()
    post_meta.tables['vibe'].columns['public'].drop()
    post_meta.tables['vibe'].columns['seen_timestamp'].drop()

from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
vibe = Table('vibe', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('vibe_img', LargeBinary),
    Column('vibe_txt', String(length=77)),
    Column('timestamp', DateTime),
)

vibes = Table('vibes', post_meta,
    Column('vibe_id', Integer),
    Column('follower_id', Integer),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['vibe'].create()
    post_meta.tables['vibes'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['vibe'].drop()
    post_meta.tables['vibes'].drop()

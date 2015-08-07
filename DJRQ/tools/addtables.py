from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, SmallInteger, Time, DateTime, Enum
from sqlalchemy.types import TIMESTAMP
from sqlalchemy.orm import sessionmaker
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, backref, joinedload, subqueryload, contains_eager
from sqlalchemy.sql import func, or_
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy_utils.functions import create_database, database_exists
from time import time
from datetime import datetime
from djrq.model import *
import os
import sys

tables_needed = False
print "Connecting to the database"

Base = declarative_base()
engine = create_engine('mysql+oursql://sqlalchemy:password@localhost/ampache1?charset=utf8', echo=False, encoding='utf8')
if not database_exists('mysql+oursql://sqlalchemy:password@localhost/ampache1'):
    create_database('mysql+oursql://sqlalchemy:password@localhost/ampache1')
    tables_needed = True

Session = sessionmaker(bind=engine)
session = Session()

for table, name in ((Artist(), 'Artist'), (Album(), 'Album'), (Song(), 'Song'),
                    (RequestList(), "RequestList"), (Mistags(), "Mistags"),
                    (Played(), "Played"), (Suggestions(), "Suggestions"), (User(), "User"),
                    (SiteOptions(), "SiteOptions"), (Listeners(), "Listeners"), (Account(), "Account"),
                    (Group(), "Group"), (Permission(), "Permission")):
    try:
        table.__table__.create(engine)
    except:
        print "Table %s exists" % name
for table, name in ((account_groups, 'Acccount Groups'), (group_permissions, 'Group Permissions')):
    try:
        table.create(engine)
    except:
        print "Table %s exists" % name

#    ft = "ALTER TABLE :table ADD FULLTEXT idjc (:column)"
#    session.execute("ALTER TABLE artist ADD FULLTEXT idjc (name)", mapper=ampache.Artist)
#    session.execute("ALTER TABLE album ADD FULLTEXT idjc (name)", mapper=ampache.Album)
#    session.execute("ALTER TABLE song ADD FULLTEXT idjc (title)", mapper=ampache.Song)


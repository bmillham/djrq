# Use to create tables needed by DJRQ that Ampache does not use
# Change the ampache_engine line to match your database
# Warning, after running this, you may not be able to update Ampache
# to a newer version, as ampache may not recognize the database as a valid database.
# You will still be able to use your current version of Ampache to update your database.
#
# This script will not run in it's current directory. Copy it up one level to run it!

from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils.functions import create_database, database_exists
from djrq.model import *

print "Connecting to the database"
Base = declarative_base()
ampache_engine = create_engine('mysql+oursql://sqlalchemy:password@localhost/ampache1', echo=False, encoding='utf8')
Session = sessionmaker(bind=ampache_engine)
session = Session()
print "Creating tables needed for DJRQ"
created = 0
need_catalog = False
for table in (RequestList, Mistags, Played, Suggestions, SiteOptions, Listeners, ):
    try:
        table().__table__.create(ampache_engine)
    except:
        print "Table %s already in database, skipping" % table().__tablename__
    else:
        print "Created table %s" % table().__tablename__
        if table().__tablename__ == 'siteoptions': need_catalog = True
        created += 1
session.commit()
print "%d Tables created" % created
if not need_catalog:
    c = session.query(Catalog).filter(Catalog.catalog_type=='local').first()
    print "Setting catalog to:", c.name


from paste.registry import StackedObjectProxy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import *
from sqlalchemy import *
from sqlalchemy.ext.hybrid import hybrid_property
#from auth import *

Base = declarative_base()
metadata = Base.metadata
session = StackedObjectProxy()
prefixes = ['the']
database_type = "PostgreSQL"

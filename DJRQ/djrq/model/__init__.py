from paste.registry import StackedObjectProxy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import *
from sqlalchemy import *
from sqlalchemy.sql import func, or_
from sqlalchemy.types import TIMESTAMP
from sqlalchemy.ext.hybrid import hybrid_property
from time import time
import markupsafe
import paste
from web.core import request
from sqlalchemy.ext.associationproxy import association_proxy
#from auth import *

Base = declarative_base()
metadata = Base.metadata
session = StackedObjectProxy()
prefixes = ['the']

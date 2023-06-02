from sqlalchemy.ext.declarative import declarative_base
from session import createSessionFactory
from config import get_genomicsdb_binds

Sessions = { bind: createSessionFactory(connectionStr) for bind, connectionStr in get_genomicsdb_binds().items() }
Base = declarative_base()


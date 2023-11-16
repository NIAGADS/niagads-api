''' Ontology Term data model '''
from sqlalchemy import select, func, column
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.dialects import postgresql

from shared_resources.db import db




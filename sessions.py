from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session


# TODO -- manage pooling; see https://docs.sqlalchemy.org/en/20/core/pooling.html
def createSessionFactory(connectionString):
    """create session factory from DB connection string
    
    Keyword arguments:
    engine -- connection string
    Return: session factory object
    """
    engine = create_engine(connectionString)
    return sessionmaker(bind=engine)

def getSession(sessionFactory):
    ''' return instantiated session from a session factory '''
    session = scoped_session(sessionFactory)
    return session()
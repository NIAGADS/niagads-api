from flask_sqlalchemy import SQLAlchemy, SignallingSession
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from contextlib import contextmanager

from sessions import createSessionFactory, getSession
from config import get_sql_binds

class MySignallingSession(SignallingSession):
    def __init__(self, db, *args, **kwargs):
        super().__init__(db, *args, **kwargs)
        self.db = db

    def get_bind(self, mapper=None, clause=None):
        if mapper is not None:
            info = getattr(mapper.persist_selectable, 'info', {})
            if info.get('bind_key') == '__all__':
                info['bind_key'] = self.db.context_bind_key
                try:
                    return super().get_bind(mapper=mapper, clause=clause)
                finally:
                    info['bind_key'] = '__all__'
        return super().get_bind(mapper=mapper, clause=clause)


class MySQLAlchemy(SQLAlchemy):
    context_bind_key = None

    @contextmanager
    def context(self, bind=None):
        _context_bind_key = self.context_bind_key
        try:
            self.context_bind_key = bind
            yield
        finally:
            self.context_bind_key = _context_bind_key

    def create_session(self, options):
        return sessionmaker(class_=MySignallingSession, db=self, **options)

    def get_binds(self, app=None):
        binds = super().get_binds(app=app)
        # Restore default engine for table.info.get('bind_key') == '__all__'
        app = self.get_app(app)
        engine = self.get_engine(app, None)
        tables = self.get_tables_for_bind('__all__')
        binds.update(dict((table, engine) for table in tables))
        return binds

    def get_tables_for_bind(self, bind=None):
        result = []
        for table in self.Model.metadata.tables.values():
            if table.info.get('bind_key') == bind or (bind is not None and table.info.get('bind_key') == '__all__'):
                result.append(table)
        return result

# bindings = get_sql_binds()

# genomicsdb_sf = createSessionFactory(bindings['GRCh38'])
# genomicsdb37_sf = createSessionFactory(bindings['GRCh37'])

# genomicsdb_session = getSession(genomicsdb_sf)

genomicsdb = MySQLAlchemy()
# genomicsdb37 = MySQLA

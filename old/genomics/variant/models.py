''' GenomicsDB variant data model '''
from sqlalchemy import select, func, column
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.dialects import postgresql

from shared_resources.db import db
from shared_resources.fields import GenomeBuild
from shared_resources import utils

def get_session(genomeBuild):
    bind_db = GenomeBuild().deserialize(genomeBuild)
    engine = db.get_engine(bind_db)
    return scoped_session(sessionmaker(autocommit=False,
            autoflush=False,
            bind=engine))

def validate_variant(genomeBuild, id):
    dbSession = get_session(genomeBuild)
    result = dbSession.execute(func.find_variant_primary_key(id)).all()
    dbSession.remove()
    return utils.extract_result_data(result)[0]


def get_variant(genomeBuild, ids, full=False, single=False):
    dbSession = get_session(genomeBuild)
    lookupFunc = func.get_variant_primary_keys_and_annotations_tbl(ids).table_valued('lookup_variant_id', 'mapping')
    statement = select(lookupFunc)
    queryResult = dbSession.execute(statement)
   
    dbSession.remove()
    result = utils.extract_variant_result_data(queryResult, fullAnnotation=full)
    if single:
        mapping = result[0]
        if mapping is None:
            return {"message": "No variant with id '" + str(ids) + "' found in the NIAGADS GenomicsDB. "}
        return mapping
    return result
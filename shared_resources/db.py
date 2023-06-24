import logging
from flask_sqlalchemy import SQLAlchemy
from requests import get
from requests.exceptions import HTTPError

# from filer.models import Metadata
from filer.metadata.parsers import FILERMetadataParser
from shared_resources.constants import URLS

db = SQLAlchemy()
logger = logging.getLogger(__name__)

def initialize_FILER_metadata_cache(metadataFileName, debug):
    ''' initializes FILER metadta from the metadata template file '''
    
    try:
        # fetch the template file 
        requestUrl = URLS.gadb_metadata + '/' + metadataFileName
        if debug:
            logger.debug("Fetching FILER metadata from " + requestUrl)
        response = get(requestUrl)
        response.raise_for_status()
        
        metadata = response.text.split('\n')
        header = metadata.pop(0).split('\t')
        if debug:
            logger.debug("Retrieved metadata for " + str(len(metadata)) + " tracks.")
    
        for line in metadata:
            # parse & create Metadata object
            track = FILERMetadataParser(dict(zip(header, line.split('\t')))).parse()
            # db.session.add(Metadata(track))
            
        db.session.commit()
        
    except HTTPError as err:
        raise HTTPError("Unable to fetch FILER metadata", err)
    except Exception as err:
        raise IOError("Unable to parse FILER metadata", err)


def create_tables(app, bind):
    with app.app_context():
        if bind in ['filer', 'all']:
            # db.drop_all('filer')
            # db.create_all('filer')
            initialize_FILER_metadata_cache(app.config['FILER_METADATA_TEMPLATE_FILE'], app.config['DEBUG'])
            
        if bind in ['cache', 'all']:
            True
            # db.drop_all('cache')
            # db.create_all('cache')
    
    
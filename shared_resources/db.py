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
    lineNum = 0
    currentLine = None
    try:
        # fetch the template file 
        requestUrl = URLS.filer_downloads + '/metadata/' + metadataFileName
        if debug:
            logger.debug("Fetching FILER metadata from " + requestUrl)
        response = get(requestUrl)
        response.raise_for_status()
        
        metadata = response.text.split('\n')
        header = metadata.pop(0).split('\t')
        if metadata[-1] == '': metadata.pop()    # file may end with empty line
            
        if debug:
            logger.debug("Retrieved metadata for " + str(len(metadata)) + " tracks.")
    
        for line in metadata:

            lineNum += 1
            currentLine = line
        
            # parse & create Metadata object
            track = FILERMetadataParser(dict(zip(header, line.split('\t')))).parse()

            # db.session.add(Metadata(track))
            if debug and lineNum % 10000 == 0:
                logger.debug("Loaded metadata for " + str(lineNum) +" tracks")
            
        # db.session.commit()
        
    except HTTPError as err:
        raise HTTPError("Unable to fetch FILER metadata", err)
    except Exception as err:
        raise RuntimeError("Unable to parse FILER metadata, problem with line #: " 
                + str(lineNum), currentLine , err)


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
    
    
import logging
from requests import get
from requests.exceptions import HTTPError

# from filer.models import Metadata
from filer.parsers import FILERMetadataParser
from filer.track.models import Track
from shared_resources import constants

logger = logging.getLogger(__name__)

def initialize_metadata_cache(db, metadataFileName, debug):
    ''' initializes FILER metadta from the metadata template file '''
    lineNum = 0
    currentLine = None
    try:
        # fetch the template file 
        requestUrl = constants.URLS.filer_downloads + '/metadata/' + metadataFileName
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
            db.session.add(Track(**track))
            
            if debug and lineNum % 10000 == 0:
                logger.debug("Loaded metadata for " + str(lineNum) +" tracks")
            
        db.session.commit()
        
    except HTTPError as err:
        raise HTTPError("Unable to fetch FILER metadata", err)
    except Exception as err:
        raise RuntimeError("Unable to parse FILER metadata, problem with line #: " 
                + str(lineNum), currentLine , err)

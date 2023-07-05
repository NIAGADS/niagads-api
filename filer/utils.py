import requests
from urllib.parse import urlencode
from copy import deepcopy

from shared_resources import constants


def __genome_build(genomeBuild):
    ''' return genome build in format filer expects '''
    if '38' in genomeBuild:
        return 'hg38'
    if genomeBuild == 'GRCh37':
        return 'hg19'
    return genomeBuild

# ?trackIDs=NGEN000611,NGEN000615,NGEN000650&region=chr1:50000-1500000

def __map_request_params(params):
    ''' map request params to format expected by FILER'''
    # genome build
    newParams = {"outputFormat": "json"}
    if 'assembly' in params:
        newParams['genomeBuild'] = __genome_build(params['assembly'])

    if 'id' in params:
        newParams['trackIDs'] = params['id']

    if 'span' in params:
        newParams['region'] = params['span']
   
    return newParams


# TODO: error checking
def make_request(endpoint, params):
    ''' map request params and submit to FILER API'''
    requestParams = __map_request_params(params)
    requestUrl = constants.URLS.filer_api + "/" + endpoint + ".php?" + urlencode(requestParams)
    response = requests.get(requestUrl)
    return response.json()
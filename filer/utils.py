import requests
from urllib.parse import urlencode
from copy import deepcopy

from shared_resources.constants import URLS


def genome_build(genomeBuild):
    ''' return genome build in format filer expects '''
    if '38' in genomeBuild:
        return 'hg38'
    if genomeBuild == 'GRCh37':
        return 'hg19'
    return genomeBuild


def map_request_params(params):
    ''' map request params to format expected by FILER'''
    # genome build
    if hasattr(params, 'assembly'):
        params.genomeBuild = genome_build(params['assembly'])
        del params['assembly']

    return params


# TODO: error checking
def make_request(endpoint, params):
    ''' map request params and submit to FILER API'''
    requestUrl = URLS.filer + "/" + endpoint + ".php?" + urlencode(map_request_params(deepcopy(params)))
    response = requests.get(requestUrl)
    return response
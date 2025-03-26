from pydantic import BaseModel
from aiohttp import ClientSession
from typing import List, Union

from api.common.enums.genome import Assembly
from api.routers.filer.models.track_overlaps import TrackOverlap, sort_track_overlaps

from .enums import FILERApiEndpoint
from ..models.bed_features import BEDFeature

class FILERApiDataResponse(BaseModel):
    Identifier: str
    features: List[BEDFeature]
    
class ApiWrapperService:
    def __init__(self, session):
        self.__session: ClientSession = session
    
        
    def __map_genome_build(self, assembly: Assembly):
        ''' return genome build value FILER expects '''
        return 'hg19' if assembly == Assembly.GRCh37 \
            else 'hg38'

    def __build_request_params(self, parameters: dict):
        ''' map request params to format expected by FILER'''
        requestParams = {'outputFormat': 'json'}
        
        if 'assembly' in parameters:
            requestParams['genomeBuild'] = self.__map_genome_build(parameters['assembly'])

        if 'track' in parameters:
            # key = "trackIDs" if ',' in params['track_id'] else "trackID"
            requestParams['trackIDs'] = parameters['track']
            
        if 'span' in parameters:
            requestParams['region'] = parameters['span']

        return requestParams


    async def __fetch(self, endpoint: FILERApiEndpoint, params: dict):
        ''' map request params and submit to FILER API'''
        try:
            requestParams = self.__build_request_params(params)
            async with self.__session.get(str(endpoint), params=requestParams) as response:
                result = await response.json() 
            return result
        except Exception as e:
            raise LookupError(f'Unable to get FILER response `{response.content}` for the following request: {str(response.url)}')
    
    
    async def __count_track_overlaps(self, span: str, assembly: str, tracks: List[str]) -> List[TrackOverlap]:   
        # TODO: new FILER endpoint, count overlaps for specific track ID?
        if len(tracks) <= 3: # for now, probably faster to retrieve the data and count, but may depend on span
            response = await self.__fetch(FILERApiEndpoint.OVERLAPS, {'track': ','.join(tracks), 'span': span})
            return [TrackOverlap(track_id=t['Identifier'], num_overlaps=len(t['features'])) for t in response]
        
        else:
            response = await self.get_informative_tracks(span, assembly, sort=True)   
            
            # need to filter all informative tracks for the ones that were requested
            # and add in the zero counts for the ones that have no hits
            informativeTracks = set([t.track_id for t in response]) # all informative tracks
            nonInformativeTracks = set(tracks).difference(informativeTracks) # tracks with no hits in the span
            informativeTracks = set(tracks).intersection(informativeTracks) # informative tracks in the requested list
        
            return [tc for tc in response if tc.track_id in informativeTracks] \
                + [TrackOverlap(track_id=t, num_overlaps=0) for t in nonInformativeTracks]


    async def get_track_hits(self, tracks: List[str], span: str,
        assembly: str, countsOnly: bool=False) -> Union[List[FILERApiDataResponse], List[TrackOverlap]]: 
        
        if countsOnly:
            return await self.__count_track_overlaps(span, assembly, tracks)
        
        result = await self.__fetch(FILERApiEndpoint.OVERLAPS, {'track': ','.join(tracks), 'span': span})
        
        # FIXME: more efficient?

        try:
            return [FILERApiDataResponse(**r) for r in result]
        except:
            raise LookupError(f'Unable to process FILER response for track(s) `{tracks}` in the span: {span} ({assembly})')


    async def get_informative_tracks(self, span: str, assembly: str, sort=False) -> List[TrackOverlap]:
        result = await self.__fetch(FILERApiEndpoint.INFORMATIVE_TRACKS, {'span': span, 'assembly': assembly})
        result = [TrackOverlap(track_id=t['Identifier'], num_overlaps=t['numOverlaps']) for t in result]
        return sort_track_overlaps(result) if sort else result


import asyncio
from typing import Any, List
from fastapi.exceptions import RequestValidationError
from sqlalchemy.ext.asyncio import AsyncSession
from collections import ChainMap
from itertools import groupby
from operator import itemgetter

from niagads.utils.list import cumulative_sum, chunker

from api.common.enums import ResponseContent, CacheNamespace
from api.common.helpers import Parameters, ResponseConfiguration, RouteHelper
from api.common.utils import get_attribute

from .constants import TRACKS_PER_API_REQUEST_LIMIT
from .enums import FILERApiEndpoint
from .services import MetadataQueryService, ApiWrapperService
from ..dependencies import InternalRequestParameters
from ..models.track_metadata_cache import Track

import logging
LOGGER = logging.getLogger(__name__)

    
class FILERRouteHelper(RouteHelper):  
    
    def __init__(self, managers: InternalRequestParameters, responseConfig: ResponseConfiguration, params: Parameters):
        super().__init__(managers, responseConfig, params)
        self._managers: InternalRequestParameters = managers
    

    def __page_data_query(self, trackSummary: dict):
        """ calculate expected result size, number of pages; 
            returns current set of paged tracks"""
        
        # calculate cumulative sum of expected hits per track 
        sortedTrackSummary = sorted(trackSummary, key = lambda item: item['num_overlaps'], reverse=True)
        cumulativeSum = cumulative_sum([t['num_overlaps'] for t in sortedTrackSummary])
        self._resultSize = cumulativeSum[-1] # last element is total number of hits
        
        self.initialize_pagination()
        
        pagedTracks = None
        if self._resultSize <= self._pageSize:
            pagedTracks = [t['track_id'] for t in trackSummary]
        
        else:
            pageRange = self.page_array()
            
            # NOTE: () in the `next` returns an iterator instead of a list 
            # (i.e. instead of []) for dictionary comprehension
            pageStartIndex = next((index for index, counts in enumerate(cumulativeSum) if counts >= pageRange.start))
            pageEndIndex = len(cumulativeSum) - 1 if pageRange.end == self._resultSize \
                else next((index for index, counts in enumerate(cumulativeSum) if counts >= pageRange.start)) - 1
            pagedTracks = [t['track_id'] for t in sortedTrackSummary[pageStartIndex:pageEndIndex]]
        
        return pagedTracks

    
    def __merge_track_lists(self, trackList1, trackList2):
        matched = groupby(sorted(trackList1 + trackList2, key=itemgetter('track_id')), itemgetter('track_id'))
        combinedLists = [dict(ChainMap(*g)) for k, g in matched]
        return combinedLists
    

    async def __validate_tracks(self, tracks: List[str]):
        """ by setting validate=True, the service runs .validate_tracks before validating the genome build"""
        assembly = await MetadataQueryService(self._managers.session).get_genome_build(tracks, validate=True)
        if isinstance(assembly, dict):
            raise RequestValidationError(f'Tracks map to multiple assemblies; please query GRCh37 and GRCh38 data independently')
        return assembly


    async def __get_track_data_task(self, tracks, assembly: str, span: str, countsOnly: bool, cacheKey: str):
        cacheKey += ','.join(tracks)
        result = await self._managers.internalCache.get(cacheKey, namespace=CacheNamespace.FILER_EXTERNAL_API)
        if result is None:   
            result = await ApiWrapperService(self._managers.apiClientSession).get_track_hits(tracks, span, assembly, countsOnly=countsOnly)
            await self._managers.internalCache.set(cacheKey, result, namespace=CacheNamespace.FILER_EXTERNAL_API)
        return result


    async def get_track_data(self, validate=True): 
        isCached = True # assuming true from the start
        cacheKey = self._managers.cacheKey
        
        result = await self._managers.internalCache.get(cacheKey.internal, namespace=cacheKey.namespace)

        if result is None:
            isCached = False
            
            summarize = self._responseConfig.content == ResponseContent.SUMMARY
            countsOnly = self._responseConfig.content == ResponseContent.COUNTS or summarize == True 
            
            tracks = get_attribute(self._parameters, '_paged_tracks', get_attribute(self._parameters, 'track'))
            tracks = tracks.split(',') if isinstance(tracks, str) else tracks
            tracks = sorted(tracks) # best for caching
            
            assembly = get_attribute(self._parameters, 'assembly')
            if validate or assembly is None: # for internal helper calls, don't always need to validate; already done
                assembly = await self.__validate_tracks(tracks)         
                
            cacheKey = f'/{FILERApiEndpoint.OVERLAPS}?countsOnly={countsOnly}&span={self._parameters.span}&tracks=' 
            cacheKey = cacheKey.replace(':', '_')
            
            if countsOnly: # summarize & counts only do not need to be chunked
                result = await self.__get_track_data_task(tracks, assembly, self._parameters.span, countsOnly, cacheKey)
            
                if summarize: # summarize doesn't need to be chunked b/c DB query
                    metadata: List[Track] = await self.get_track_metadata(rawResponse=True)
                    result = self.__merge_track_lists(
                        [t.serialize(promoteObjs=True) for t in metadata], 
                        [t.serialize() for t in result])
                    result = sorted(result, key = lambda item: item['num_overlaps'], reverse=True)
                    # this step will be cached in __generate_response
                    
            else: # make parallel calls for large lists of tracks
                chunks = chunker(tracks, TRACKS_PER_API_REQUEST_LIMIT, returnIterator=True)
                tasks = [self.__get_track_data_task(c, assembly, self._parameters.span, countsOnly, cacheKey) for c in chunks]
                result = await asyncio.gather(tasks)
                
        return await self.generate_response(result, isCached=isCached)


    async def get_track_metadata(self, rawResponse=False):
        """ fetch track metadata; expects a list of track identifiers in the parameters"""
        isCached = True # assuming true from the start
        cacheKey = self._managers.cacheKey.internal
        if rawResponse:
            cacheKey = cacheKey + '&raw'    
        
        result = await self._managers.internalCache.get(
            cacheKey, 
            namespace=self._managers.cacheKey.namespace)
        
        if result is None:
            isCached = False
        
            tracks = get_attribute(self._parameters, '_paged_tracks', get_attribute(self._parameters, 'track'))
            tracks = tracks.split(',') if isinstance(tracks, str) else tracks
            tracks = sorted(tracks) # best for caching & pagination
            
            result = await MetadataQueryService(self._managers.session).get_track_metadata(tracks)
            
            if not rawResponse and len(tracks) > self._pageSize:
                self.initialize_pagination()
                pageRange = self.page_array()
                result = result[pageRange.start:pageRange.end]
            
        if rawResponse:
            # cache the raw response
            await self._managers.internalCache.set(
                cacheKey,
                result, 
                namespace=self._managers.cacheKey.namespace)
            
            return result

        return await self.generate_response(result, isCached=isCached)


    async def search_track_metadata(self, rawResponse=False):
        """ retrieve track metadata based on filter/keyword searches """
        isCached = True # assuming true from the start
        cacheKey = self._managers.cacheKey.internal
        content = ResponseContent.IDS if rawResponse else self._responseConfig.content
        if rawResponse:
            cacheKey = cacheKey + '&raw'    
        
        result = await self._managers.internalCache.get(
            cacheKey, 
            namespace=self._managers.cacheKey.namespace)
        
        if result is None:
            isCached = False
            offset = None

            result = await MetadataQueryService(self._managers.session) \
                .query_track_metadata(self._parameters.assembly, 
                    self._parameters.filter, self._parameters.keyword, ResponseContent.COUNTS)
            
            if content == ResponseContent.COUNTS:
                return self.generate_response(result, isCached=isCached)
            
            self._resultSize = result['track_count']
            
            self.initialize_pagination()
            offset = None if rawResponse else self.offset()
            limit = None if rawResponse else self._pageSize
            
            result = await MetadataQueryService(self._managers.session) \
                .query_track_metadata(self._parameters.assembly, 
                    self._parameters.filter, self._parameters.keyword, content, limit, offset)

        if rawResponse:
            # cache the raw response
            await self._managers.internalCache.set(
                cacheKey,
                result, 
                namespace=self._managers.cacheKey.namespace)
            return result
            
        return await self.generate_response(result, isCached=isCached)


    async def search_track_data(self):
        result = await self._managers.internalCache.get(self._managers.cacheKey.internal, namespace=self._managers.cacheKey.namespace)
        if result is not None: # just return the cached response
            return await self.generate_response(result, isCached=True)
        
        # get list of tracks that match the search filter
        matchingTracks = await self.search_track_metadata(rawResponse=True)
            
        # get informative tracks from the FILER API & cache
        cacheKey = f'/{FILERApiEndpoint.INFORMATIVE_TRACKS}?genomeBuild={self._parameters.assembly}&span={self._parameters.span}' 
        cacheKey = cacheKey.replace(':','_')
        informativeTracks = await self._managers.internalCache.get(cacheKey, namespace=CacheNamespace.FILER_EXTERNAL_API)
        if informativeTracks is None:
            # get tracks with data in the region
            informativeTracks = await ApiWrapperService(self._managers.apiClientSession) \
                .get_informative_tracks(self._parameters.span, self._parameters.assembly)
            # cache this response from the FILER Api
            await self._managers.internalCache.set(cacheKey, informativeTracks, namespace=CacheNamespace.FILER_EXTERNAL_API)
        
        # filter for tracks that match the filter
        matchingTrackIds = matchingTracks 
        informativeTrackIds = [t['track_id'] for t in informativeTracks] 
        targetTrackIds = list(set(matchingTrackIds).intersection(informativeTrackIds))
        targetTracks = [t for t in informativeTracks if t['track_id'] in targetTrackIds]
        
        # page the result
        self._parameters._paged_tracks = self.__page_data_query(targetTracks)
        
        if self._responseConfig.content == ResponseContent.IDS:
            return await self.generate_response(self._parameters._paged_tracks)

        return await self.get_track_data(validate=False)

    
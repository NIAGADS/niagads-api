import asyncio
from typing import List, Optional
from fastapi.exceptions import RequestValidationError
from collections import ChainMap
from itertools import groupby
from operator import itemgetter

from niagads.utils.list import cumulative_sum, chunker
from pydantic import BaseModel

from api.common.enums.cache import CacheKeyQualifier, CacheNamespace
from api.common.enums.database import DataStore
from api.common.enums.genome import FeatureType
from api.common.enums.response_properties import ResponseContent
from api.common.helpers import Parameters, ResponseConfiguration, MetadataRouteHelper, PaginationCursor

from api.common.services.metadata_query import MetadataQueryService
from api.models.genome import Feature
from api.models.response_model_properties import CacheKeyDataModel

from api.routes.filer.common.constants import CACHEDB_PARALLEL_TIMEOUT, TRACKS_PER_API_REQUEST_LIMIT
from api.routes.filer.common.enums import FILERApiEndpoint
from api.routes.filer.common.services import ApiWrapperService, FILERApiDataResponse
from api.routes.filer.dependencies.parameters import InternalRequestParameters
from api.routes.filer.models.bed_features import BEDFeature
from api.models.database.metadata import Track
from api.routes.filer.models.track_overlaps import TrackOverlap, sort_track_overlaps


class FILERPaginationCursor(BaseModel):
    tracks: List[str]
    start: PaginationCursor
    end: PaginationCursor


class FILERRouteHelper(MetadataRouteHelper):  
    
    def __init__(self, managers: InternalRequestParameters, responseConfig: ResponseConfiguration, params: Parameters):
        super().__init__(managers, responseConfig, params, [DataStore.FILER, DataStore.SHARED])

    async def __initialize_data_query_pagination(self, trackOverlaps: List[TrackOverlap]) -> FILERPaginationCursor:
        """ calculate expected result size, number of pages; 
            determines and caches cursor-based pagination
            
            pagination determined as follows:
            
            1. sort track summary in DESC order by number of data points
            2. calculate cumulative sum to estimate result size
            3. create array of `ordered_track_index`:`offset` pairs defining the end point for the current page
                (start point is cursor[page - 1], with cursor[0] always being `0:0`)
            
            returns current set of pagedTracks, and start/end points for slicing within track results
        """
        # sort the track summary
        sortedTrackOverlaps: List[TrackOverlap] = sort_track_overlaps(trackOverlaps)
        
        # generate cache keys
        noPageCacheKey = self._managers.cacheKey.no_page()
        cursorCacheKey = CacheKeyDataModel.encrypt_key(noPageCacheKey + CacheKeyQualifier.CURSOR)
        rsCacheKey = CacheKeyDataModel.encrypt_key(noPageCacheKey + CacheKeyQualifier.RESULT_SIZE)
        
        # check to see if pagination has been cached
        cursors = await self._managers.cache.get(cursorCacheKey, 
            namespace=CacheNamespace.QUERY_CACHE, timeout=CACHEDB_PARALLEL_TIMEOUT)
        self._resultSize = await self._managers.cache.get(rsCacheKey,
                namespace=CacheNamespace.QUERY_CACHE, timeout=CACHEDB_PARALLEL_TIMEOUT)
        
        # if either is uncached, the data may be out of sync so recalculate cache size
        if cursors is None or self._resultSize is None: 
            cumulativeSum = cumulative_sum([t.num_overlaps for t in sortedTrackOverlaps])
            self._resultSize = cumulativeSum[-1] # last element is total number of hits    

            await self._managers.cache.set(rsCacheKey, self._resultSize,
                namespace=CacheNamespace.QUERY_CACHE, timeout=CACHEDB_PARALLEL_TIMEOUT)
            
            self.initialize_pagination() # need total number of pages to find cursors
            
            cursors = ['0:0']
            if self._resultSize > self._pageSize:  # figure out page cursors
                residualRecords = 0
                priorTrackIndex = 0
                offset = 0
                for p in range(1, self._pagination.total_num_pages):
                    sliceRange = self.slice_result_by_page(p)
                    for index, counts in enumerate(cumulativeSum):
                        if counts > sliceRange.end: # end of page  
                            offset = offset + self._pageSize if priorTrackIndex == index \
                                else self._pageSize - residualRecords 
                            cursors.append(f'{index}:{offset}')
                            
                            residualRecords = sortedTrackOverlaps[index].num_overlaps - offset
                            priorTrackIndex = index

                            break
                        
            # end of final page is always the last track, last feature
            cursors.append(f'{len(sortedTrackOverlaps)-1}:{sortedTrackOverlaps[-1].num_overlaps}') 

            # cache the pagination cursor
            await self._managers.cache.set(cursorCacheKey, cursors,
                namespace=CacheNamespace.QUERY_CACHE, timeout=CACHEDB_PARALLEL_TIMEOUT)

        else: # initialize from cached pagination
            self.initialize_pagination()
        
        startTrackIndex, startOffset = [int(x) for x in cursors[self._pagination.page - 1].split(':')]
        endTrackIndex, endIndex = [int (x) for x in cursors[self._pagination.page].split(':')]
        pagedTracks = [t.track_id for t in sortedTrackOverlaps[startTrackIndex:endTrackIndex + 1]]
        
        return FILERPaginationCursor(tracks=pagedTracks,
            # cursor list & start/endTrackIndex is based on all tracks; need to adjust for pagedTrack slice
            start=PaginationCursor(key=0, offset=startOffset),
            end=PaginationCursor(key=endTrackIndex - startTrackIndex, offset=endIndex))
    
    
    def __merge_track_lists(self, trackList1, trackList2):
        matched = groupby(sorted(trackList1 + trackList2, key=itemgetter('track_id')), itemgetter('track_id'))
        combinedLists = [dict(ChainMap(*g)) for k, g in matched]
        return combinedLists
    

    async def __validate_tracks(self, tracks: List[str]):
        """ by setting validate=True, the service runs .validate_tracks before validating the genome build"""
        assembly = await MetadataQueryService(self._managers.metadataSession, dataStore=self._dataStore).get_genome_build(tracks, validate=True)
        if isinstance(assembly, dict):
            raise RequestValidationError(f'Tracks map to multiple assemblies; please query GRCh37 and GRCh38 data independently')
        return assembly


    def __page_data_result(self, cursor: FILERPaginationCursor, data: List[FILERApiDataResponse]) -> List[BEDFeature]:
        
        # sort the response by the cursor pagedTracks so the track order is correct
        # FILER currently processes sequentially so this is unecessary but if updated
        # to process in parallel, it will be required
        sortedResponse = sorted(response, key=lambda  x:cursor.tracks == x.Identifier)
        
        result: List[BEDFeature] = [] 
        for trackIndex, track in enumerate(sortedResponse):
            sliceStart = cursor.start.offset if trackIndex == cursor.start.key \
                else None
            sliceEnd = cursor.end.offset if  trackIndex == cursor.end.key \
                else None
            
            features: List[BEDFeature] = track.features[sliceStart:sliceEnd]
            for f in features:
                f.add_track(track.Identifier)
                result.append(f)
                
        return result
    

    async def __get_track_data_task(self, tracks: List[str], assembly: str, span: str, countsOnly: bool):
        cacheKey = CacheKeyDataModel.encrypt_key(
            f'/{FILERApiEndpoint.OVERLAPS}?assembly={assembly}&countsOnly={countsOnly}'
            + f'&span={span}&tracks={','.join(tracks)}'
            )
        result = await self._managers.cache.get(cacheKey, 
            namespace=CacheNamespace.FILER_EXTERNAL_API, timeout=CACHEDB_PARALLEL_TIMEOUT)
        if result is None:   
            result = await ApiWrapperService(self._managers.apiClientSession) \
                .get_track_hits(tracks, span, assembly, countsOnly=countsOnly)
            await self._managers.cache.set(cacheKey, result, 
                namespace=CacheNamespace.FILER_EXTERNAL_API, timeout=CACHEDB_PARALLEL_TIMEOUT)
        return result
    

    async def __get_gene_qtl_data_task(self, track: str, gene: str):
        cacheKey = CacheKeyDataModel.encrypt_key(
            f'/{FILERApiEndpoint.GENE_QTLS}?'
            + f'&gene={gene}&track={track}')
        result = await self._managers.cache.get(cacheKey, 
            namespace=CacheNamespace.FILER_EXTERNAL_API, timeout=CACHEDB_PARALLEL_TIMEOUT)
        if result is None:   
            result = await ApiWrapperService(self._managers.apiClientSession) \
                .get_gene_qtls(track, gene)
            await self._managers.cache.set(cacheKey, result, 
                namespace=CacheNamespace.FILER_EXTERNAL_API, timeout=CACHEDB_PARALLEL_TIMEOUT)
        return result


    async def __get_paged_track_data(self, trackOverlaps:List[TrackOverlap], validate=True):

        result = await self._managers.cache.get(
            self._managers.cacheKey.encrypt(), namespace=self._managers.cacheKey.namespace)
        if result is not None:
            return await self.generate_response(result, isCached=True)
        
        cursor: FILERPaginationCursor = await self.__initialize_data_query_pagination(trackOverlaps)
        
        assembly = self._parameters.get('assembly')
        if validate or assembly is None: # for internal helper calls, don't always need to validate; already done
            assembly = await self.__validate_tracks(cursor.tracks)     
                    
        chunks = chunker(cursor.tracks, TRACKS_PER_API_REQUEST_LIMIT, returnIterator=True)
        tasks = [self.__get_track_data_task(c, assembly, self._parameters.span, False) for c in chunks]
        chunkedResults = await asyncio.gather(*tasks, return_exceptions=False)
        
        data: List[FILERApiDataResponse] = []
        for r in chunkedResults:
            response = response + r

        result = self.__page_data_result(cursor, response)
        
        return await self.generate_response(result, isCached=False)
    
        
    async def get_track_data(self, validate=True): 
        """ if trackSummary is set, then fetches from the summary not from a parameter"""
        
        cachedResponse = await self._get_cached_response()
        if cachedResponse is not None:
            return cachedResponse
        
        tracks = self._parameters.get('track') 
        tracks = tracks.split(',') if isinstance(tracks, str) else tracks
        tracks = sorted(tracks) # best for caching
        
        assembly = self._parameters.get('assembly')
        if validate or assembly is None: # for internal helper calls, don't always need to validate; already done
            assembly = await self.__validate_tracks(tracks)         
    
        # get counts - needed for full pagination, counts only, summary
        trackOverlaps = await self.__get_track_data_task(tracks, assembly, self._parameters.span, True)
        
        if self._responseConfig.content == ResponseContent.FULL:
            return await self.__get_paged_track_data(trackOverlaps, validate=validate)

        # to ensure pagination order, need to sort by counts
        sortedTrackOverlaps = sort_track_overlaps(trackOverlaps)
        self._resultSize = len(sortedTrackOverlaps)
        self.initialize_pagination()
        sliceRange = self.slice_result_by_page()
        
        match self._responseConfig.content:
            case ResponseContent.IDS:
                result = [t['track_id'] for t in sortedTrackOverlaps[sliceRange.start:sliceRange.end]]
                return await self.generate_response(result)
            
            case ResponseContent.COUNTS:
                # sort by counts to ensure pagination order
                return await self.generate_response(sortedTrackOverlaps[sliceRange.start:sliceRange.end])
            
            case ResponseContent.SUMMARY | ResponseContent.URLS: 
                metadata: List[Track] = await self.get_track_metadata(rawResponse=ResponseContent.SUMMARY)
                summary = self.__generate_track_overlap_summary(metadata, sortedTrackOverlaps)
                result = [t['url'] for t in summary[sliceRange.start:sliceRange.end]] \
                    if self._responseConfig.content == ResponseContent.URLS \
                    else summary[sliceRange.start:sliceRange.end] 
                return await self.generate_response(result)
            
            case _:
                raise RuntimeError('Invalid response content specified')


    def __generate_track_overlap_summary(self, metadata: List[Track], data):
        result = self.__merge_track_lists(
            [t.serialize(promoteObjs=True) for t in metadata], 
            data if isinstance(data[0], dict) else [t.serialize() for t in data])
        result = sorted(result, key = lambda item: item['num_overlaps'], reverse=True)
        return result


    async def search_track_data(self):
        cachedResponse = await self._get_cached_response()
        if cachedResponse is not None:
            return cachedResponse
    
        hasMetadataFilters = self._parameters.keyword is not None or self._parameters.filter is not None
        
        # note: we test for metadata filters twice so we don't
        # need to do the informativeTrack lookup if metadata filters return nothing
        
        # apply metadata filters, if valid
        if hasMetadataFilters:
            # get list of tracks that match the search filter
            rawResponse = ResponseContent.IDS
            if self._responseConfig.content == ResponseContent.SUMMARY:
                rawResponse = ResponseContent.SUMMARY
            matchingTracks: List[Track] = await self.search_track_metadata(rawResponse=rawResponse) 
            
            if len(matchingTracks) == 0:
                self._managers.requestData.add_message('No tracks meet the specified metadata filter criteria.')
                return await self.generate_response([], isCached=False)
        
        # get informative tracks from the FILER API & cache
        cacheKey = f'/{FILERApiEndpoint.INFORMATIVE_TRACKS}?assembly={self._parameters.assembly}&span={self._parameters.span}' 
        cacheKey = CacheKeyDataModel.encrypt_key(cacheKey.replace(':','_'))
        
        informativeTrackOverlaps: List[TrackOverlap] = await self._managers.cache \
            .get(cacheKey, namespace=CacheNamespace.FILER_EXTERNAL_API)
        if informativeTrackOverlaps is None:
            informativeTrackOverlaps = await ApiWrapperService(self._managers.apiClientSession) \
                .get_informative_tracks(self._parameters.span, self._parameters.assembly)
            await self._managers.cache.set(cacheKey, 
                informativeTrackOverlaps, namespace=CacheNamespace.FILER_EXTERNAL_API)
            
        if len(informativeTrackOverlaps) == 0:
            self._managers.requestData.add_message('No overlapping features found in the query region.')
            return await self.generate_response([], isCached=False)
        
        targetTrackOverlaps = informativeTrackOverlaps
        
        if hasMetadataFilters:
            # filter for tracks that match the filter
            matchingTrackIds = [t.track_id for t in matchingTracks] if rawResponse != ResponseContent.IDS else matchingTracks
            informativeTrackIds = [t.track_id for t in informativeTrackOverlaps] 
            targetTrackIds = list(set(matchingTrackIds).intersection(informativeTrackIds))
            targetTrackOverlaps: List[TrackOverlap] = [t for t in informativeTrackOverlaps if t.track_id in targetTrackIds]
        
        if self._responseConfig.content == ResponseContent.FULL:
            return await self.__get_paged_track_data(targetTrackOverlaps)
        
        # to ensure pagination order, need to sort by counts
        result: List[TrackOverlap] = sort_track_overlaps(targetTrackOverlaps)
        self._resultSize = len(result)
        self.initialize_pagination()
        sliceRange = self.slice_result_by_page()
        
        match self._responseConfig.content:
            case ResponseContent.IDS:
                result = [t.track_id for t in result[sliceRange.start:sliceRange.end]]
                return await self.generate_response(result)
            
            case ResponseContent.COUNTS:
                # sort by counts to ensure pagination order
                return await self.generate_response(result[sliceRange.start:sliceRange.end])
            
            case ResponseContent.SUMMARY | ResponseContent.URLS: 
                metadata:List[Track] = [t for t in matchingTracks if t.track_id in targetTrackIds]
                summary = self.__generate_track_overlap_summary(metadata, result)
                result = [t['url'] for t in summary[sliceRange.start:sliceRange.end]] \
                    if self._responseConfig.content == ResponseContent.URLS \
                    else summary[sliceRange.start:sliceRange.end] 
                return await self.generate_response(result)
            
            case _:
                raise RuntimeError('Invalid response content specified')

    async def get_feature_qtls(self):
        cachedResponse = await self._get_cached_response()
        if cachedResponse is not None:
            return cachedResponse
        
        assembly = await self.__validate_tracks([self._parameters.track])
        
        feature: Feature = self._parameters.location
        
        match feature.feature_type:
            case FeatureType.GENE:
                if feature.feature_id.startswith('ENSG'):
                    raise NotImplementedError(f'Mapping through Ensembl IDS not yet implemented')
                data: FILERApiDataResponse = await self.__get_gene_qtl_data_task(self._parameters.track, feature.feature_id)
                counts = TrackOverlap(track_id=self._parameters.track,num_overlaps=len(response.features))
                
                if self._responseConfig.content == ResponseContent.COUNTS:
                    return await self.generate_response(counts)
                
                cursor: FILERPaginationCursor = await self.__initialize_data_query_pagination([counts])
                result = self.__page_data_result(cursor, [response])
                return await self.generate_response(result, isCached=False)
    
            case FeatureType.VARIANT:
                if feature.feature_id.startswith('rs'):
                    raise NotImplementedError(f'Mapping through refSNP IDS not yet implemented')
                # chr:pos:ref-alt -> chr:pos-1:pos
                [chr, pos, ref, alt] = feature.feature_id.split(':')
                span = f'{chr}:{int(pos) - 1}-{pos}'
                self._parameters.update("assembly", assembly)
                self._parameters.update("span", span)
                return await self.get_track_data(validate=False)
            
            case FeatureType.SPAN:
                self._parameters.update("assembly", assembly)
                self._parameters.update("span", feature.feature_id)
                return await self.get_track_data(validate=False)
            
            case _:
                raise NotImplementedError(f'QTL queries for feature type ${str(feature.feature_type)} not yet implemented.')
        

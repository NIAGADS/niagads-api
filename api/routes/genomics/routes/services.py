from typing import List, Union
from fastapi import APIRouter, Depends, Query
from fastapi.responses import JSONResponse

from api.common.enums.response_properties import ResponseContent, ResponseFormat, ResponseView
from api.common.exceptions import RESPONSES
from api.common.helpers import Parameters, ResponseConfiguration

from api.models.base_response_models import BaseResponseModel, T_ResponseModel
from api.models.genome import GenomicRegion
from api.models.search import RecordSearchResult

from ..common.helpers import GenomicsRouteHelper
from ..dependencies.parameters import InternalRequestParameters
from ..queries.igvbrowser import IGVFeatureLookupQuery
from ..queries.search import SearchType, SiteSearchQueryDefinition

router = APIRouter(prefix="/service", responses=RESPONSES)

tags = ["Service"]
@router.get("/search", tags=tags, response_model=Union[List[RecordSearchResult]],
    name="Site Search",
    description="Find Alzheimer's GenomicsDB Records (features, tracks, collections) by identifier or keyword")

async def site_search(
    keyword: str = Query(description="feature identifier or keyword (NOTE: searches for gene symbols use exact, case-sensitive, matching)"),
    searchType: SearchType = Query(default=SearchType.GLOBAL, description=SearchType.get_description()),
    internal: InternalRequestParameters = Depends()
)->Union[List[RecordSearchResult]]:
    
    query = SiteSearchQueryDefinition(searchType=searchType)
    
    test = {'primary_key': 'ENSG00000130203', 'display': 'APOE', 'record_type': 'gene', 'match_rank': 0, 
            'matched_term': 'APOE', 
            'description': 'Gene // protein coding // apolipoprotein E // Also Known As: AD2 // Location: 19q13.32'}
    
    x = RecordSearchResult(**test)
    
    helper = GenomicsRouteHelper(
        internal,
        ResponseConfiguration(
            format=ResponseFormat.JSON,
            content=ResponseContent.FULL,
            view=ResponseView.DEFAULT,
            model=BaseResponseModel
        ),
        Parameters(keyword=keyword),
        query=query
    )

    result:T_ResponseModel = await helper.get_query_response()
    if len(result.response) == 0:
        return JSONResponse([]) 
    
    return result.response


tags = ["NIAGADS Genome Browser"]
@router.get("/igvbrowser/feature", tags=tags, 
    response_model=GenomicRegion, response_model_exclude_none=True,
    name="IGV Genome Browser feature lookup service",
    description="retrieve genomic location (variants) or footprint (genes) feature in the format required by the IGV Browser")

async def get_browser_feature_region(
    id: str,
    flank: int = Query(default=0, description='add flanking region +/- `flank` kb up- and downstream to the returned feature location'),
    internal: InternalRequestParameters = Depends()
) -> GenomicRegion:

    helper = GenomicsRouteHelper(
        internal,
        ResponseConfiguration(
            format=ResponseFormat.JSON,
            content=ResponseContent.FULL,
            view=ResponseView.DEFAULT,
            model=BaseResponseModel
        ),
        Parameters(id=id),
        query=IGVFeatureLookupQuery
    )
    
    result:T_ResponseModel = await helper.get_query_response()
    
    if len(result.response) == 0:
        return JSONResponse({}) # result.response
    
    # add the flank
    region = GenomicRegion(**result.response)
    region.start -= flank
    region.end += flank
        
    return region
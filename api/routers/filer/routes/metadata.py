from fastapi import APIRouter, Depends, Query
from fastapi.exceptions import RequestValidationError
from typing import Annotated, Union

from api.common.enums import ResponseContent, ResponseFormat, ResponseView
from api.common.exceptions import RESPONSES
from api.common.formatters import print_enum_values
from api.common.helpers import Parameters, ResponseConfiguration
from api.dependencies.parameters.filters import ExpressionType, FilterParameter
from api.dependencies.parameters.location import Assembly, assembly_param
from api.dependencies.parameters.optional import PaginationParameters, keyword_param
from api.models.base_response_models import PagedResponseModel

from ..common.helpers import FILERRouteHelper
from ..common.constants import TRACK_SEARCH_FILTER_FIELD_MAP
from ..models.filer_track import FILERTrackBriefResponse, FILERTrackResponse
from ..dependencies.parameters import InternalRequestParameters, required_query_track_id

router = APIRouter(prefix="/metadata", responses=RESPONSES)

tags = ["Track Metadata by ID"]

@router.get("/", tags=tags, response_model=Union[FILERTrackResponse, FILERTrackBriefResponse],
    name="Get metadata for multiple tracks",
    description="retrieve full metadata for one or more FILER track records")

async def get_track_metadata(
        track: str = Depends(required_query_track_id),
        content: str = Query(ResponseContent.FULL, description=ResponseContent.descriptive(description=True)),
        format: str = Query(ResponseFormat.JSON, description=ResponseFormat.generic(description=True)),
        internal: InternalRequestParameters = Depends()
    ) -> Union[FILERTrackBriefResponse, FILERTrackResponse]:
    
    rContent = ResponseContent.descriptive().validate(content, 'content', ResponseContent)
    helper = FILERRouteHelper(
        internal,
        ResponseConfiguration(
            format=ResponseFormat.generic().validate(format, 'format', ResponseFormat),
            content=rContent,
            model=FILERTrackResponse if rContent == ResponseContent.FULL \
                else FILERTrackBriefResponse 
        ), 
        Parameters(track=track)
    )
    return await helper.get_track_metadata()


tags = ['Record(s) by Text Search'] + ['Track Metadata by Text Search']
filter_param = FilterParameter(TRACK_SEARCH_FILTER_FIELD_MAP, ExpressionType.TEXT)

@router.get("/search", tags=tags, response_model=Union[PagedResponseModel, FILERTrackBriefResponse, FILERTrackResponse],
    name="Search for tracks", 
    description="find functional genomics tracks using category filters or by a keyword search against all text fields in the track metadata")

async def search_track_metadata(
        pagination: Annotated[PaginationParameters, Depends(PaginationParameters)],
        assembly: Assembly = Depends(assembly_param), 
        filter = Depends(filter_param), 
        keyword: str = Depends(keyword_param),
        content: str = Query(ResponseContent.FULL, description=ResponseContent.get_description(True)),
        format: str = Query(ResponseFormat.JSON, description=ResponseFormat.generic(description=True)),
        view: str =  Query(ResponseView.DEFAULT, description=ResponseView.get_description(True)),
        internal: InternalRequestParameters = Depends(),
    ) -> Union[PagedResponseModel, FILERTrackBriefResponse, FILERTrackResponse]:
    
    if filter is None and keyword is None:
        raise RequestValidationError('must specify either a `filter` and/or a `keyword` to search')
    
    rContent = ResponseContent.validate(content, 'content', ResponseContent)
    helper = FILERRouteHelper(
        internal,
        ResponseConfiguration(
            format=ResponseFormat.generic().validate(format, 'format', ResponseFormat),
            content=rContent,
            view=ResponseView.validate(view, 'view', ResponseView), 
            model=FILERTrackResponse if rContent == ResponseContent.FULL \
                else FILERTrackBriefResponse if rContent == ResponseContent.SUMMARY \
                    else PagedResponseModel
        ),
        Parameters(
            page=pagination.page,
            assembly=assembly,
            filter=filter,
            keyword=keyword)
    )
    
    return await helper.search_track_metadata()


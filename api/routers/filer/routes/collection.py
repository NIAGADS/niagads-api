from fastapi import APIRouter, Depends, Query
from typing import Union

from api.common.enums.response_properties import ResponseContent, ResponseFormat, ResponseView
from api.common.exceptions import RESPONSES
from api.common.helpers import Parameters, ResponseConfiguration

from api.dependencies.parameters.identifiers import path_collection_name
from api.dependencies.parameters.optional import page_param

from api.models.base_response_models import BaseResponseModel
from api.models.collection import CollectionResponse
from api.models.view_models import TableViewResponse

from api.routers.filer.common.helpers import FILERRouteHelper
from api.routers.filer.common.services import MetadataQueryService
from api.routers.filer.dependencies.parameters import InternalRequestParameters
from api.routers.filer.models.filer_track import FILERTrackSummaryResponse, FILERTrackResponse

router = APIRouter(prefix="/collection", tags = ["Collections"], responses=RESPONSES)

@router.get("/", 
    response_model=CollectionResponse, 
    name="Get FILER Track Collections", 
    description="list available collections of related FILER tracks")

async def get_collections(
    format: str = Query(ResponseFormat.JSON, description=ResponseFormat.generic(description=True)), 
    internal: InternalRequestParameters = Depends()
)-> CollectionResponse:
    

    helper = FILERRouteHelper(
        internal,
        ResponseConfiguration(
            format=ResponseFormat.generic().validate(format, 'format', ResponseFormat),
            content=ResponseContent.FULL,
            model=CollectionResponse
        ), 
        Parameters()
    )

    
    result = await MetadataQueryService(internal.session).get_collections()
    return await helper.generate_response(result)


@router.get("/{collection}",
    response_model=Union[BaseResponseModel, FILERTrackSummaryResponse, FILERTrackResponse, TableViewResponse],
    name="Get track metadata by collection", 
    description="retrieve full metadata for FILER track records associated with a collection")

async def get_collection_track_metadata(
    collection: str = Depends(path_collection_name),
    page: int=Depends(page_param),
    content: str = Query(ResponseContent.FULL, description=ResponseContent.get_description(True)),
    format: str = Query(ResponseFormat.JSON, description=ResponseFormat.generic(description=True)),
    view: str =  Query(ResponseView.DEFAULT, description=ResponseView.table(description=True)),
    internal: InternalRequestParameters = Depends()
)-> Union[BaseResponseModel, FILERTrackSummaryResponse, FILERTrackResponse, TableViewResponse]:
    
    rContent = ResponseContent.validate(content, 'content', ResponseContent)
    helper = FILERRouteHelper(
        internal,
        ResponseConfiguration(
            format=ResponseFormat.generic().validate(format, 'format', ResponseFormat),
            content=rContent,
            view=ResponseView.table().validate(view, 'view', ResponseView), 
            model=FILERTrackResponse if rContent == ResponseContent.FULL \
                else FILERTrackSummaryResponse if rContent == ResponseContent.SUMMARY \
                    else BaseResponseModel
        ), 
        Parameters(collection=collection, page=page)
    )
    
    return await helper.get_collection_track_metadata()

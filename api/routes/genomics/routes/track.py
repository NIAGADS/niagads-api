from fastapi import APIRouter, Depends, Query
from typing import Union

from api.common.enums.response_properties import ResponseContent, ResponseFormat, ResponseView
from api.common.exceptions import RESPONSES
from api.common.helpers import Parameters, ResponseConfiguration

from api.dependencies.parameters.optional import page_param
from api.dependencies.parameters.identifiers import path_track_id
from api.models.base_response_models import PagedResponseModel, BaseResponseModel
from api.models.view_models import TableViewResponse
from api.routes.genomics.common.helpers import GenomicsRouteHelper
from api.routes.genomics.dependencies.parameters import InternalRequestParameters
from api.routes.genomics.models.feature_score import GWASSumStatResponse, QTLResponse
from api.routes.genomics.models.genomics_track import GenomicsTrackResponse, GenomicsTrackSummaryResponse
from api.routes.genomics.queries.track_metadata import TrackMetadataQuery


router = APIRouter(prefix="/track", responses=RESPONSES)

tags = ["Record by ID", "Track Metadata by ID"]
@router.get("/{track}", tags=tags,
    response_model=Union[GenomicsTrackSummaryResponse, GenomicsTrackResponse, BaseResponseModel],
    name="Get track metadata",
    description="retrieve track metadata for the FILER record identified by the `track` specified in the path; use `content=summary` for a brief response")

async def get_track_metadata(
    track = Depends(path_track_id),
    content: str = Query(ResponseContent.SUMMARY, description=ResponseContent.descriptive(description=True)),
    format: str = Query(ResponseFormat.JSON, description=ResponseFormat.generic(description=True)),
    internal: InternalRequestParameters = Depends()
) -> Union[GenomicsTrackSummaryResponse, GenomicsTrackResponse, BaseResponseModel]:
    
    rContent = ResponseContent.descriptive().validate(content, 'content', ResponseContent)
    rFormat = ResponseFormat.generic().validate(format, 'format', ResponseFormat)
    helper = GenomicsRouteHelper(
        internal,
        ResponseConfiguration(
            content=rContent,
            format=rFormat,
            model = GenomicsTrackResponse if rContent == ResponseContent.FULL \
                else GenomicsTrackSummaryResponse
        ),
        Parameters(track=track),
        # idParameter='track',
        # query=TrackMetadataQuery
    )
    
    return await helper.get_track_metadata()
    # return await helper.get_query_response()


tags = ["Record by ID", "Track Data by ID"]

@router.get("/{track}/data", tags=tags,
    name="Get track data",
    response_model=Union[GWASSumStatResponse, QTLResponse, GenomicsTrackSummaryResponse, TableViewResponse, BaseResponseModel],
    description="Get the top scoring (most statistically-significant based on a p-value filter) variant associations or QTLs from a data track.")

async def get_track_data(
    track = Depends(path_track_id),
    page:int=Depends(page_param),
    content: str = Query(ResponseContent.FULL, description=ResponseContent.data(description=True)),
    format: str = Query(ResponseFormat.JSON, description=ResponseFormat.variant_score(description=True)),
    view: str = Query(ResponseView.DEFAULT, description=ResponseView.get_description()),
    internal: InternalRequestParameters = Depends()
) -> Union[GWASSumStatResponse, QTLResponse, GenomicsTrackSummaryResponse, TableViewResponse, BaseResponseModel]:
    
    rContent = ResponseContent.data().validate(content, 'content', ResponseContent)
    
    # GWAS, QTL, Table response models will be updated by the helper depending on query result
    helper = GenomicsRouteHelper(
        internal,
        ResponseConfiguration(
            content=rContent,
            format=ResponseFormat.variant_score().validate(format, 'format', ResponseFormat),
            view=ResponseView.validate(view, 'view', ResponseView),
            model=GenomicsTrackSummaryResponse if rContent == ResponseContent.SUMMARY \
                else PagedResponseModel
        ),
        Parameters(track=track, page=page),
        query=TrackMetadataQuery,
        idParameter='track'
    )

    return await helper.get_track_data_query_response()

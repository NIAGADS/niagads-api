from datetime import date
from sqlmodel import SQLModel
from typing import Optional, List

from api.common.enums.response_properties import ResponseView
from api.common.formatters import id2title

from api.models.base_response_models import PagedResponseModel
from api.models.track import GenericTrack, GenericTrackSummary
from api.models.track_properties import BiosampleCharacteristics
from api.models.database.metadata import FILERAccession

# Developer Note: not setting a default for optionals b/c coming from
# the SQLModel, which will have nulls if no value

# note this is a generic data model so that we can add summary fields (e.g., counts) as needed
class FILERTrackSummary(SQLModel, GenericTrackSummary):
    assay: Optional[str] 
    

class FILERTrack(SQLModel, GenericTrack):  
    assay: Optional[str]
    provenance: FILERAccession
    
    # FILER properties
    file_name: Optional[str]
    index_url: Optional[str]
    md5sum: Optional[str]
    raw_file_url: Optional[str]
    raw_file_md5sum: Optional[str]
    bp_covered: Optional[int] 
    number_of_intervals: Optional[int] 
    file_size: Optional[int]
    file_format: Optional[str]
    file_schema: Optional[str]    

    def get_view_config(self, view: ResponseView, **kwargs):
        return super().get_view_config(view, **kwargs)
    
    def to_view_data(self, view: ResponseView, **kwargs):
        return self.serialize(promoteObjs=True, exclude=['replicates'])
    
    def _build_table_config(self):
        config = super()._build_table_config()
        columns = [ c for c in config['columns'] if c['id'] not in ['biosample_characteristics', 
            'replicates', 'provenance', 'data_source'] ] # data source will be promoted from provenance 
        columns += [ {'id': f, 'header': id2title(f)} for f in BiosampleCharacteristics.model_fields]
        columns += [ {'id': f, 'header': id2title(f)} for f in FILERAccession.model_fields]
        config.update({'columns': columns })
        return config

class FILERTrackSummaryResponse(PagedResponseModel):
    response: List[FILERTrackSummary]
    
    def to_text(self, format: ResponseView, **kwargs):
        # fields could contain num_overlaps if a result is present
        fields = self.response[0].get_field_names() \
            if len(self.response) > 0 else FILERTrackSummary.get_model_fields()
        return super().to_text(format, fields=fields)

    
class FILERTrackResponse(PagedResponseModel):
    response: List[FILERTrack]

    def to_text(self, format: ResponseView, **kwargs):
        fields = FILERTrack.get_model_fields()
        return super().to_text(format, fields=fields)


